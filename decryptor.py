#!/usr/bin/env python3
"""
Jieshuo / AndroLua Plugin Decryptor and Decompiler
أداة فك تشفير وعكس حزم وإضافات قارئ الشاشة جيشوا إلى السورس كود الأصلي
"""

import argparse
import base64
import os
import re
import shutil
import string
import struct
import subprocess
import sys
import tempfile
import zipfile
import zlib
from pathlib import Path

CORE_MODULES = {
    "io",
    "os",
    "math",
    "table",
    "string",
    "coroutine",
    "utf8",
    "debug",
}

COMMON_EXACT = {
    "require",
    "import",
    "service",
    "this",
    "speak",
    "node",
    "execute",
    "print",
    "top",
    "bottom",
    "left",
    "right",
    "desc",
    "show",
    "title",
    "setItems",
    "Check",
    "check",
    "radio",
    "Radio",
    "dismiss",
    "dialog",
    "Dialog",
    "rect",
    "Rect",
    "parent",
    "child",
    "bounds",
    "Bounds",
    "BoundsInScreen",
    "ar",
    "en",
    "fr",
    "es",
    "tr",
    "de",
    "nl",
    "it",
    "pt",
    "ro",
    "ru",
    "ja",
    "zh",
    "sv",
    "th",
    "hi",
    "pl",
    "ko",
    "fa",
    "az",
    "bn",
    "bg",
    "ca",
    "cs",
    "da",
    "el",
    "et",
    "tl",
    "fi",
    "ka",
    "gu",
    "hr",
    "hy",
    "id",
    "eo",
    "is",
    "kn",
    "lv",
    "lt",
    "mk",
    "ml",
    "mt",
    "mr",
    "no",
    "uk",
    "pa",
    "rm",
    "sr",
    "sk",
    "sl",
    "sw",
    "ta",
    "te",
    "vi",
    "cy",
    "uz",
    "zu",
    "ur",
    "ms",
    "ku",
    "خطأ",
    "خطا",
    "سطر",
    "مربع",
    "نقطة",
    "نقطه",
    "شرطة",
    "شرطه",
    "فاصلة",
    "فاصله",
    "مسافة",
    "مسافه",
    "تخطي",
    "ترجم",
    "قلب",
    "ضحك",
    "حب",
    "سعادة",
    "مساعد",
    "ارسال",
    "إرسال",
    "انهاء",
    "إنهاء",
    "اعدادات",
    "إعدادات",
    "احصائيات",
    "إحصائيات",
    "tostring",
    "tonumber",
    "type",
    "table",
    "string",
    "math",
    "pairs",
    "ipairs",
    "error",
    "pcall",
    "xpcall",
    "coroutine",
    "utf8",
    "select",
    "next",
    "rawget",
    "rawset",
    "rawequal",
    "setmetatable",
    "getmetatable",
    "load",
    "loadfile",
    "loadstring",
    "floor",
    "ceil",
    "abs",
    "min",
    "max",
    "random",
    "randomseed",
    "sqrt",
    "sin",
    "cos",
    "tan",
    "deg",
    "rad",
    "exp",
    "log",
    "fmod",
    "modf",
    "format",
    "sub",
    "gsub",
    "find",
    "match",
    "gmatch",
    "rep",
    "reverse",
    "byte",
    "char",
    "dump",
    "pack",
    "unpack",
    "concat",
    "insert",
    "remove",
    "sort",
    "cjson",
    "json",
    "http",
    "Http",
    "task",
    "thread",
    "sleep",
    "newTimer",
    "Timer",
    "bind",
    "callEvent",
    "AccessibilityService",
    "AccessibilityNodeInfo",
    "isUseWebMove",
    "isUseViewMove",
    "isInWebView",
    "isNoneFocusView",
    "setUseWebMove",
    "setUseViewMove",
    "isAutoTrans",
    "setAutoTrans",
    "io",
    "os",
    "date",
    "time",
    "post",
    "get",
    "put",
    "delete",
    "head",
    "download",
    "upload",
    " | ",
    ": ",
    " - ",
    " = ",
    "topK",
    "topP",
    "temperature",
    "maxOutputTokens",
    "generationConfig",
    "contents",
    "parts",
    "inlineData",
    "mimeType",
    "models",
    "generateContent",
    "gemini_prefs",
    "api_counter",
    "MODE_PRIVATE",
    "getSharedPreferences",
    "encode",
    "decode",
    "compress",
    "toByteArray",
    "encodeToString",
    "NO_WRAP",
    "layout",
    "editor",
    "main",
    "init",
    "create",
    "split",
    "new",
    "id",
    "click",
    "text",
    "view",
    "get",
    "set",
    "call",
    "is",
    "has",
    "name",
    "data",
    "path",
    "file",
    "open",
    "read",
    "write",
    "close",
    "android",
    "widget",
    "app",
    "os",
    "content",
    "context",
    "activity",
    "Toast",
    "AlertDialog",
    "Builder",
    "Intent",
    "Uri",
    "Button",
    "TextView",
    "EditText",
    "ListView",
    "LinearLayout",
    "FrameLayout",
    "RelativeLayout",
    "loadlayout",
    "Environment",
    "SimpleDateFormat",
    "Date",
    "Bitmap",
    "ByteArrayOutputStream",
    "CompressFormat",
    "JPEG",
    "PNG",
    "Base64",
    "execute_command",
    "SplitEditView",
    "ArrayListAdapter",
    "LuaUtil",
    "rmDir",
    "zip",
    "unzip",
    "astable",
    "build_aly",
    "loopClick",
    "setSoftInputMode",
    "luaExtDir",
    "getLuaExtDir",
    "newActivity",
    "LuaDialog",
    "onItemClick",
    "onItemLongClick",
    "onCreateOptionsMenu",
    "onOptionsItemSelected",
    "onStart",
    "onStop",
    "onSave",
    "onTextChanged",
    "ZipOutputStream",
    "ZipEntry",
    "FileInputStream",
    "FileOutputStream",
    "dofile",
    "console",
    "startApp",
    "cancel",
    "filter",
    "SingleLine",
    "Hint",
    "Width",
    "无操作",
    "上个焦点",
    "下个焦点",
    "左快捷功能",
    "右快捷功能",
    "向上滚动",
    "向下滚动",
    "减少进度",
    "增加进度",
    "减小音量",
    "增大音量",
    "现在时间",
    "计时器",
    "当前位置",
    "虚拟屏幕",
    "验证码识别",
    "手势帮助",
    "黑屏模式",
    "剪切板",
    "收藏夹",
    "复制",
    "清空",
    "追加复制",
    "通知盒子",
    "抬手激活",
    "点击浏览",
    "节点浏览",
    "最近任务",
    "主屏幕",
    "返回",
    "点击",
    "长按",
    "长文本编辑",
    "高级菜单",
    "快捷菜单",
    "主菜单",
    "阅读模式",
    "逐字朗读",
    "逐字浏览",
    "自动浏览",
    "拆分浏览",
    "拆分编辑",
    "列表浏览",
    "全屏朗读",
    "全文浏览",
    "语音助手",
    "语音输入",
    "扩展插件",
    "扩展工具",
    "图片识别",
    "解说相机",
    "程序设置",
    "暂停触摸浏览",
    "暂停语音反馈",
    "通知栏",
    "编辑手势",
    "解说",
    "插件",
    "备份",
    "加密",
    "删除",
    "重命名",
    "保存",
    "查错",
    "输入循环次数",
    "输入按钮列表",
    "初始化代码",
    "循环执行代码",
    "循环次数",
    "后续操作代码",
    "定时间隔(单位秒)",
    # Arabic punctuation
    "،",
    "؛",
    "؟",
    # Common UI & Poll phrases
    "Select one",
    "selected",
    "not selected",
    "NONE",
    "checkbox",
    "poll",
    "cancel",
    # Lua patterns and format specifiers
    "^%s+",
    "%s+$",
    "%.$",
    "%d. %s%s",
    "[\u200e\u200f]",
    "^([^\r\n]+)",
    "^([^\n\r]+)",
}

