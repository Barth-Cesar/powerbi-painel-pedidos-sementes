# Medidas e regras DAX

Gerado a partir do modelo (TMDL). Todas as regras valem para a base fictícia deste repositório.

## Regras de negócio
- Itens **cancelados** ficam fora de todos os totais.
- Item **fechado** conta só a quantidade **faturada** (`QTD_EFETIVA`); o saldo fechado sem entrega não entra no vendido.
- **Valor TSI** é proporcional à quantidade efetiva.
- Toda embalagem é convertida para **bag** pelo `FATOR_BAG`: 5MM = 1 bag; saca de 200 mil sementes = 1/25; bigbag = 1; trigo em kg ÷ 1.000; aveia em kg ÷ 760; milho em sacas.
- **Vendedor principal**: primeiro o grupo do vendedor, depois o vendedor; canais de revenda ficam ligados ao vendedor principal (tabela `dVendedorPrincipal`).

## Colunas calculadas (FATO_ITENS_PEDIDO)

### MES_ANO_NUM
```dax
YEAR ( FATO_ITENS_PEDIDO[DATA_PEDIDO] ) * 100 + MONTH ( FATO_ITENS_PEDIDO[DATA_PEDIDO] )
```

### MES_ANO
```dax
FORMAT ( FATO_ITENS_PEDIDO[DATA_PEDIDO], "mmm/yy" )
```

### TEM_TSI
```dax
IF ( UPPER ( TRIM ( FATO_ITENS_PEDIDO[TRATAMENTO] ) ) IN { "SEM TRATAMENTO", "SEM TSI", "" }, "SEM TSI", "COM TSI" )
```

### LOCAL_MAPA
```dax
FATO_ITENS_PEDIDO[CIDADE_CLIENTE] & ", " & FATO_ITENS_PEDIDO[UF_CLIENTE] & ", Brasil"
```

### VENDEDOR_PRINCIPAL
```dax
VAR _g = LOOKUPVALUE ( dVendedorPrincipal[VENDEDOR_PRINCIPAL], dVendedorPrincipal[CHAVE], TRIM ( FATO_ITENS_PEDIDO[GRUPO_VENDEDOR] ) ) VAR _v = LOOKUPVALUE ( dVendedorPrincipal[VENDEDOR_PRINCIPAL], dVendedorPrincipal[CHAVE], TRIM ( FATO_ITENS_PEDIDO[VENDEDOR] ) ) RETURN COALESCE ( _g, _v, "Sem vínculo" )
```

### CANAL
```dax
VAR _v = LOOKUPVALUE ( dVendedorPrincipal[VENDEDOR_PRINCIPAL], dVendedorPrincipal[CHAVE], TRIM ( FATO_ITENS_PEDIDO[VENDEDOR] ) ) VAR _nome = TRIM ( FATO_ITENS_PEDIDO[VENDEDOR] ) RETURN IF ( _v = FATO_ITENS_PEDIDO[VENDEDOR_PRINCIPAL] || _nome = "Sem Vendedor" || _nome = "", "Venda direta", _nome )
```

### EMBALAGEM
```dax
VAR _u = TRIM ( FATO_ITENS_PEDIDO[UNIDADE_ORIGINAL] ) VAR _c = UPPER ( FATO_ITENS_PEDIDO[NOME_CULTURA] ) RETURN SWITCH ( TRUE (), _u = "5MM", "Bag", _u = "SC200", "Saca 200 mil", _u = "4MM", "Bag 4 milhões", _u = "140M", "Saca 140 mil", _u = "60M", "Saca 60 mil", _u = "80M", "Saca 80 mil", LEFT ( _u, 4 ) = "INAT" && CONTAINSSTRING ( _c, "MILHO" ), "Saca (cód. antigo)", LEFT ( _u, 4 ) = "INAT", "Bag (cód. antigo)", LEFT ( _u, 2 ) = "BB", "Bigbag " & TRIM ( MID ( _u, 3, 10 ) ) & " kg", _u = "TON", "Tonelada", _u = "KG", "Kg", LEFT ( _u, 2 ) = "SC", "Saco " & TRIM ( MID ( _u, 3, 10 ) ) & " kg", _u )
```

### RECEITA_TSI
```dax
VAR _t = TRIM ( FATO_ITENS_PEDIDO[TRATAMENTO] ) RETURN IF ( UPPER ( _t ) IN { "SEM TRATAMENTO", "SEM TSI", "" }, "SEM TSI", _t )
```

