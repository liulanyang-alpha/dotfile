#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Single-file HTTP server with GitHub-style Markdown preview.

Usage:
    python betterhttpserver.py [port] [-b BIND]
    python betterhttpserver.py 8001            # http://127.0.0.1:8001/
    python betterhttpserver.py 8001 -b 0.0.0.0 # expose on LAN

Features:
  * .md / .markdown -> rendered HTML preview (GitHub Markdown style)
  * ?raw=1          -> raw Markdown, served as text/markdown; charset=utf-8
  * other files     -> normal download / directory listing
No third-party dependencies; marked.js and github-markdown-css are embedded.
"""

import argparse
import base64
import gzip
import html
import http.server
import io
import json
import os
import re
import socketserver
import time
import urllib.parse
import zipfile

_CSS_GZ = "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"
_JS_GZ = "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"

def _asset(blob: str) -> str:
    return gzip.decompress(base64.b64decode(blob)).decode("utf-8")

_CSS = _asset(_CSS_GZ)
_JS = _asset(_JS_GZ)

PAGE = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
__CSS__
html,body{margin:0;padding:0;}
body{background:#fff;color:#1f2328;}
.topbar{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:10px;padding:10px 18px;background:rgba(255,255,255,.92);backdrop-filter:blur(8px);border-bottom:1px solid #d0d7de;font:14px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;}
.topbar .name{font-weight:600;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.topbar a,.topbar button{flex:none;border:1px solid #d0d7de;background:#f6f8fa;color:#1f2328;border-radius:6px;padding:4px 10px;font-size:13px;cursor:pointer;text-decoration:none;}
.topbar a:hover,.topbar button:hover{background:#eef1f4;}
.wrap{max-width:920px;margin:0 auto;padding:28px 20px 80px;}
.markdown-body{box-sizing:border-box;}
@media (prefers-color-scheme: dark){
body{background:#0d1117;color:#e6edf3;}
.topbar{background:rgba(13,17,23,.92);border-color:#30363d;}
.topbar a,.topbar button{background:#21262d;border-color:#30363d;color:#e6edf3;}
}
</style>
</head>
<body>
<div class="topbar"><span class="name">__TITLE__</span><a href="?raw=1">源码</a><button onclick="window.print()">打印</button></div>
<div class="wrap"><article id="md" class="markdown-body"></article></div>
<pre id="source" hidden>__CONTENT__</pre>
<script>__JS__</script>
<script>
(function(){
  var src = document.getElementById('source').textContent;
  var el = document.getElementById('md');
  try { el.innerHTML = marked.parse(src, {gfm:true, breaks:false}); }
  catch (e) { el.textContent = src; }
})();
</script>
</body>
</html>"""