COMMON_SUBSTR = {
    "layout",
    "editor",
    "click",
    "view",
    "text",
    "node",
    "service",
    "android",
    "widget",
    "trans",
    "auto",
    "focus",
    "move",
    "speak",
    "button",
    "image",
    "linear",
    "frame",
    "relative",
    "dialog",
    "alert",
    "toast",
    "intent",
    "context",
    "activity",
    "thread",
    "timer",
    "java",
    "util",
    "graphics",
    "bitmap",
    "base64",
    "input",
    "output",
}


def find_java() -> str | None:
    """Finds an available Java 8+ runtime executable."""
    found = shutil.which("java")
    if found:
        return found

    candidates = [
        Path(r"C:\Program Files (x86)\AudioRelay\runtime\bin\java.exe"),
        Path(r"C:\Program Files\Android\Android Studio\jbr\bin\java.exe"),
        Path(r"C:\Program Files\Common Files\Oracle\Java\javapath\java.exe"),
    ]
    for c in candidates:
        if c.exists():
            return str(c)

    for p in Path(r"C:\Program Files\Java").glob("*/bin/java.exe"):
        if p.exists():
            return str(p)

    for p in Path(r"C:\Program Files\Eclipse Adoptium").glob("*/bin/java.exe"):
        if p.exists():
            return str(p)

    return None


def decrypt_lua_buffer(data: bytes) -> tuple[bytes, str]:
    """
    Decodes/decrypts a Lua script buffer from Jieshuo/AndroLua.
    Recursively peels multi-layer wrappings (Base64 zlib payloads,
    AndroLua XOR streams, CJK Matrix protectors, XOR stagers, and custom packers).
    Returns: (decrypted_bytes, method_name)
    """
    current = data
    methods: list[str] = []

    for _ in range(10):
        if len(current) < 2:
            break

        # 1. Check load/loadstring wrappers
        m_load = re.search(
            rb'(?:load|loadstring)\s*\(\s*(?:["\']|\[=*\[)\s*(=[A-Za-z0-9+/=]+)',
            current,
        )
        if m_load:
            current = m_load.group(1)
            methods.append("load wrapper")
            continue

        # 2. Check Base64 (=H or direct) + Cumulative XOR + zlib
        if current.startswith(b"="):
            payloads = [b"H" + current[1:].strip(), current[1:].strip()]
            unpacked = None
            for raw_b64 in payloads:
                rem = len(raw_b64) % 4
                if rem != 0:
                    raw_b64 += b"=" * (4 - rem)
                try:
                    decoded = base64.b64decode(raw_b64)
                    if len(decoded) > 0 and decoded[0] == 0x1C:
                        acc = 0
                        buf = bytearray()
                        for b in decoded:
                            acc ^= b
                            buf.append(acc)
                        buf[0] = 0x78
                        try:
                            decomp = bytearray(zlib.decompress(bytes(buf)))
                            if decomp.startswith(b"\x1cLua"):
                                decomp[0] = 0x1B
                            unpacked = bytes(decomp)
                            methods.append("Base64 (=H) + Cumulative XOR + zlib")
                            break
                        except Exception:
                            pass
                    if decoded.startswith(b"\x1bLua") or all(
                        32 <= c <= 126 or c in (9, 10, 13) for c in decoded[:50]
                    ):
                        unpacked = decoded
                        methods.append("Base64 Direct Payload")
                        break
                except Exception:
                    continue
            if unpacked is not None:
                current = unpacked
                continue

        # 3. Check AndroLua XOR stream (0x1B)
        if len(current) > 1 and current[0] == 0x1B and current[1] != 0x4C:
            length = len(current)
            out = bytearray(length)
            out[0] = 0x1B
            for i in range(1, length):
                k = (i * length) % 255
                out[i] = current[i] ^ k
            methods.append("AndroLua XOR Stream (0x1B)")
            current = bytes(out)
            continue

        # 4. Check Jieshuo CJK Matrix Protector (bytecode)
        res_cjk = unpack_cjk_protector(current)
        if res_cjk is not None:
            cjk_bytes, cjk_name = res_cjk
            methods.append(cjk_name)
            current = cjk_bytes
            continue

        # 5. Check Lua XOR Stager (bytecode)
        res_stg = unpack_xor_stager(current)
        if res_stg is not None:
            stg_bytes, stg_name = res_stg
            methods.append(stg_name)
            current = stg_bytes
            continue

        # 6. Check custom packers
        res_p = unpack_decimal_array_packer(current)
        if res_p is not None:
            p_bytes, p_meth = res_p
            methods.append(p_meth)
            current = p_bytes
            continue

        res_p = unpack_custom_cbc_packer(current)
        if res_p is not None:
            p_bytes, p_meth = res_p
            methods.append(p_meth)
            current = p_bytes
            continue

        res_p = unpack_aes_reflection_packer(current)
        if res_p is not None:
            p_bytes, p_meth = res_p
            methods.append(p_meth)
            current = p_bytes
            continue

        break

    if not methods:
        if current.startswith(b"\x1bLua"):
            return current, "plaintext bytecode"
        return current, "plaintext"

    return current, " -> ".join(methods)