### KG_POR_UNIDADE
```dax
VAR _u = TRIM ( FATO_ITENS_PEDIDO[UNIDADE_ORIGINAL] ) RETURN SWITCH ( _u, "KG", 1, "TON", 1000, "SC25", 25, "SC40", 40, "SC50", 50, "SC60", 60, "BB 550", 550, "BB 600", 600, "BB 680", 680, "BB 700", 700, "BB 720", 720, "BB 760", 760, "BB 800", 800, "BB1000", 1000, DIVIDE ( FATO_ITENS_PEDIDO[QTD_PEDIDA_SACASPADRAO], FATO_ITENS_PEDIDO[QUANTIDADE_ORIGINAL] ) )
```

### FATOR_BAG
```dax
-- Quantos BAGS vale 1 unidade da embalagem do pedido (regras por cultura - 16/10/2026)
VAR _u = TRIM ( FATO_ITENS_PEDIDO[UNIDADE_ORIGINAL] )
VAR _c = UPPER ( FATO_ITENS_PEDIDO[NOME_CULTURA] )
VAR _kg = FATO_ITENS_PEDIDO[KG_POR_UNIDADE]
RETURN
    SWITCH (
        TRUE (),
        CONTAINSSTRING ( _c, "MILHO" ), 1,                      -- milho: sacas como estão no banco
        CONTAINSSTRING ( _c, "SOJA" ),
            SWITCH (
                TRUE (),
                _u = "5MM", 1,
                _u = "SC200", 1 / 25,
                _u = "4MM", 0.8,
                _u = "140M", 0.028,
                LEFT ( _u, 2 ) = "BB", 1,                         -- cada bigbag = 1 bag
                LEFT ( _u, 4 ) = "INAT", 1,
                DIVIDE ( _kg, 1000 )                              -- saco/kg: peso / 1.000 kg
            ),
        CONTAINSSTRING ( _c, "AVEIA" ), DIVIDE ( _kg, 760 ),  -- aveia: bag de 760 kg
        CONTAINSSTRING ( _c, "TRIGO" ), DIVIDE ( _kg, 1000 ), -- trigo: bag de 1.000 kg
        DIVIDE ( _kg, 1000 )
    )
```

### QTD_EFETIVA
```dax
IF ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] = "FECHADO", FATO_ITENS_PEDIDO[QTD_FATURADA], FATO_ITENS_PEDIDO[QUANTIDADE_ORIGINAL] )
```

## Medidas

### Pasta: 1. Pedidos

**Nº Pedidos**
```dax
CALCULATE ( DISTINCTCOUNT ( FATO_ITENS_PEDIDO[ID_PEDIDO_INTERNO] ), KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] <> "CANCELADO" ) )
```

**Nº Clientes**
```dax
CALCULATE ( DISTINCTCOUNT ( FATO_ITENS_PEDIDO[COD_CLIENTE] ), KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] <> "CANCELADO" ) )
```

**Nº Itens Fechados**
```dax
CALCULATE ( COUNTROWS ( FATO_ITENS_PEDIDO ), KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] = "FECHADO" ) )
```

**Nº Itens Abertos**
```dax
CALCULATE ( COUNTROWS ( FATO_ITENS_PEDIDO ), KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] = "ABERTO" ) )
```

### Pasta: 2. Valores

**Valor Sementes**
```dax
CALCULATE ( SUMX ( FATO_ITENS_PEDIDO, FATO_ITENS_PEDIDO[QTD_EFETIVA] * FATO_ITENS_PEDIDO[VALOR_UN_SEMENTE] ), KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] <> "CANCELADO" ) )
```

**Valor TSI**
```dax
CALCULATE ( SUMX ( FATO_ITENS_PEDIDO, FATO_ITENS_PEDIDO[VALOR_TSI] * DIVIDE ( FATO_ITENS_PEDIDO[QTD_EFETIVA], FATO_ITENS_PEDIDO[QUANTIDADE_ORIGINAL] ) ), KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] <> "CANCELADO" ) )
```

**Valor Total**
```dax
[Valor Sementes] + [Valor TSI]
```

**Valor Fechado**
```dax
CALCULATE ( [Valor Total], KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] = "FECHADO" ) )
```

**Valor Aberto**
```dax
CALCULATE ( [Valor Total], KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] = "ABERTO" ) )
```

**Preço Médio por Bag**
```dax
DIVIDE ( [Valor Sementes], [Bags Total] )
```

### Pasta: 3. Quantidades

**Bags Total**
```dax
CALCULATE ( SUMX ( FATO_ITENS_PEDIDO, FATO_ITENS_PEDIDO[QTD_EFETIVA] * FATO_ITENS_PEDIDO[FATOR_BAG] ), KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] <> "CANCELADO" ) )
```