LIST_PAGE = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root{color-scheme:light dark;}
*{box-sizing:border-box;}
body{margin:0;background:#fff;color:#1f2328;font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;}
.topbar{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:12px;padding:10px 20px;background:rgba(255,255,255,.92);backdrop-filter:blur(8px);border-bottom:1px solid #d0d7de;}
.topbar .title{font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0;}
.topbar .count{color:#6e7781;font-size:12px;}
.topbar a,.topbar button,.topbar label{flex:none;border:1px solid #d0d7de;background:#f6f8fa;color:#1f2328;border-radius:6px;padding:4px 10px;font-size:13px;cursor:pointer;text-decoration:none;}
.topbar a:hover,.topbar button:hover,.topbar label:hover{background:#eef1f4;}
.crumbs{max-width:920px;margin:0 auto;padding:16px 20px 0;font-size:13px;color:#6e7781;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.crumbs a{color:#0969da;text-decoration:none;}
.crumbs a:hover{text-decoration:underline;}
.crumbs .sep{margin:0 6px;color:#afb8c1;}
.list{max-width:920px;margin:0 auto;padding:14px 20px 70px;}
.head,.row{display:flex;align-items:center;gap:10px;padding:6px 10px;border-radius:6px;}
.head{font-size:12px;color:#6e7781;border-bottom:1px solid #d0d7de;border-radius:0;padding-bottom:8px;margin-bottom:2px;}
.row{text-decoration:none;color:inherit;}
.row:hover{background:#f6f8fa;}
.ico{width:22px;flex:none;text-align:center;font-size:16px;font-family:"Apple Color Emoji","Segoe UI Emoji","Noto Color Emoji",sans-serif;}
.name{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;text-decoration:none;color:inherit;}
.size{width:92px;flex:none;text-align:right;color:#6e7781;font-size:12px;font-variant-numeric:tabular-nums;}
.time{width:148px;flex:none;text-align:right;color:#6e7781;font-size:12px;font-variant-numeric:tabular-nums;}
.dl{flex:none;width:26px;height:26px;line-height:24px;text-align:center;border-radius:6px;color:#6e7781;text-decoration:none;font-size:15px;opacity:.55;transition:opacity .15s,background .15s;}
.row:hover .dl{opacity:1;}
.dl:hover{background:#eaeef2;color:#0969da;}
.dir .name{color:#9a6700;font-weight:500;}
.md .name{color:#0969da;}
.py .name{color:#2da44e;}
.json .name,.conf .name{color:#bf8700;}
.code .name{color:#8250df;}
.web .name{color:#0550ae;}
.pdf .name,.doc .name,.ppt .name{color:#cf222e;}
.img .name{color:#bf3989;}
.zip .name{color:#6e7781;}
.sheet .name{color:#1a7f37;}
.media .name{color:#bc4c00;}
.db .name{color:#6e7781;}
.text .name{color:#57606a;}
.hidden{opacity:.55;}
.drop{position:fixed;inset:0;z-index:100;display:none;align-items:center;justify-content:center;background:rgba(9,105,218,.10);border:3px dashed #0969da;color:#0969da;font-size:20px;font-weight:600;}
.drop.on{display:flex;}
@media (max-width:600px){.time{display:none}.size{width:70px}}
@media (prefers-color-scheme:dark){
body{background:#0d1117;color:#e6edf3;}
.topbar{background:rgba(13,17,23,.92);border-color:#30363d;}
.head{border-color:#30363d;color:#8b949e;}
.row:hover{background:#161b22;}
.size,.time,.count{color:#8b949e;}
.crumbs{color:#8b949e;}
.crumbs a{color:#58a6ff;}
.topbar a,.topbar button,.topbar label{background:#21262d;border-color:#30363d;color:#e6edf3;}
.dl{color:#8b949e;}
.dl:hover{background:#21262d;color:#58a6ff;}
.drop{background:rgba(88,166,255,.12);border-color:#58a6ff;color:#58a6ff;}
.dir .name{color:#e3b341;}
.md .name{color:#58a6ff;}
.py .name{color:#3fb950;}
.json .name,.conf .name{color:#d29922;}
.code .name{color:#bc8cff;}
.web .name{color:#79c0ff;}
.pdf .name,.doc .name,.ppt .name{color:#ff7b72;}
.img .name{color:#f778ba;}
.sheet .name{color:#3fb950;}
.media .name{color:#ffa657;}
.text .name{color:#8b949e;}
}
</style>
</head>
<body>
<div class="topbar"><span class="title">__TITLE__</span><span class="count">__COUNT__ 项</span><label class="btn">上传<input id="file" type="file" multiple hidden></label></div>
<div class="crumbs">__CRUMBS__</div>
<div class="list">
<div class="head"><span class="ico"></span><span class="name">名称</span><span class="size">大小</span><span class="time">修改时间</span></div>
__ROWS__
</div>
<div id="drop" class="drop">松开以上传</div>
<script>
(function(){
  var drop = document.getElementById('drop');
  var input = document.getElementById('file');
  var depth = 0;
  function upload(files){
    if(!files || !files.length) return;
    var fd = new FormData();
    for(var i=0;i<files.length;i++) fd.append('file', files[i], files[i].name);
    drop.textContent = '上传中…';
    drop.classList.add('on');
    fetch(location.pathname, {method:'POST', body:fd}).then(function(r){
      if(!r.ok) return r.text().then(function(t){ throw new Error(t || ('HTTP ' + r.status)); });
      location.reload();
    }).catch(function(e){
      alert('上传失败：' + e.message);
      drop.classList.remove('on');
      drop.textContent = '松开以上传';
    });
  }
  if(input) input.addEventListener('change', function(){ upload(input.files); });
  window.addEventListener('dragenter', function(e){ e.preventDefault(); depth++; drop.classList.add('on'); });
  window.addEventListener('dragover', function(e){ e.preventDefault(); });
  window.addEventListener('dragleave', function(e){ e.preventDefault(); depth--; if(depth <= 0){ depth = 0; drop.classList.remove('on'); } });
  window.addEventListener('drop', function(e){ e.preventDefault(); depth = 0; drop.classList.remove('on'); upload(e.dataTransfer.files); });
})();
</script>
</body>
</html>"""

_ICONS = {
    ".md": ("📝", "md"), ".markdown": ("📝", "md"),
    ".py": ("🐍", "py"),
    ".js": ("📜", "code"), ".mjs": ("📜", "code"), ".cjs": ("📜", "code"),
    ".ts": ("📜", "code"), ".tsx": ("📜", "code"), ".jsx": ("📜", "code"),
    ".json": ("🧾", "json"), ".jsonc": ("🧾", "json"),
    ".yml": ("⚙️", "conf"), ".yaml": ("⚙️", "conf"), ".toml": ("⚙️", "conf"),
    ".ini": ("⚙️", "conf"), ".conf": ("⚙️", "conf"), ".env": ("⚙️", "conf"),
    ".html": ("🌐", "web"), ".htm": ("🌐", "web"),
    ".css": ("🎨", "web"), ".scss": ("🎨", "web"), ".less": ("🎨", "web"),
    ".sh": ("🖥️", "code"), ".bash": ("🖥️", "code"), ".zsh": ("🖥️", "code"),
    ".txt": ("📄", "text"), ".log": ("📄", "text"),
    ".pdf": ("📕", "pdf"),
    ".png": ("🖼️", "img"), ".jpg": ("🖼️", "img"), ".jpeg": ("🖼️", "img"),
    ".gif": ("🖼️", "img"), ".webp": ("🖼️", "img"), ".svg": ("🖼️", "img"),
    ".bmp": ("🖼️", "img"), ".ico": ("🖼️", "img"),
    ".zip": ("🗜️", "zip"), ".tar": ("🗜️", "zip"), ".gz": ("🗜️", "zip"),
    ".tgz": ("🗜️", "zip"), ".bz2": ("🗜️", "zip"), ".xz": ("🗜️", "zip"),
    ".7z": ("🗜️", "zip"), ".rar": ("🗜️", "zip"),
    ".csv": ("📊", "sheet"), ".xls": ("📊", "sheet"), ".xlsx": ("📊", "sheet"),
    ".doc": ("📘", "doc"), ".docx": ("📘", "doc"),
    ".ppt": ("📙", "ppt"), ".pptx": ("📙", "ppt"),
    ".mp4": ("🎬", "media"), ".mov": ("🎬", "media"), ".mkv": ("🎬", "media"),
    ".mp3": ("🎵", "media"), ".wav": ("🎵", "media"), ".flac": ("🎵", "media"),
    ".db": ("🗄️", "db"), ".sqlite": ("🗄️", "db"), ".sqlite3": ("🗄️", "db"),
    ".ipynb": ("📓", "code"),
    ".go": ("💻", "code"), ".rs": ("💻", "code"), ".c": ("💻", "code"),
    ".h": ("💻", "code"), ".cpp": ("💻", "code"), ".java": ("💻", "code"),
    ".rb": ("💻", "code"), ".php": ("💻", "code"),
    ".lock": ("🔒", "lock"),
}


def _icon_for(name, is_dir):
    if is_dir:
        return "📁", "dir"
    return _ICONS.get(os.path.splitext(name)[1].lower(), ("📄", "file"))


def _human_size(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return ("%d %s" % (n, unit)) if unit == "B" else ("%.1f %s" % (n, unit))
        n /= 1024.0


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = dict(http.server.SimpleHTTPRequestHandler.extensions_map)
    extensions_map.update({
        ".md": "text/markdown; charset=utf-8",
        ".markdown": "text/markdown; charset=utf-8",
    })

    def _is_markdown(self, path: str) -> bool:
        return path.lower().endswith((".md", ".markdown"))

    def list_directory(self, path):
        try:
            names = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None

        names.sort(key=lambda n: (not os.path.isdir(os.path.join(path, n)), n.casefold()))
        urlpath = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
        parts = [p for p in urlpath.split("/") if p]

        crumbs = ['<a href="/">🏠 根目录</a>']
        acc = ""
        for p in parts:
            acc += "/" + urllib.parse.quote(p)
            crumbs.append('<span class="sep">/</span><a href="%s/">%s</a>' % (acc, html.escape(p)))

        rows = []
        if parts:
            rows.append('<div class="row dir"><span class="ico">⬆️</span>'
                        '<a class="name" href="../">..</a><span class="size">—</span>'
                        '<span class="time"></span></div>')

        for name in names:
            full = os.path.join(path, name)
            is_dir = os.path.isdir(full)
            try:
                st = os.stat(full)
                mtime = time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime))
                size = "—" if is_dir else _human_size(st.st_size)
            except OSError:
                mtime, size = "", "—"
            icon, group = _icon_for(name, is_dir)
            href = urllib.parse.quote(name) + ("/" if is_dir else "")
            dl = href + ("?zip=1" if is_dir else "?download=1")
            dlname = (name + ".zip") if is_dir else name
            cls = "row " + group + (" hidden" if name.startswith(".") else "")
            rows.append(
                '<div class="%s"><span class="ico">%s</span>'
                '<a class="name" href="%s">%s%s</a><span class="size">%s</span>'
                '<span class="time">%s</span>'
                '<a class="dl" href="%s" title="下载" download="%s">⬇</a></div>' % (
                    cls, icon, href, html.escape(name), "/" if is_dir else "",
                    size, mtime, dl, html.escape(dlname)
                )
            )

        title = "文件 · " + os.path.abspath(path)
        page = (LIST_PAGE
                .replace("__TITLE__", html.escape(title))
                .replace("__COUNT__", str(len(names)))
                .replace("__CRUMBS__", "".join(crumbs))
                .replace("__ROWS__", "\n".join(rows)))
        data = page.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        return io.BytesIO(data)

    def send_head(self):
        parsed = urllib.parse.urlsplit(self.path)
        path = self.translate_path(parsed.path)
        query = urllib.parse.parse_qs(parsed.query)
        if os.path.isfile(path) and "download" in query:
            return self._send_download(path)
        if os.path.isdir(path) and "zip" in query:
            return self._send_zip(path)
        if os.path.isfile(path) and self._is_markdown(path) and "raw" not in query:
            return self._send_preview(path)
        return super().send_head()

    def _send_preview(self, path: str):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                raw = fh.read()
        except OSError:
            self.send_error(404, "File not found")
            return None
        title = os.path.basename(path)
        page = (PAGE
                .replace("__CSS__", _CSS)
                .replace("__JS__", _JS)
                .replace("__TITLE__", html.escape(title))
                .replace("__CONTENT__", html.escape(raw)))
        data = page.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        return io.BytesIO(data)

    def _send_download(self, path):
        try:
            fh = open(path, "rb")
            st = os.fstat(fh.fileno())
        except OSError:
            self.send_error(404, "File not found")
            return None
        name = os.path.basename(path)
        self.send_response(200)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Disposition",
                         "attachment; filename*=UTF-8''" + urllib.parse.quote(name))
        self.send_header("Content-Length", str(st.st_size))
        self.end_headers()
        return fh

    def _send_zip(self, path):
        base = os.path.basename(os.path.normpath(path)) or "download"
        buf = io.BytesIO()
        try:
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
                for root, _dirs, files in os.walk(path):
                    for fn in files:
                        full = os.path.join(root, fn)
                        if not os.path.isfile(full):
                            continue
                        zf.write(full, os.path.relpath(full, path))
        except OSError as exc:
            self.send_error(500, "zip failed: %s" % exc)
            return None
        data = buf.getvalue()
        self.send_response(200)
        self.send_header("Content-Type", "application/zip")
        self.send_header("Content-Disposition",
                         "attachment; filename*=UTF-8''" + urllib.parse.quote(base + ".zip"))
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        return io.BytesIO(data)

    def do_POST(self):
        parsed = urllib.parse.urlsplit(self.path)
        path = self.translate_path(parsed.path)
        if not os.path.isdir(path):
            self.send_error(405, "Upload target must be a directory")
            return
        ctype = self.headers.get("Content-Type", "")
        m = re.search(r'boundary="?([^";]+)"?', ctype, re.I)
        if not ctype.lower().startswith("multipart/form-data") or not m:
            self.send_error(415, "multipart/form-data required")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0:
            self.send_error(400, "empty body")
            return
        body = self.rfile.read(length)
        saved = self._save_uploads(path, body, m.group(1).encode("utf-8"))
        payload = json.dumps({"ok": True, "files": saved}, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _save_uploads(self, directory, body, boundary):
        delim = b"--" + boundary
        saved = []
        for part in body.split(delim):
            if not part.startswith(b"\r\n"):
                continue
            part = part[2:]
            if part.startswith(b"--") or b"\r\n\r\n" not in part:
                continue
            head, data = part.split(b"\r\n\r\n", 1)
            if data.endswith(b"\r\n"):
                data = data[:-2]
            headers = head.decode("utf-8", "replace")
            m = re.search(r"filename\*=(?:UTF-8'')?([^;\r\n]+)", headers, re.I)
            if m:
                name = urllib.parse.unquote(m.group(1).strip().strip('"'))
            else:
                m = (re.search(r'filename="([^"]*)"', headers, re.I)
                     or re.search(r"filename=([^;\r\n]+)", headers, re.I))
                name = m.group(1).strip().strip('"') if m else ""
            name = name.replace("\\", "/").split("/")[-1].strip()
            name = "".join(ch for ch in name if ch >= " " and ch not in "/\\")
            if not name or name in (".", ".."):
                continue
            target = os.path.join(directory, name)
            stem, ext = os.path.splitext(target)
            i = 1
            while os.path.exists(target):
                target = "%s (%d)%s" % (stem, i, ext)
                i += 1
            try:
                with open(target, "wb") as out:
                    out.write(data)
                saved.append(os.path.basename(target))
            except OSError:
                continue
        return saved

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args), flush=True)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("port", nargs="?", type=int, default=8000)
    parser.add_argument("-b", "--bind", default="127.0.0.1")
    args = parser.parse_args(argv)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer((args.bind, args.port), Handler) as httpd:
        print("Serving on http://%s:%d/" % (args.bind, args.port), flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
