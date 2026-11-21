#!/usr/bin/env python3
"""Gera a página do painel a partir do modelo.

uso: python3 scripts/build.py            -> painel/dist/radar.html (a página publicada no Claude)
     python3 scripts/build.py --preview  -> painel/dist/preview.html (com os dados de dados/produtos, para ver no navegador)
"""
import json, os, sys, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "https://github.com/andredabliu/radar-black-friday"
tpl = open(os.path.join(ROOT, "painel/radar.template.html"), encoding="utf-8").read()
charts = open(os.path.join(ROOT, "painel/charts.js"), encoding="utf-8").read()
out = tpl.replace("/*CHARTS*/", charts).replace("/*REPO*/", REPO)
name = "radar.html"
if "--preview" in sys.argv:
    prods = []
    for f in sorted(glob.glob(os.path.join(ROOT, "dados/produtos/*.json"))):
        d = json.load(open(f, encoding="utf-8")); d["id"] = os.path.basename(f)[:-5]
        d["imagem"] = "../../dados/imagens/" + d["id"] + ".jpg"
        prods.append(d)
    meta = json.load(open(os.path.join(ROOT, "dados/status.json"), encoding="utf-8"))
    out = out.replace("/*SAMPLE*/null", json.dumps({"produtos": prods, "meta": meta}, ensure_ascii=False))
    out = "<!doctype html><html><head><meta charset=utf-8><meta name=viewport content=\"width=device-width,initial-scale=1,viewport-fit=cover\"></head><body style=\"margin:0\">" + out + "</body></html>"
    name = "preview.html"
os.makedirs(os.path.join(ROOT, "painel/dist"), exist_ok=True)
open(os.path.join(ROOT, "painel/dist", name), "w", encoding="utf-8").write(out)
print(os.path.join("painel/dist", name))