**Bags Fechado**
```dax
CALCULATE ( [Bags Total], KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] = "FECHADO" ) )
```

**Bags Aberto**
```dax
CALCULATE ( [Bags Total], KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] = "ABERTO" ) )
```

**Bags Faturado**
```dax
CALCULATE ( SUMX ( FATO_ITENS_PEDIDO, FATO_ITENS_PEDIDO[QTD_FATURADA] * FATO_ITENS_PEDIDO[FATOR_BAG] ), KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] <> "CANCELADO" ) )
```

**Bags a Faturar**
```dax
CALCULATE ( SUMX ( FATO_ITENS_PEDIDO, FATO_ITENS_PEDIDO[QTD_A_FATURAR] * FATO_ITENS_PEDIDO[FATOR_BAG] ), KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] = "ABERTO" ) )
```

**Bags Entregue**
```dax
CALCULATE ( SUMX ( FATO_ITENS_PEDIDO, FATO_ITENS_PEDIDO[QTD_ENTREGUE] * FATO_ITENS_PEDIDO[FATOR_BAG] ), KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] <> "CANCELADO" ) )
```

**Bags a Entregar**
```dax
CALCULATE ( SUMX ( FATO_ITENS_PEDIDO, FATO_ITENS_PEDIDO[QTD_A_ENTREGAR] * FATO_ITENS_PEDIDO[FATOR_BAG] ), KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] = "ABERTO" ) )
```

**Bags Top 5 Cultivares**
```dax
VAR _top5 = CALCULATETABLE ( TOPN ( 5, VALUES ( FATO_ITENS_PEDIDO[CULTIVAR] ), [Bags Total], DESC ), ALLSELECTED ( FATO_ITENS_PEDIDO[CULTIVAR] ), ALLSELECTED ( FATO_ITENS_PEDIDO[MES_ANO] ), ALLSELECTED ( FATO_ITENS_PEDIDO[MES_ANO_NUM] ) ) RETURN IF ( SELECTEDVALUE ( FATO_ITENS_PEDIDO[CULTIVAR] ) IN _top5, [Bags Total] )
```

**Peso (kg)**
```dax
CALCULATE ( SUM ( FATO_ITENS_PEDIDO[QTD_PEDIDA_SACASPADRAO] ), KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] <> "CANCELADO" ) )
```

**Bags Com TSI**
```dax
CALCULATE ( [Bags Total], KEEPFILTERS ( FATO_ITENS_PEDIDO[TEM_TSI] = "COM TSI" ) )
```

**% Com TSI**
```dax
DIVIDE ( [Bags Com TSI], [Bags Total] )
```

**Bags Sem TSI**
```dax
CALCULATE ( [Bags Total], KEEPFILTERS ( FATO_ITENS_PEDIDO[TEM_TSI] = "SEM TSI" ) )
```

**Sacas 200 mil (equivalente)**
```dax
[Bags Total] * 25
```

**Total em Bags**
```dax
[Bags Total]
```

**Qtd Pedida**
```dax
CALCULATE ( SUM ( FATO_ITENS_PEDIDO[QTD_EFETIVA] ), KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] <> "CANCELADO" ) )
```

**Bags (com % do total)**
```dax
[Bags Total]
```

### Pasta: 4. Conferência

**Qtd sem Regra de Bag**
```dax
CALCULATE ( SUM ( FATO_ITENS_PEDIDO[QTD_EFETIVA] ), ISBLANK ( FATO_ITENS_PEDIDO[FATOR_BAG] ), KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] <> "CANCELADO" ) )
```

**Bags sem Vínculo de Vendedor**
```dax
CALCULATE ( [Bags Total], KEEPFILTERS ( FATO_ITENS_PEDIDO[VENDEDOR_PRINCIPAL] = "Sem vínculo" ) )
```

**Qtd Fechada sem Entrega**
```dax
CALCULATE ( SUMX ( FATO_ITENS_PEDIDO, FATO_ITENS_PEDIDO[QUANTIDADE_ORIGINAL] - FATO_ITENS_PEDIDO[QTD_FATURADA] ), KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] = "FECHADO" ) )
```

### Pasta: 4. Títulos

**Total Bags (texto)**
```dax
"Total: " & FORMAT ( [Bags Total], "#,0" ) & " bags"
```

**Total Bags (card)**
```dax
FORMAT ( [Bags Total], "#,0" ) & " bags"
```