def score_candidate(cand_bytes: bytes, raw_bytes: bytes) -> float:
    try:
        s = cand_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return -1e9

    bad_ctrl = sum(1 for c in s if ord(c) < 32 and c not in "\n\t\r")
    if bad_ctrl > 0:
        return -10000.0 * bad_ctrl

    has_latin = any("a" <= c.lower() <= "z" for c in s)
    has_arabic = any("\u0600" <= c <= "\u06ff" or "\u0750" <= c <= "\u077f" for c in s)
    has_cyrillic = any("\u0400" <= c <= "\u052f" for c in s)
    has_cjk = any("\u4e00" <= c <= "\u9fff" or "\u3040" <= c <= "\u30ff" for c in s)
    if (
        (has_latin and has_arabic and " " not in s)
        or (has_cyrillic and has_arabic)
        or (has_cyrillic and has_cjk)
        or (has_latin and has_cjk and " " not in s)
    ):
        return -10000.0

    if s == "،":
        return 6000.0

    score = 0.0
    std_arabic = sum(1 for c in s if "\u0621" <= c <= "\u064a")
    ext_arabic = sum(
        1 for c in s if ("\u0600" <= c < "\u0621") or ("\u064b" <= c <= "\u06ff")
    )
    chinese = sum(1 for c in s if "\u4e00" <= c <= "\u9fff")
    score += std_arabic * 100.0 + ext_arabic * 20.0 + chinese * 50.0

    if any(s.startswith(p) for p in ("android.", "java.", "com.", "org.")):
        score += 1500.0

    s_lower = s.lower()
    if s in COMMON_EXACT:
        score += 2500.0
    elif s_lower in COMMON_EXACT:
        score += 800.0

    if s in CORE_MODULES:
        score += 500.0

    for w in COMMON_SUBSTR:
        if w in s_lower:
            score += 200.0

    for w in ("select", "selected", "option", "poll", "cancel", "vote"):
        if w in s_lower:
            score += 400.0

    if re.search(r"%[sSwWdDaApPcfegq%]", s):
        score += 1500.0
    if re.search(r"\^\[\^[a-zA-Z\r\n\t]+\]", s) or ("^(" in s and ")" in s):
        score += 1500.0

    if has_latin:
        if re.search(r"[bcdfghjklmnpqrstvwxyz]{5,}", s_lower):
            score -= 3000.0

    if s.isidentifier():
        score += 400.0
        is_lower = s.islower()
        is_upper = s.isupper()
        is_camel = (
            (s[0].islower() or s[0] == "_")
            and any(c.isupper() for c in s)
            and not any(
                s[i].isupper() and s[i + 1].isupper() for i in range(len(s) - 1)
            )
        )
        is_pascal = (
            s[0].isupper()
            and any(c.islower() for c in s)
            and not any(
                s[i].isupper() and s[i + 1].isupper() for i in range(len(s) - 1)
            )
        )
        is_snake = "_" in s and (s.islower() or s.isupper())
        if is_lower or is_upper or is_camel or is_pascal or is_snake:
            score += 200.0

        if has_latin:
            letters = [c for c in s_lower if c.isalpha()]
            if len(letters) >= 3:
                vowels = sum(1 for c in letters if c in "aeiou")
                ratio = vowels / len(letters)
                if 0.2 <= ratio <= 0.6:
                    score += 150.0
                elif ratio == 0 or ratio > 0.8:
                    score -= 150.0

    ascii_printable = sum(
        1 for c in s if c in string.printable and c not in "\r\x0b\x0c"
    )
    score += ascii_printable * 5.0
    if cand_bytes == raw_bytes:
        score += 50.0

    return score


def solve_string(raw: bytes) -> bytes:
    length = len(raw)
    if length == 0:
        return raw
    if length == 1:
        # Obfuscator unconditionally XORs 1-byte strings with 1 (len % 255)
        return bytes([raw[0] ^ 1])

    best_cand = raw
    best_score = score_candidate(raw, raw)
    for step in range(256):
        key = [length % 255]
        for _ in range(1, length):
            key.append((key[-1] + step) % 255)
        dec = bytes([raw[i] ^ key[i] for i in range(length)])
        sc = score_candidate(dec, raw)
        if sc > best_score:
            best_score = sc
            best_cand = dec
    return best_cand


