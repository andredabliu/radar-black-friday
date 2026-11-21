#!/usr/bin/env python3
"""Gera a página do painel a partir do modelo.

uso: python3 scripts/build.py            -> painel/dist/radar.html (a página publicada no Claude)
     python3 scripts/build.py --pages    -> index.html na raiz (a versão pública no GitHub Pages, com os dados embutidos)
     python3 scripts/build.py --preview  -> painel/dist/preview.html (com os dados de dados/produtos, para ver no navegador)
"""
import json, os, sys, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "https://github.com/andredabliu/radar-black-friday"
PUBLIC = "https://andredabliu.github.io/radar-black-friday/"
tpl = open(os.path.join(ROOT, "painel/radar.template.html"), encoding="utf-8").read()
charts = open(os.path.join(ROOT, "painel/charts.js"), encoding="utf-8").read()
out = tpl.replace("/*CHARTS*/", charts).replace("/*REPO*/", REPO).replace("/*PUBLIC*/", PUBLIC)
name = "radar.html"
pages = "--pages" in sys.argv
if "--preview" in sys.argv or pages:
    prods = []
    for f in sorted(glob.glob(os.path.join(ROOT, "dados/produtos/*.json"))):
        d = json.load(open(f, encoding="utf-8")); d["id"] = os.path.basename(f)[:-5]
        d["imagem"] = ("" if pages else "../../") + "dados/imagens/" + d["id"] + ".jpg"
        prods.append(d)
    meta = json.load(open(os.path.join(ROOT, "dados/status.json"), encoding="utf-8"))
    lj = json.load(open(os.path.join(ROOT, "dados/lojas.json"), encoding="utf-8")) if os.path.exists(os.path.join(ROOT, "dados/lojas.json")) else {"lojas": {}}
    vgs = []
    for f in sorted(glob.glob(os.path.join(ROOT, "dados/viagens/*.json"))):
        d = json.load(open(f, encoding="utf-8")); d["id"] = os.path.basename(f)[:-5]; vgs.append(d)
    vm_path = os.path.join(ROOT, "dados/viagens-meta.json")
    vmeta = json.load(open(vm_path, encoding="utf-8")) if os.path.exists(vm_path) else None
    data = json.dumps({"produtos": prods, "meta": meta, "lojas": lj.get("lojas", {}), "lojasAt": lj.get("atualizado"), "viagens": vgs, "vmeta": vmeta}, ensure_ascii=False).replace("</", "<\\/")
    out = out.replace("/*SAMPLE*/null", data)
    out = "<!doctype html><html lang=\"pt-BR\"><head><meta charset=utf-8><meta name=viewport content=\"width=device-width,initial-scale=1,viewport-fit=cover\"><meta name=\"robots\" content=\"noindex\"></head><body style=\"margin:0\">" + out + "</body></html>"
    name = "preview.html"
if pages:
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(out)
    open(os.path.join(ROOT, ".nojekyll"), "w").write("")
    print("index.html"); sys.exit(0)
os.makedirs(os.path.join(ROOT, "painel/dist"), exist_ok=True)
open(os.path.join(ROOT, "painel/dist", name), "w", encoding="utf-8").write(out)
print(os.path.join("painel/dist", name))