**SVG Total Bags**
```dax
VAR _v = FORMAT ( [Bags Total], "#,0" ) & " bags" VAR _svg = "<svg xmlns='http://www.w3.org/2000/svg' width='340' height='30'>" & "<defs><linearGradient id='g' x1='0' x2='1'><stop offset='0' stop-color='#9DCBDB'/><stop offset='1' stop-color='#16425B'/></linearGradient></defs>" & "<text x='0' y='20' font-family='Segoe UI' font-size='12' font-weight='600' fill='#5B6B78'>Bags Total</text>" & "<rect x='74' y='8' width='96' height='14' rx='2' fill='url(#g)'/>" & "<text x='180' y='21' font-family='Segoe UI' font-size='16' font-weight='700' fill='#16425B'>" & _v & "</text></svg>" RETURN "data:image/svg+xml;utf8," & SUBSTITUTE ( _svg, "#", "%23" )
```

### Pasta: 5. Títulos

**Título Cultivar**
```dax
"Cultivar: " & SELECTEDVALUE ( FATO_ITENS_PEDIDO[CULTIVAR], "vários selecionados" )
```

**Título Obtentor**
```dax
"Obtentor: " & SELECTEDVALUE ( FATO_ITENS_PEDIDO[GRUPO_CULTIVAR], "vários selecionados" )
```

**Título Receita**
```dax
"Receita TSI: " & SELECTEDVALUE ( FATO_ITENS_PEDIDO[TRATAMENTO], "vários selecionados" )
```

**Título Biotecnologia**
```dax
"Biotecnologia: " & SELECTEDVALUE ( FATO_ITENS_PEDIDO[BIOTECNOLOGIA], "vários selecionados" )
```

**Título TSI**
```dax
"TSI: " & SELECTEDVALUE ( FATO_ITENS_PEDIDO[TEM_TSI], "vários selecionados" )
```

**Título Vendedor**
```dax
"Vendedor: " & SELECTEDVALUE ( FATO_ITENS_PEDIDO[VENDEDOR_PRINCIPAL], "vários selecionados" )
```

**Título Vendedor Embalagem**
```dax
"Vendedor: " & SELECTEDVALUE ( FATO_ITENS_PEDIDO[VENDEDOR_PRINCIPAL], "vários selecionados" ) & " · embalagem do pedido"
```

**Título Cliente**
```dax
IF ( HASONEVALUE ( FATO_ITENS_PEDIDO[CLIENTE] ), "Cliente: " & SELECTEDVALUE ( FATO_ITENS_PEDIDO[CLIENTE] ), "Todos os clientes · escolha um cliente no filtro acima" )
```

### Pasta: 6. Embalagem do pedido

**Embalagem Selecionada**
```dax
SELECTEDVALUE ( FATO_ITENS_PEDIDO[EMBALAGEM], "Bag" )
```

**Qtd na Embalagem**
```dax
VAR _e = [Embalagem Selecionada] RETURN CALCULATE ( SUM ( FATO_ITENS_PEDIDO[QTD_EFETIVA] ), FATO_ITENS_PEDIDO[EMBALAGEM] = _e, KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] <> "CANCELADO" ) )
```

**Qtd na Embalagem Com TSI**
```dax
CALCULATE ( [Qtd na Embalagem], KEEPFILTERS ( FATO_ITENS_PEDIDO[TEM_TSI] = "COM TSI" ) )
```

**Qtd na Embalagem Sem TSI**
```dax
CALCULATE ( [Qtd na Embalagem], KEEPFILTERS ( FATO_ITENS_PEDIDO[TEM_TSI] = "SEM TSI" ) )
```

**Valor na Embalagem**
```dax
VAR _e = [Embalagem Selecionada] RETURN CALCULATE ( [Valor Total], FATO_ITENS_PEDIDO[EMBALAGEM] = _e )
```

**Preço Médio na Embalagem**
```dax
VAR _e = [Embalagem Selecionada] RETURN DIVIDE ( CALCULATE ( [Valor Sementes], FATO_ITENS_PEDIDO[EMBALAGEM] = _e ), [Qtd na Embalagem] )
```

**Bags (pedidos em bag)**
```dax
CALCULATE ( SUM ( FATO_ITENS_PEDIDO[QTD_EFETIVA] ), FATO_ITENS_PEDIDO[EMBALAGEM] = "Bag", KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] <> "CANCELADO" ) )
```

**Sacas (pedidos em saca)**
```dax
CALCULATE ( SUM ( FATO_ITENS_PEDIDO[QTD_EFETIVA] ), FATO_ITENS_PEDIDO[EMBALAGEM] = "Saca 200 mil", KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] <> "CANCELADO" ) )
```