class BytecodePatcher:
    """Parses Lua 5.3 bytecode and decrypts embedded string constants in-place."""

    def __init__(self, data: bytes):
        self.data = bytearray(data)
        self.pos = 0
        self.cint_size = 4
        self.sizet_size = 8
        self.inst_size = 4
        self.int_size = 8
        self.num_size = 8
        self.replacements: list[tuple[int, bytes]] = []

    def read_bytes(self, n: int = 1) -> bytes:
        p = self.pos
        end_pos = p + n
        res = bytes(self.data[p:end_pos])
        self.pos = end_pos
        return res

    def read_u8(self) -> int:
        return self.read_bytes(1)[0]

    def read_cint(self) -> int:
        fmt = "<I" if self.cint_size == 4 else "<Q"
        return struct.unpack(fmt, self.read_bytes(self.cint_size))[0]

    def read_sizet(self) -> int:
        fmt = "<I" if self.sizet_size == 4 else "<Q"
        return struct.unpack(fmt, self.read_bytes(self.sizet_size))[0]

    def read_int(self) -> int:
        fmt = "<i" if self.int_size == 4 else "<q"
        return struct.unpack(fmt, self.read_bytes(self.int_size))[0]

    def read_num(self) -> float:
        fmt = "<f" if self.num_size == 4 else "<d"
        return struct.unpack(fmt, self.read_bytes(self.num_size))[0]

    def read_str(self) -> bytes | None:
        b = self.read_u8()
        if b == 0:
            return None
        elif b == 0xFF:
            size = self.read_sizet()
        else:
            size = b
        str_len = size - 1
        pos = self.pos
        raw = self.read_bytes(str_len)
        sol = solve_string(raw)
        if sol != raw and len(sol) == len(raw):
            self.replacements.append((pos, sol))
        return sol

    def parse_header(self) -> None:
        self.read_bytes(4)  # 0x1bLua
        self.read_u8()
        self.read_u8()
        self.read_bytes(6)
        self.cint_size = self.read_u8()
        self.sizet_size = self.read_u8()
        self.inst_size = self.read_u8()
        self.int_size = self.read_u8()
        self.num_size = self.read_u8()
        self.read_bytes(self.int_size + self.num_size + 1)

    def parse_proto(self) -> None:
        self.read_str()  # source
        self.read_cint()  # linedefined
        self.read_cint()  # lastlinedefined
        self.read_u8()  # numparams
        self.read_u8()  # is_vararg
        self.read_u8()  # maxstacksize

        sizecode = self.read_cint()
        self.pos += sizecode * self.inst_size

        sizek = self.read_cint()
        for _ in range(sizek):
            t = self.read_u8()
            if t == 0:
                pass
            elif t == 1:
                self.read_u8()
            elif t in (3, 0x13):
                self.pos += 8
            elif t in (4, 0x14):
                self.read_str()

        sizeup = self.read_cint()
        self.pos += sizeup * 2

        sizep = self.read_cint()
        for _ in range(sizep):
            self.parse_proto()

        sizeline = self.read_cint()
        self.pos += sizeline * self.cint_size

        sizeloc = self.read_cint()
        for _ in range(sizeloc):
            self.read_str()
            self.read_cint()
            self.read_cint()

        sizeupn = self.read_cint()
        for _ in range(sizeupn):
            self.read_str()

    def patch(self) -> tuple[bytes, int]:
        try:
            self.parse_header()
            self.parse_proto()
            for pos, sol in self.replacements:
                end_pos = pos + len(sol)
                self.data[pos:end_pos] = sol
            return bytes(self.data), len(self.replacements)
        except Exception:
            return bytes(self.data), 0


def char_deobfuscate(s_bytes: bytes) -> bytes:
    """Decodes \\xHH encoded bytes with XOR 0x55 and 8-bit ROR 3."""
    s = s_bytes.decode("latin-1")
    out = []
    matches = re.findall(r"\\x([0-9a-fA-F]{2})", s)
    for h in matches:
        c = int(h, 16) ^ 0x55
        c = (c >> 3) | ((c << 5) & 0xFF)
        out.append(c)
    return bytes(out)


def reverse_sub(data: bytes, key: bytes) -> bytes:
    """Reverses byte unshifting: (b - k + 256) % 256."""
    res = bytearray(len(data))
    klen = len(key)
    for i in range(len(data)):
        res[i] = (data[i] - key[i % klen] + 256) % 256
    return bytes(res)


def unpack_cbc_xor(ct: bytes, key: bytes, iv: bytes) -> bytes:
    """Decrypts CBC mode XOR cipher with block size 16."""
    bs = 16
    pr = iv[:16]
    pt = bytearray()
    k_16 = key[:16]
    for i in range(0, len(ct), bs):
        end_idx = i + bs
        blk = ct[i:end_idx]
        if len(blk) < bs:
            blk = blk + b"\x00" * (bs - len(blk))
        dec = bytes([blk[j] ^ k_16[j % 16] for j in range(len(blk))])
        xblk = bytes([dec[j] ^ pr[j % 16] for j in range(len(dec))])
        pt.extend(xblk)
        pr = blk
    if len(pt) > 0:
        p = pt[-1]
        if 0 < p <= bs:
            return bytes(pt[:-p])
    return bytes(pt)


def extract_key_from_kf_bytecode(dec_kf: bytes) -> bytes | None:
    """Extracts the encryption key by evaluating the compiled kf function bytecode."""
    try:

        class KeyConstCollector(BytecodePatcher):
            def __init__(self, data: bytes):
                super().__init__(data)
                self.collected_strings: list[bytes] = []

            def read_str(self) -> bytes | None:
                b = self.read_u8()
                if b == 0:
                    return None
                elif b == 0xFF:
                    size = self.read_sizet()
                else:
                    size = b
                str_len = size - 1
                raw = self.read_bytes(str_len)
                sol = solve_string(raw)
                self.collected_strings.append(sol)
                return sol

        collector = KeyConstCollector(dec_kf)
        collector.parse_header()
        collector.parse_proto()

        hex_str = None
        key_str = None
        for s in collector.collected_strings:
            try:
                st = s.decode("latin-1")
                if re.match(r"^[0-9A-Fa-f]{32,}$", st):
                    hex_str = st
                elif len(s) in (32, 64) and not re.match(r"^[0-9A-Fa-f]+$", st):
                    key_str = s
            except Exception:
                pass

        if hex_str and key_str:
            raw_c1 = bytes.fromhex(hex_str)
            klen = len(key_str)
            return bytes([raw_c1[i] ^ key_str[i % klen] for i in range(len(raw_c1))])
    except Exception:
        pass
    return None


def unpack_decimal_array_packer(data: bytes) -> tuple[bytes, str] | None:
    """Unpacks decimal ASCII array packer: encodedCode = '61 73 ...'."""
    try:
        text = data.decode("utf-8", errors="ignore")
    except Exception:
        return None
    if "encodedCode" not in text:
        return None
    m = re.search(r'encodedCode\s*=\s*["\']([0-9\s]+)["\']', text)
    if not m:
        return None
    try:
        codes = [int(x) for x in m.group(1).split()]
        raw_payload = bytes(codes)
        dec, meth = decrypt_lua_buffer(raw_payload)
        return dec, f"Decimal Array (encodedCode) -> {meth}"
    except Exception:
        return None


