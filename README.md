# Painel de Pedidos de Sementes — Power BI

Painel comercial de vendas de sementes (soja, trigo, aveia e milho), construído em **Power BI (PBIP/TMDL)**.
Todos os dados deste repositório são **fictícios**, gerados por script. A empresa "Lumina Sementes", os clientes, os vendedores, as cultivares e os valores foram inventados.

![Demonstração do painel](midia/painel_pedidos_demo.gif)

## O que o painel mostra
- **Visão Geral**: valor total, fechado × aberto, preço médio por bag, ranking de cultivares, obtentores, biotecnologias, receitas de tratamento (TSI), safras e vendedores.
- **Páginas de detalhamento** (drill-through): por cultivar, obtentor, receita de TSI, biotecnologia, TSI e vendedor. Cada uma traz KPIs, mapa por cidade, evolução mensal e tabela de clientes.
- **Cultivar × TSI × Embalagem**: matriz por cliente, com quantidades na embalagem original e em bags.

## Telas
| Visão Geral | Detalhe por Cultivar |
|---|---|
| ![Visão Geral](imagens/01_visao_geral.png) | ![Detalhe por Cultivar](imagens/02_detalhe_cultivar.png) |
| **Detalhe por Obtentor** | **Vendedor × Embalagem** |
| ![Detalhe por Obtentor](imagens/03_detalhe_obtentor.png) | ![Vendedor × Embalagem](imagens/04_detalhe_vendedor_embalagem.png) |

**Cultivar × TSI × Embalagem**
![Cultivar × TSI × Embalagem](imagens/05_cultivar_tsi_embalagem.png)

## Destaques técnicos
- Conversão de qualquer embalagem para **bag** por cultura (5MM, saca de 200 mil sementes, bigbag, saco em kg), numa coluna `FATOR_BAG` em DAX.
- Regras de negócio: itens cancelados ficam fora; no item fechado conta só a quantidade faturada; o TSI é proporcional.
- **Vendedor principal × canais de revenda**, por uma tabela de-para.
- Medidas com formato dinâmico, títulos dinâmicos e um total em SVG desenhado por medida DAX.
- Projeto em formato **PBIP**, versionável no Git.

📄 Todas as medidas, colunas calculadas e regras estão em [docs/MEDIDAS_DAX.md](docs/MEDIDAS_DAX.md).

## Como abrir
1. Rode `dados/gerar_base_ficticia.py` (Python 3, sem bibliotecas extras). Ele gera `pedidos_ficticios.csv`.
2. Abra `Pedidos_Sementes.pbip` no Power BI Desktop.
3. Em **Página Inicial → Transformar dados → Editar parâmetros**, aponte `Pasta_Dados` para a pasta `dados\` (com a barra no final).
4. Clique em **Atualizar**.

---
Desenvolvido por **César Barth** · Análise de Dados · [LinkedIn](https://www.linkedin.com/in/barthcesar07)