**R$ por Bag (pedidos em bag)**
```dax
DIVIDE ( CALCULATE ( [Valor Sementes], FATO_ITENS_PEDIDO[EMBALAGEM] = "Bag" ), [Bags (pedidos em bag)] )
```

**R$ por Saca (pedidos em saca)**
```dax
DIVIDE ( CALCULATE ( [Valor Sementes], FATO_ITENS_PEDIDO[EMBALAGEM] = "Saca 200 mil" ), [Sacas (pedidos em saca)] )
```

**Valor Total (todas embalagens)**
```dax
CALCULATE ( [Valor Total], REMOVEFILTERS ( FATO_ITENS_PEDIDO[EMBALAGEM] ) )
```

**Nº Clientes (todas embalagens)**
```dax
CALCULATE ( [Nº Clientes], REMOVEFILTERS ( FATO_ITENS_PEDIDO[EMBALAGEM] ) )
```

**Entregue na Embalagem**
```dax
VAR _e = [Embalagem Selecionada] RETURN CALCULATE ( SUM ( FATO_ITENS_PEDIDO[QTD_FATURADA] ), FATO_ITENS_PEDIDO[EMBALAGEM] = _e, KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] <> "CANCELADO" ) )
```

**Saldo a Carregar na Embalagem**
```dax
VAR _e = [Embalagem Selecionada] RETURN CALCULATE ( SUMX ( FATO_ITENS_PEDIDO, MAX ( 0, FATO_ITENS_PEDIDO[QTD_A_FATURAR] ) ), FATO_ITENS_PEDIDO[EMBALAGEM] = _e, KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] = "ABERTO" ) )
```

### Pasta: 7. Matriz por cliente

**Qtd Bag**
```dax
CALCULATE ( SUM ( FATO_ITENS_PEDIDO[QTD_EFETIVA] ), KEEPFILTERS ( FATO_ITENS_PEDIDO[EMBALAGEM] = "Bag" ), KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] <> "CANCELADO" ) )
```

**Qtd Saca**
```dax
CALCULATE ( SUM ( FATO_ITENS_PEDIDO[QTD_EFETIVA] ), KEEPFILTERS ( FATO_ITENS_PEDIDO[EMBALAGEM] = "Saca 200 mil" ), KEEPFILTERS ( FATO_ITENS_PEDIDO[STATUS_PEDIDO] <> "CANCELADO" ) )
```

**Qtd Bag Com TSI**
```dax
CALCULATE ( [Qtd Bag], KEEPFILTERS ( FATO_ITENS_PEDIDO[TEM_TSI] = "COM TSI" ) )
```

**Qtd Bag Sem TSI**
```dax
CALCULATE ( [Qtd Bag], KEEPFILTERS ( FATO_ITENS_PEDIDO[TEM_TSI] = "SEM TSI" ) )
```

**Qtd Saca Com TSI**
```dax
CALCULATE ( [Qtd Saca], KEEPFILTERS ( FATO_ITENS_PEDIDO[TEM_TSI] = "COM TSI" ) )
```

**Qtd Saca Sem TSI**
```dax
CALCULATE ( [Qtd Saca], KEEPFILTERS ( FATO_ITENS_PEDIDO[TEM_TSI] = "SEM TSI" ) )
```

**Matriz Bag**
```dax
IF ( ISFILTERED ( FATO_ITENS_PEDIDO[RECEITA_TSI] ), [Qtd Bag], CALCULATE ( [Qtd Bag], FATO_ITENS_PEDIDO[RECEITA_TSI] = "SEM TSI" ) )
```

**Matriz Saca**
```dax
IF ( ISFILTERED ( FATO_ITENS_PEDIDO[RECEITA_TSI] ), [Qtd Saca], CALCULATE ( [Qtd Saca], FATO_ITENS_PEDIDO[RECEITA_TSI] = "SEM TSI" ) )
```

**Matriz Total (bags)**
```dax
IF ( ISFILTERED ( FATO_ITENS_PEDIDO[RECEITA_TSI] ), [Total em Bags], CALCULATE ( [Total em Bags], FATO_ITENS_PEDIDO[RECEITA_TSI] = "SEM TSI" ) )
```

**Título Matriz**
```dax
"Receita: " & IF ( ISFILTERED ( FATO_ITENS_PEDIDO[RECEITA_TSI] ), IF ( HASONEVALUE ( FATO_ITENS_PEDIDO[RECEITA_TSI] ), VALUES ( FATO_ITENS_PEDIDO[RECEITA_TSI] ), "várias selecionadas" ), "SEM TSI" ) & "  ·  para ver outra receita, clique nela na pizza ou escolha no filtro"
```