def unpack_custom_cbc_packer(data: bytes) -> tuple[bytes, str] | None:
    """Unpacks custom multi-stage CBC-XOR packer with wrap_hex or comb_hex."""
    try:
        text = data.decode("utf-8", errors="ignore")
    except Exception:
        return None
    if "wrap_hex" not in text and "comb_hex" not in text:
        return None

    try:
        if "wrap_hex" in text:
            m = re.search(r'wrap_hex\s*=\s*["\']([0-9A-Fa-f]+)["\']', text)
            if not m:
                return None
            inner_script = bytes.fromhex(m.group(1)).decode("utf-8", errors="ignore")
        else:
            inner_script = text

        m_kf = re.search(r'kf_hex\s*=\s*["\']([0-9A-Fa-f]+)["\']', inner_script)
        m_comb = re.search(r'comb_hex\s*=\s*["\']([0-9A-Fa-f]+)["\']', inner_script)
        m_sk = re.search(r'sk_hex\s*=\s*["\']([0-9A-Fa-f]+)["\']', inner_script)
        if not (m_kf and m_comb and m_sk):
            return None

        kf_b = bytes.fromhex(m_kf.group(1))
        dec_kf, _ = decrypt_lua_buffer(kf_b)
        key = extract_key_from_kf_bytecode(dec_kf)
        if not key:
            return None

        comb_bin = bytes.fromhex(m_comb.group(1))
        sk = bytes.fromhex(m_sk.group(1))
        m_pad = re.search(r'padding_len\s*=\s*["\']?(\d+)["\']?', inner_script)
        padding_len = int(m_pad.group(1)) if m_pad else 0

        iv = comb_bin[:64]
        total_enc_len = len(comb_bin) - 64 - 32 - padding_len
        end_ed = 96 + total_enc_len
        ed = comb_bin[96:end_ed]

        deobf = char_deobfuscate(ed)
        rev = reverse_sub(deobf, sk)
        pt = unpack_cbc_xor(rev, key, iv)
        dec, meth = decrypt_lua_buffer(pt)
        return dec, f"Custom CBC-XOR Packer -> {meth}"
    except Exception:
        return None


def unpack_aes_reflection_packer(data: bytes) -> tuple[bytes, str] | None:
    """Unpacks Java reflection AES-256-CBC cipher with HMAC-SHA256."""
    try:
        text = data.decode("utf-8", errors="ignore")
    except Exception:
        return None
    if "_K1=" not in text or "_M1=" not in text or "_B64=" not in text:
        return None

    try:
        m1 = int(re.search(r"_M1=(\d+)", text).group(1))
        m2 = int(re.search(r"_M2=(\d+)", text).group(1))
        k1_str = re.search(r"_K1=\{([0-9, ]+)\}", text).group(1)
        k2_str = re.search(r"_K2=\{([0-9, ]+)\}", text).group(1)
        k1 = [int(x.strip()) for x in k1_str.split(",") if x.strip()]
        k2 = [int(x.strip()) for x in k2_str.split(",") if x.strip()]

        aes_key = bytes([k ^ m1 for k in k1] + [k ^ m2 for k in k2])
        iv_b64 = re.search(r"_IV=[\'\"]([^\'\"]+)[\'\"]", text).group(1)
        iv = base64.b64decode(iv_b64)
        b64_data = re.search(r"_B64=[\'\"]([^\'\"]+)[\'\"]", text).group(1)
        ct = base64.b64decode(b64_data)

        pt = None
        try:
            from cryptography.hazmat.primitives.ciphers import (
                Cipher,
                algorithms,
                modes,
            )
            from cryptography.hazmat.backends import default_backend

            cipher = Cipher(
                algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend()
            )
            dec_obj = cipher.decryptor()
            pt_pad = dec_obj.update(ct) + dec_obj.finalize()
            pad = pt_pad[-1]
            if 0 < pad <= 16:
                pt = pt_pad[:-pad]
            else:
                pt = pt_pad
        except Exception:
            pass

        if pt is None:
            with tempfile.NamedTemporaryFile(
                suffix=".bin", delete=False
            ) as f_ct, tempfile.NamedTemporaryFile(suffix=".bin", delete=False) as f_pt:
                f_ct.write(ct)
                f_ct_name, f_pt_name = f_ct.name, f_pt.name
            try:
                ps = (
                    f"$key = [byte[]]@({','.join(str(b) for b in aes_key)});"
                    f"$iv = [byte[]]@({','.join(str(b) for b in iv)});"
                    "$aes = [System.Security.Cryptography.Aes]::Create();"
                    "$aes.Key = $key;"
                    "$aes.IV = $iv;"
                    "$aes.Mode = [System.Security.Cryptography.CipherMode]::CBC;"
                    "$aes.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7;"
                    "$dec = $aes.CreateDecryptor();"
                    f"$ct = [System.IO.File]::ReadAllBytes('{f_ct_name}');"
                    "$pt = $dec.TransformFinalBlock($ct, 0, $ct.Length);"
                    f"[System.IO.File]::WriteAllBytes('{f_pt_name}', $pt);"
                )
                subprocess.run(["powershell", "-Command", ps], check=True)
                pt = Path(f_pt_name).read_bytes()
            finally:
                for p_tmp in (f_ct_name, f_pt_name):
                    try:
                        os.remove(p_tmp)
                    except Exception:
                        pass

        if pt:
            dec, meth = decrypt_lua_buffer(pt)
            return dec, f"AES-256-CBC Reflection Packer -> {meth}"
    except Exception:
        pass
    return None


