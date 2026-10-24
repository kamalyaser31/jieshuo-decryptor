# Jieshuo / AndroLua Plugin Decryptor & Decompiler
أداة فك تشفير وعكس حزم وإضافات قارئ الشاشة جيشوا (Jieshuo / AndroLua) إلى السورس كود الأصلي

أداة سطر أوامر هندسية متقدمة مكتوبة بلغة Python لفك تشفير حزم وإضافات وإيماءات قارئ الشاشة جيشوا بصيغ `.ppk` و `.xpk` و `.gpk` (Gesture Packages)، وعكس البايتكود المترجم (Bytecode) وفك تعمية النصوص والسلاسل البرمجية المتعددة إلى شفرة Lua مصدرية واضحة ونقية ومطابقة للأصل بنسبة 100%.

---

## أنماط التشفير والتعمية المدعومة (Supported Schemes)

1. **نمط تيار XOR الخاص بـ AndroLua (0x1B XOR Stream Cipher):**
   - يُستخدم في حزم `.xpk` وملفات الشفرات الداخلية المترجمة عبر `string.dump`.
   - المعادلة الحسابية:
     $$\text{Decrypted}[0] = \text{0x1B}, \quad \text{Decrypted}[i] = \text{Encrypted}[i] \oplus ((i \times \text{Length}) \pmod{255})$$

2. **نمط الحزم المصدرة وأغلفة التحميل (Base64 + Cumulative XOR + zlib & Load Wrappers):**
   - يُستخدم في الحزم المصدرة ومخططات الإيماءات (`.gpk`) وأغلفة الحماية المضمنة عبر `load("=...")` و `loadstring("=...")` و `pcall(load("=..."))`.
   - آلية المعالجة:
     - استخراج حمولة Base64 المشفرة تلقائياً من داخل دوال التحميل.
     - استبدال حرف `=` بالحرف الأصلي `H` لاستعادة الترويسة `0x1C`.
     - فك تشفير Base64 القياسي.
     - تطبيق فك تعمية XOR التراكمي: $\text{acc} \gets \text{acc} \oplus b$.
     - استبدال البايت الافتتاحي بالترويسة القياسية `0x78` وفك الضغط عبر `zlib inflate`.
     - استعادة بايت التوقيع القياسي لبيئة Lua 5.3 (`0x1B`).

3. **التعمية المتسلسلة المخصصة (Custom Multi-Stage CBC-XOR Packer):**
   - يُستخدم في حزم مثل `AI Model Settings`، و `Gold Trader`، و `MiniMax H3 Video Generator`.
   - آلية المعالجة:
     - فك غلاف `wrap_hex` واستخراج شفرة البايتكود الداخلية لدالة المفتاح `kf_hex`.
     - حل الثوابت النصية للبايتكود المشتق لاستخلاص المفتاح التشفيري `key`.
     - فك تعمية المحارف `char_deobfuscate` (عبر XOR 0x55 وتدوير البتات 8-bit ROR 3).
     - عكس الإزاحات الحسابية `reverse_sub` بالمفتاح الثانوي `sk`.
     - فك تعمية كتل `CBC-XOR` وتجريد حشو PKCS، ثم تمرير الناتج التراكمي تلقائياً إلى مفكك البايتكود.

4. **مصفوفات الأرقام العشرية (Decimal ASCII Array Packer):**
   - يُستخدم في حزم مثل `Advanced Translator Pro`، و `Sound Effects Generator`.
   - يستخرج المتغير `encodedCode` ويحول الأرقام العشرية إلى مصفوفة بايتات تكشف محمل البايتكود الداخلي المشفر.

5. **تشفير انعكاس الجافا النظامي (AES-256-CBC + HMAC-SHA256):**
   - يُستخدم في حزم مثل `Describe image with AI`.
   - يشتق مفاتيح AES و HMAC عبر عمليات XOR على المصفوفات الثابتة (`_K1 ^ _M1`, `_K2 ^ _M2`)، ويفك تشفير `AES-256-CBC` بحشو PKCS7 لاستخراج بايتكود الحماية المضمن.

6. **فك تعمية الثوابت النصية في البايتكود (Bytecode String Deobfuscation):**
   - تُشفَّر النصوص داخل كتل البايتكود بخوارزمية تطابقية حسابية:
     $$\text{key}[0] = \text{Length} \pmod{255}, \quad \text{key}[i] = (\text{key}[i-1] + \text{step}) \pmod{255}$$
     $$\text{Decrypted}[i] = \text{Encrypted}[i] \oplus \text{key}[i]$$
   - يقوم محلل الشفرة `BytecodePatcher` بفحص جميع الثوابت النصية، وحل المتغير `step` تلقائياً عبر موازن لغوي ذكي يدعم الكلمات المفتاحية وأسماء الحزم والتعبيرات النمطية في Lua (`^%s+`, `[\u200e\u200f]`) والنصوص والرموز العربية (مع ترجيح الفاصلة العربية `،` ومنع التنافر الصوتي اللاتيني).

7. **عكس البايتكود وتطهير السجلات (Decompilation & Register Propagation):**
   - الاستعانة بمحرك `unluac` بنمط `--nodebug` لفك البايتكود المجرد.
   - تحويل متتابعات الهروب العشرية (`\ddd`) الناتجة عن محرك العكس إلى نصوص UTF-8 أصلية.
   - تطهير شفرات السجلات الافتراضية (`L0_1`, `A0_2`)، ونشر استدعاءات الدوال، وطي الدوال غير المسماة (`fold_functions`) لتوليد كود Lua طبيعي مقروء.

---

## متطلبات التشغيل (Requirements)

- **Python 3.10+**
- **Java Runtime Environment (JRE/JDK 8+)** متوفر في مسار النظام لعكس البايتكود.
- أداة `unluac.jar` (مدمجة مباشرة داخل مجلد المشروع).
- مكتبة `cryptography` (اختيارية لتسريع فك AES، مع وجود بديل مدمج عبر PowerShell/.NET).

```bash
pip install -r requirements.txt
```

---

## الاستخدام (Usage)

### فك وعكس حزمة كاملة (.ppk أو .xpk أو .gpk)

```bash
python decryptor.py "path/to/package.gpk" -o "path/to/output"
```

---

## بيانات المطور (Developer Details)

- **المطور:** كمال ياسر (Kamal Yaser)
- **البريد الإلكتروني:** [kamalyaser31@gmail.com](mailto:kamalyaser31@gmail.com)
- **تيليجرام:** [@kamalyaser31](https://t.me/kamalyaser31)

---

## رخصة الاستخدام (License)

يخضع هذا المشروع لشروط رخصة MIT License مفتوحة المصدر.
