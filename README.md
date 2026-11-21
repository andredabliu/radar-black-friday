# Radar Black Friday

Monitor pessoal de preços em lojas brasileiras. O Claude confere as lojas todo dia às 8h, atualiza o painel e grava aqui o histórico.

- **Painel:** https://claude.ai/artifact/Ne3kz5uEwCoLWENHSqoaMf
- **Produtos acompanhados:** `dados/produtos/<id>.json` (ficha, ofertas atuais, preço-alvo e menor preço de cada dia)

## Histórico

| Arquivo | O que guarda |
|---|---|
| `dados/historico-precos.csv` | Uma linha por loja por dia: `data, produto, loja, preco, preco_pix, verificado, disponivel, url` |
| `dados/menor-preco.csv` | Uma linha por produto por dia: o menor preço confirmado e a loja |
| `dados/status.json` | Última checagem e alertas do dia |

"Menor preço" considera o valor no Pix quando a loja informa e usa só ofertas verificadas (página aberta e preço visto) e com estoque. Ofertas com `verificado=false` vêm de resultados de busca, porque Mercado Livre e Magalu costumam bloquear acesso automatizado.

## Painel

`painel/radar.template.html` é o código da página. `python3 scripts/build.py` gera `painel/dist/radar.html`, que é a versão publicada no Claude; `--preview` gera uma prévia com os dados desta pasta para abrir no navegador.

Para acompanhar um produto novo, peça ao Claude no chat.