def unpack_cjk_protector(data: bytes) -> tuple[bytes, str] | None:
    """Unpacks Chinese CJK Matrix Protector (解说代码加密 / 禁止进入程序!)."""
    if not data.startswith(b"\x1bLua"):
        return None
    try:
        p = BytecodePatcher(data)
        p.parse_header()

        def read_raw_str(p_obj: BytecodePatcher) -> bytes:
            b = p_obj.read_u8()
            if b == 0:
                return b""
            elif b == 0xFF:
                sz = p_obj.read_sizet()
            else:
                sz = b
            return p_obj.read_bytes(sz - 1)

        read_raw_str(p)
        p.read_cint()
        p.read_cint()
        p.read_u8()
        p.read_u8()
        p.read_u8()
        sizecode = p.read_cint()
        p.pos += sizecode * p.inst_size
        sizek = p.read_cint()
        raw_strings: list[bytes] = []
        for _ in range(sizek):
            t = p.read_u8()
            if t in (4, 0x14):
                raw_strings.append(read_raw_str(p))

        if not raw_strings:
            return None

        enc = max(raw_strings, key=len)
        if len(enc) < 300:
            return None

        length = len(enc)
        best_step = -1
        best_cnt = 0
        sample_len = min(length, 300)
        for step in range(256):
            key = [length % 255]
            for _ in range(1, sample_len):
                key.append((key[-1] + step) % 255)
            cand_sample = bytes([enc[i] ^ key[i] for i in range(sample_len)])
            cjk = sum(
                1
                for i in range(0, sample_len - 2, 3)
                if (0xE4 <= cand_sample[i] <= 0xE9)
                and (0x80 <= cand_sample[i + 1] <= 0xBF)
                and (0x80 <= cand_sample[i + 2] <= 0xBF)
            )
            if cjk > best_cnt:
                best_cnt = cjk
                best_step = step

        if best_cnt < 20 or best_step == -1:
            return None

        full_key = [length % 255]
        for _ in range(1, length):
            full_key.append((full_key[-1] + best_step) % 255)

        cand = bytes([enc[i] ^ full_key[i] for i in range(length)])
        vals: list[int] = []
        for i in range(0, len(cand) - 2, 3):
            b1, b2, b3 = cand[i], cand[i + 1], cand[i + 2]
            cp = (b1 - 224) * 4096 + (b2 - 128) * 64 + (b3 - 128)
            vals.append((cp - 19968) % 256)

        if not vals:
            return None

        kb = vals[0]
        decoded = bytes(
            [(vals[j] ^ (kb + (j % 32))) % 256 for j in range(1, len(vals))]
        )
        return decoded, f"CJK Protector (step {best_step})"
    except Exception:
        return None


def unpack_xor_stager(data: bytes) -> tuple[bytes, str] | None:
    """Unpacks Lua two-string repeating XOR stager."""
    if not data.startswith(b"\x1bLua"):
        return None
    try:
        p = BytecodePatcher(data)
        p.parse_header()

        def read_raw_str(p_obj: BytecodePatcher) -> bytes:
            b = p_obj.read_u8()
            if b == 0:
                return b""
            elif b == 0xFF:
                sz = p_obj.read_sizet()
            else:
                sz = b
            return p_obj.read_bytes(sz - 1)

        read_raw_str(p)
        p.read_cint()
        p.read_cint()
        p.read_u8()
        p.read_u8()
        p.read_u8()
        sizecode = p.read_cint()
        p.pos += sizecode * p.inst_size
        sizek = p.read_cint()
        raw_strings: list[bytes] = []
        for _ in range(sizek):
            t = p.read_u8()
            if t in (4, 0x14):
                raw_strings.append(read_raw_str(p))

        if len(raw_strings) < 2:
            return None

        k0, k1 = raw_strings[0], raw_strings[1]
        if len(k0) > 200 and len(k1) < 200:
            s_k0 = solve_string(k0)
            s_k1 = solve_string(k1)
            payload = bytes([s_k0[i] ^ s_k1[i % len(s_k1)] for i in range(len(s_k0))])
            return payload, "Lua XOR Stager"
        return None
    except Exception:
        return None


def unescape_lua_string(code: str) -> str:
    """Converts unluac decimal byte escape sequences into UTF-8 characters."""

    def repl(m: re.Match) -> str:
        byte_vals = [int(x[1:]) for x in re.findall(r"\\\d{1,3}", m.group(0))]
        b = bytes(byte_vals)
        try:
            return b.decode("utf-8")
        except UnicodeDecodeError:
            return m.group(0)

    return re.sub(r"(\\\d{1,3})+", repl, code)


