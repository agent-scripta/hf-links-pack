#!/usr/bin/env python3
"""生成 Sentinel7/h3 的 hf-mirror.net 直链清单。只连 hf-mirror.net，不依赖 GitHub/HuggingFace 官方。"""
import json, urllib.parse, urllib.request, sys

REPO = sys.argv[1] if len(sys.argv) > 1 else "Sentinel7/h3"
MIRROR = "https://hf-mirror.net"
ONLY_WEIGHTS = "--all" not in sys.argv

print(f"拉取 {REPO} 文件列表 ...", file=sys.stderr)
d = json.load(urllib.request.urlopen(f"{MIRROR}/api/models/{REPO}", timeout=60))
paths = [s["rfilename"] for s in d["siblings"]]
if ONLY_WEIGHTS:
    paths = [p for p in paths if p.endswith(".safetensors")]
paths.sort(key=lambda p: p)

out = [f"{MIRROR}/{REPO}/resolve/main/{urllib.parse.quote(p, safe='/')}" for p in paths]
name = "hf-links.txt"
open(name, "w", encoding="utf-8").write("\n".join(out) + "\n")
print(f"已写入 {name}: {len(out)} 条", file=sys.stderr)