def deobfuscate_registers(code: str) -> str:
    """Propagates compiler register assignments and eliminates synthetic locals."""
    lines = code.splitlines()
    out = []

    env_regs: set[str] = set()
    bindings: dict[str, str] = {}
    tail_regs: set[str] = set()

    re_local_decl = re.compile(r"^\s*local\s+[LA]\d+_\d+(?:,\s*[LA]\d+_\d+)*\s*$")
    re_assign = re.compile(r"^(\s*)([LA]\d+_\d+)\s*=\s*(.+)$")
    re_env_assign = re.compile(r"^(\s*)([LA]\d+_\d+)\.([a-zA-Z_0-9]+)\s*=\s*(.+)$")
    re_env_bracket = re.compile(r'^(\s*)([LA]\d+_\d+)\["([a-zA-Z_0-9]+)"\]\s*=\s*(.+)$')
    re_call_stmt = re.compile(r"^(\s*)([LA]\d+_\d+)\((.*)\)\s*$")
    re_multi_call = re.compile(
        r"^(\s*)([LA]\d+_\d+(?:\s*,\s*[LA]\d+_\d+)+)\s*=\s*(.+)$"
    )

    def sub_env(s: str) -> str:
        res = s
        for er in sorted(env_regs, key=len, reverse=True):
            res = re.sub(rf"\b{er}\.([a-zA-Z_0-9]+)\b", r"\1", res)
            res = re.sub(rf'\b{er}\["([a-zA-Z_0-9]+)"\]', r"\1", res)
            if res == er:
                return "_ENV"
        res = re.sub(r"\b_ENV\.([a-zA-Z_0-9]+)\b", r"\1", res)
        res = re.sub(r'\b_ENV\["([a-zA-Z_0-9]+)"\]', r"\1", res)
        return res

    def sub_regs(s: str) -> str:
        res = sub_env(s)
        for r in sorted(bindings.keys(), key=len, reverse=True):
            val = bindings[r]
            if val in ("{}",):
                continue
            res = re.sub(rf"\b{r}\b", lambda _, v=val: v, res)
        return sub_env(res)

    def clean_args(args_str: str) -> str:
        if not args_str.strip():
            return ""
        args = [a.strip() for a in args_str.split(",")]
        cleaned = []
        for a in args:
            if a in tail_regs:
                continue
            subbed = sub_regs(a)
            if re.match(r"^[LA]\d+_\d+$", subbed) and subbed not in bindings:
                continue
            cleaned.append(subbed)
        return ", ".join(cleaned)

    for line in lines:
        stripped = line.strip()

        if not stripped:
            out.append("")
            continue

        # 1. Skip local synthetic register header
        if re_local_decl.match(line):
            continue

        # 2. Check multi-assignment: L1_1, L2_1, ... = func(...)
        m_multi = re_multi_call.match(line)
        if m_multi:
            ind, lhs, val = m_multi.groups()
            regs = [r.strip() for r in lhs.split(",")]
            first_reg = regs[0]
            val_res = sub_regs(val)

            m_fn = re.match(r"^([a-zA-Z_0-9\.:]+)\((.*)\)$", val_res)
            is_void_action = False
            if m_fn:
                fn_name = m_fn.group(1)
                if any(
                    fn_name.startswith(p)
                    for p in ("service.", "this.", "Toast.", "print")
                ):
                    is_void_action = True

            if is_void_action:
                out.append(f"{ind}{val_res}")
                bindings.pop(first_reg, None)
            else:
                bindings[first_reg] = val_res

            for tr in regs[1:]:
                tail_regs.add(tr)
            continue

        # 3. Check env assign or single assign: L0_1 = _ENV or reg = val
        m_ass = re_assign.match(line)
        if m_ass:
            ind, reg, val = m_ass.groups()
            v_env = sub_env(val)
            if v_env in ("_ENV", "") or val in env_regs:
                env_regs.add(reg)
                continue

            val_res = sub_regs(val)

            if re.search(rf"\b{reg}\b", val_res):
                out.append(f"{ind}{reg} = {val_res}")
                bindings.pop(reg, None)
                continue

            if len(val_res) > 150:
                out.append(f"{ind}{reg} = {val_res}")
                bindings[reg] = reg
                continue

            m_fn = re.match(r"^([a-zA-Z_0-9\.:]+)\((.*)\)$", val_res)
            if m_fn:
                fn_name = m_fn.group(1)
                if any(
                    fn_name.startswith(p)
                    for p in (
                        "service.set",
                        "service.speak",
                        "this.set",
                        "this.speak",
                    )
                ):
                    out.append(f"{ind}{val_res}")
                    bindings.pop(reg, None)
                    continue

            bindings[reg] = val_res
            continue

        # 4. Check global/env property assign: L0_1.var = val
        m_env = re_env_assign.match(line)
        if m_env:
            ind, r_env, var, val = m_env.groups()
            if r_env in env_regs or r_env == "_ENV":
                val_res = sub_regs(val)
                out.append(f"{ind}{var} = {val_res}")
                continue

        m_bra = re_env_bracket.match(line)
        if m_bra:
            ind, r_env, var, val = m_bra.groups()
            if r_env in env_regs or r_env == "_ENV":
                val_res = sub_regs(val)
                out.append(f"{ind}{var} = {val_res}")
                continue

        # 5. Check call statement: L1_1(args)
        m_call = re_call_stmt.match(line)
        if m_call:
            ind, f_reg, args = m_call.groups()
            fname = sub_regs(f_reg)
            args_res = clean_args(args)
            out.append(f"{ind}{fname}({args_res})")
            continue

        # 6. Function definitions: function L1_1(A0_2)
        m_def = re.match(r"^(\s*)function\s+([a-zA-Z_0-9\.:]+)\s*\((.*)\)\s*$", line)
        if m_def:
            ind, fname, params = m_def.groups()
            bindings.clear()
            tail_regs.clear()
            out.append(f"{ind}function {fname}({params})")
            continue

        # 7. Return statements: return a, b, c
        m_ret = re.match(r"^(\s*)return(?:\s+(.+))?$", line)
        if m_ret:
            ind, ret_args = m_ret.groups()
            if not ret_args:
                out.append(f"{ind}return")
                continue
            cleaned_ret = clean_args(ret_args)
            out.append(f"{ind}return {cleaned_ret}")
            continue

        # 8. Control flow & other statements
        line_res = sub_regs(line)
        line_res = re.sub(r"if\s+(.+)\s+==\s+true\s+then", r"if \1 then", line_res)
        line_res = re.sub(
            r"elseif\s+(.+)\s+==\s+true\s+then", r"elseif \1 then", line_res
        )
        line_res = re.sub(r"if\s+(.+)\s+==\s+false\s+then", r"if not \1 then", line_res)
        line_res = re.sub(
            r"elseif\s+(.+)\s+==\s+false\s+then",
            r"elseif not \1 then",
            line_res,
        )

        out.append(line_res)

    return "\n".join(out)


def normalize_multiline_strings(code: str) -> str:
    """Normalizes unluac multiline string literals [[ ... ]] into escaped strings."""

    def repl(m: re.Match) -> str:
        s = m.group(1)
        if s.startswith("\n"):
            s = s[1:]
        escaped = (
            s.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("\t", "\\t")
        )
        return f'"{escaped}"'

    return re.sub(r"\[\[(.*?)\]\]", repl, code, flags=re.DOTALL)


def fold_functions(code_str: str) -> str:
    """Folds synthetic register function declarations into idiomatic ones.

    Example: function L0_1() ... end; name = L0_1 -> function name() ... end.
    """
    lines = code_str.splitlines()
    out = []
    i = 0
    re_block_open = re.compile(
        r"^\s*(?:if\b.*?\bthen\b|while\b.*?\bdo\b|for\b.*?\bdo\b|do\b|function\b)"
    )
    re_block_close = re.compile(r"^\s*end\b")

    while i < len(lines):
        line = lines[i]
        m_def = re.match(r"^(\s*)function\s+([LA]\d+_\d+)\s*\((.*)\)\s*$", line)
        if m_def:
            ind, reg, params = m_def.groups()
            depth = 1
            j = i + 1
            while j < len(lines):
                l_j = lines[j]
                if re_block_open.search(l_j):
                    depth += 1
                if re_block_close.search(l_j):
                    depth -= 1
                    if depth == 0:
                        break
                j += 1

            if j < len(lines) and j + 1 < len(lines):
                next_line = lines[j + 1].strip()
                m_assign = re.match(
                    r"^([a-zA-Z_0-9\.:]+)\s*=\s*" + re.escape(reg) + r"$",
                    next_line,
                )
                if m_assign:
                    real_name = m_assign.group(1)
                    slice_start = i + 1
                    body_lines = lines[slice_start:j]
                    body_text = fold_functions("\n".join(body_lines))
                    out.append(f"{ind}function {real_name}({params})")
                    if body_text:
                        out.append(body_text)
                    out.append(lines[j])
                    i = j + 2
                    continue
        out.append(line)
        i += 1
    return "\n".join(out)


def decompile_lua(data: bytes, jar_path: Path | None = None) -> tuple[str, str]:
    """
    Decompiles Lua bytecode into readable source code text.
    Returns: (lua_code_or_decompiled_text, method_info)
    """
    if not data.startswith(b"\x1bLua"):
        try:
            return data.decode("utf-8"), "Plaintext Lua Source"
        except UnicodeDecodeError:
            return data.decode("utf-8", errors="replace"), "Text (non-utf8)"

    # Patch bytecode string constants in-place
    patcher = BytecodePatcher(data)
    patched_data, num_patched = patcher.patch()

    # Find unluac.jar
    if jar_path is None or not jar_path.exists():
        local_jar = Path(__file__).resolve().parent / "unluac.jar"
        if local_jar.exists():
            jar_path = local_jar

    java_bin = find_java()
    if not java_bin or not jar_path or not jar_path.exists():
        patch_info = (
            f"Deobfuscated bytecode ({num_patched} strings patched)"
            if num_patched > 0
            else "Bytecode (Java/unluac missing)"
        )
        return patched_data.decode("latin-1"), patch_info

    # Run unluac decompilation
    with tempfile.NamedTemporaryFile(suffix=".luac", delete=False) as tf:
        tf.write(patched_data)
        temp_luac = tf.name

    try:
        proc = subprocess.run(
            [java_bin, "-jar", str(jar_path), "--nodebug", temp_luac],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0:
            decompiled = unescape_lua_string(proc.stdout)
            normalized = normalize_multiline_strings(decompiled)
            cleaned = deobfuscate_registers(normalized)
            folded = fold_functions(cleaned)
            info = f"Decompiled & Cleaned Source ({num_patched} strings deobfuscated)"
            return folded, info
        else:
            return patched_data.decode("latin-1"), "Bytecode (unluac error)"
    finally:
        try:
            os.remove(temp_luac)
        except OSError:
            pass


def process_file(file_path: Path, output_path: Path) -> None:
    data = file_path.read_bytes()
    decrypted, dec_method = decrypt_lua_buffer(data)
    code_text, decomp_method = decompile_lua(decrypted)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(code_text, encoding="utf-8")
    print(
        f"  [+] {file_path.name} -> {output_path.name} "
        f"({dec_method} -> {decomp_method})"
    )


def process_archive(archive_path: Path, output_dir: Path) -> None:
    print(f"[*] Processing package: {archive_path.name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    is_gpk = archive_path.suffix.lower() == ".gpk"
    with zipfile.ZipFile(archive_path, "r") as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            raw_data = z.read(info.filename)
            safe_name = info.filename.strip().rstrip(".")
            target_path = output_dir / safe_name
            target_path.parent.mkdir(parents=True, exist_ok=True)

            if info.filename == "init.lua":
                try:
                    text = raw_data.decode("utf-8")
                    target_path.write_text(text, encoding="utf-8")
                    print(
                        f"  [+] {info.filename}: manifest copied as-is "
                        f"({len(text.splitlines())} lines)"
                    )
                    continue
                except UnicodeDecodeError:
                    pass

            if info.filename == "config":
                try:
                    text = raw_data.decode("utf-8")
                    (output_dir / "config.json").write_text(text, encoding="utf-8")
                    target_path.write_text(text, encoding="utf-8")
                    print(
                        f"  [+] {info.filename}: gesture config saved "
                        f"({len(text.splitlines())} lines)"
                    )
                    continue
                except UnicodeDecodeError:
                    pass

            is_lua = (
                info.filename.endswith((".lua", ".luac", ".aly"))
                or raw_data.startswith(b"\x1bLua")
                or raw_data.startswith(b"=")
                or (len(raw_data) > 1 and raw_data[0] == 0x1B and raw_data[1] != 0x4C)
                or b"load(" in raw_data
                or b"loadstring(" in raw_data
                or is_gpk
            )

            if is_lua:
                decrypted, dec_method = decrypt_lua_buffer(raw_data)
                code_text, decomp_method = decompile_lua(decrypted)
                if info.filename.endswith((".lua", ".luac", ".aly")):
                    target_lua = target_path.with_suffix(".lua")
                else:
                    target_lua = output_dir / f"{safe_name}.lua"
                target_lua.write_text(code_text, encoding="utf-8")
                print(
                    f"  [+] {info.filename}: {dec_method} -> {decomp_method} "
                    f"({len(code_text.splitlines())} lines)"
                )
            else:
                target_path.write_bytes(raw_data)
                print(f"  [.] {info.filename}: copied as-is ({len(raw_data)} bytes)")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Jieshuo / AndroLua Plugin Decryptor & Decompiler - "
            "فك تشفير وعكس إضافات وحزم قارئ الشاشة جيشوا إلى السورس كود الأصلي"
        )
    )
    parser.add_argument(
        "input", type=Path, help="Path to .xpk, .ppk, .gpk, .zip, or .lua file"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output file or directory path",
    )
    args = parser.parse_args()

    input_path = args.input.resolve()
    if not input_path.exists():
        print(f"Error: Input path '{input_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if zipfile.is_zipfile(input_path):
        out_dir = (
            args.output.resolve()
            if args.output
            else input_path.parent / f"{input_path.stem}_decompiled"
        )
        process_archive(input_path, out_dir)
        print(f"\n[OK] Package decompiled successfully to: {out_dir}")
    else:
        out_file = (
            args.output.resolve()
            if args.output
            else input_path.parent / f"{input_path.stem}_decomp.lua"
        )
        process_file(input_path, out_file)
        print(f"\n[OK] File decompiled successfully to: {out_file}")


if __name__ == "__main__":
    main()
