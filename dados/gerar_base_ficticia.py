"""
Gera a base FICTICIA de pedidos de sementes usada no painel de portfolio.
Todos os nomes (empresa, clientes, vendedores, cultivares, obtentores,
tecnologias, receitas) e todos os valores sao inventados.
Uso: python gerar_base_ficticia.py  -> cria pedidos_ficticios.csv nesta pasta
Autor: Cesar Barth
"""
import csv, random, datetime as dt, os, zlib
random.seed(2026)
SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pedidos_ficticios.csv")

EMPRESAS = [(101, "LUMINA SEMENTES - UNIDADE CENTRAL", "JURÍDICA", 0.62),
            (102, "LUMINA SEMENTES - UNIDADE NORTE", "JURÍDICA", 0.26),
            (103, "JOAO M. LUMINA - PRODUTOR", "FÍSICA", 0.12)]

# vendedor principal -> canais de revenda ligados a ele
VENDEDORES = {"Ana Ribeiro": ["AGRO CANAL NORTE LTDA"],
              "Bruno Kessler": [],
              "Carla Menezes": ["REVENDA CAMPO FORTE"],
              "Diego Farias": ["COMERCIAL SAFRA BOA", "INSUMOS PLANALTO"],
              "Eduarda Lopes": [],
              "Fabio Nunes": ["AGROSUL REPRESENTACOES"]}
PESO_VEND = [0.24, 0.13, 0.19, 0.21, 0.11, 0.12]

CIDADES = [("CRUZ ALTA","RS"),("IJUÍ","RS"),("SANTO ÂNGELO","RS"),("PASSO FUNDO","RS"),("CARAZINHO","RS"),
           ("PALMEIRA DAS MISSÕES","RS"),("TUPANCIRETÃ","RS"),("JÚLIO DE CASTILHOS","RS"),("SANTA BÁRBARA DO SUL","RS"),
           ("PANAMBI","RS"),("NÃO-ME-TOQUE","RS"),("ESPUMOSO","RS"),("SANTIAGO","RS"),("SÃO LUIZ GONZAGA","RS"),
           ("GIRUÁ","RS"),("TRÊS DE MAIO","RS"),("SANTA ROSA","RS"),("ERECHIM","RS"),("VACARIA","RS"),("SÃO GABRIEL","RS"),
           ("CAMPOS NOVOS","SC"),("XANXERÊ","SC"),("GUARAPUAVA","PR"),("CASCAVEL","PR"),("PONTA GROSSA","PR"),("DOURADOS","MS")]
PESO_CID = [9,7,6,6,5,5,5,4,4,4,3,3,3,3,3,3,3,2,2,2,2,1,2,2,1,1]

NOMES = "Adair Airton Alceu Aldo Arno Belmiro Celso Cleber Darci Dirceu Edson Elton Gilmar Irineu Ivo Jair Lauri Leonir Lírio Marcos Moacir Nelson Neri Osmar Paulo Renato Rogério Sadi Valdir Vilmar Lúcia Marta Neusa Rosane Sandra".split()
SOBRENOMES = "Andreolla Bervian Cassol Dalmolin Engel Fabris Gehlen Hoffmann Kunz Lorenzon Mallmann Nardi Pasqualotto Rambo Schneider Sperotto Tedesco Vettorazzi Weber Zanella Bonamigo Cerutti Durante Frizzo Grando".split()
PJ = ["AGROPECUÁRIA {s}", "FAZENDA {s} LTDA", "{s} & FILHOS AGRO", "GRANJA {s}", "COOPERATIVA AGRO {c}"]

# cultura -> lista de (cultivar, biotecnologia, detentor, obtentor)
CULTIVARES = {
 "SOJA": [("LX 5821 TMX","TOLERA MAX","BIOTEC ORION","GENÉTICA ALFA"),("LX 6140 TMX","TOLERA MAX","BIOTEC ORION","GENÉTICA ALFA"),
          ("HZ 5730 BTP","BT PRIME","BIOTEC ORION","AGROBASE"),("HZ 6355 BTP","BT PRIME","BIOTEC ORION","AGROBASE"),
          ("NV 5410 GLX","GUARDA LX","CAMPO GEN","SEMEAR GENÉTICA"),("NV 6022 GLX","GUARDA LX","CAMPO GEN","SEMEAR GENÉTICA"),
          ("TN 5915 RG","RG BASE","CAMPO GEN","TERRA NOVA"),("TN 6480 RG","RG BASE","CAMPO GEN","TERRA NOVA"),
          ("VT 5650 FLX","FLEX DUO","BIOTEC ORION","VERTENTE"),("VT 6233 FLX","FLEX DUO","BIOTEC ORION","VERTENTE"),
          ("LX 6610 TMX","TOLERA MAX","BIOTEC ORION","GENÉTICA ALFA"),("HZ 5299 CONV","Convencional","Próprio","AGROBASE")],
 "TRIGO": [("TRIGO AURA 21","Convencional","Próprio","GENÉTICA ALFA"),("TRIGO BRISA 08","Convencional","Próprio","TERRA NOVA"),
           ("TRIGO CEDRO 15","Convencional","Próprio","SEMEAR GENÉTICA")],
 "AVEIA BRANCA": [("AVEIA ALVA 33","Convencional","Próprio","SEMEAR GENÉTICA"),("AVEIA NÉVOA 12","Convencional","Próprio","TERRA NOVA")],
 "MILHO": [("MILHO MZ 410 BTP","BT PRIME","BIOTEC ORION","AGROBASE"),("MILHO MZ 525 BTP","BT PRIME","BIOTEC ORION","AGROBASE")]}
PESO_CULT_SOJA = [16,11,13,8,10,7,6,5,8,6,6,4]

RECEITAS = ["SEM TRATAMENTO","RECEITA PREMIUM","RECEITA PROTEÇÃO","RECEITA BASE","RECEITA INOCULANTE"]
PESO_REC = [52,16,13,11,8]
SAFRAS = [(9,"2023/2024",2023,0.82),(10,"2024/2025",2024,0.92),(11,"2025/2026",2025,1.0),(12,"2026/2027",2026,0.30)]
OPERACOES = [(5101,"VENDA DE SEMENTES",0.78),(5102,"VENDA ENTREGA FUTURA",0.19),(5910,"BONIFICAÇÃO",0.03)]
GRUPOS_PESSOA = ["Produtor Rural","Revenda","Cooperativa"]

# embalagens: unidade -> (id, kg por unidade)
UNID = {"5MM":(1,705.0),"SC200":(2,28.2),"BB1000":(3,1000.0),"SC40":(4,40.0),"BB 760":(5,760.0),"60M":(6,20.0)}
# preco base inventado por unidade (R$) e faixa de TSI por unidade
PRECO = {"5MM":(540,790,(70,135)),"SC200":(23.5,34,(3,6)),"BB1000":(2850,3600,(0,0)),"SC40":(120,152,(0,0)),
         "BB 760":(1450,1850,(0,0)),"60M":(560,820,(55,90))}
# mes de venda dentro da safra (jul=1 ... jun=12) por cultura
SAZON = {"SOJA":[10,18,22,17,10,5,3,3,3,3,3,3],"MILHO":[14,18,16,10,6,4,4,4,6,8,6,4],
         "TRIGO":[2,1,1,1,1,1,4,10,18,24,22,15],"AVEIA BRANCA":[2,1,1,1,1,1,6,14,24,24,16,9]}

def nova_data(ano_ini, cultura, hoje):
    while True:
        m = random.choices(range(12), SAZON[cultura])[0]
        mes, ano = (7+m, ano_ini) if m < 6 else (m-5, ano_ini+1)
        d = dt.date(ano, mes, random.randint(1,28))
        if d <= hoje: return d

def gerar():
    hoje = dt.date(2026,10,27)
    clientes = []
    for cod in range(5001, 5321):
        cid, uf = random.choices(CIDADES, PESO_CID)[0]
        if random.random() < 0.62:
            nome = f"{random.choice(NOMES)} {random.choice(SOBRENOMES)}".upper(); gp = "Produtor Rural"
        else:
            nome = random.choice(PJ).format(s=random.choice(SOBRENOMES).upper(), c=cid); gp = random.choice(GRUPOS_PESSOA)
        vend = random.choices(list(VENDEDORES), PESO_VEND)[0]
        porte = random.lognormvariate(0, 0.9)
        clientes.append(dict(cod=cod, nome=nome, cid=cid, uf=uf, gp=gp, vend=vend, porte=porte,
                             emp=random.choices(EMPRESAS, [e[3] for e in EMPRESAS])[0]))
    cods_vend = {v: 900+i for i, v in enumerate(VENDEDORES)}
    linhas, id_ped, nr_ped, id_item = [], 70000, 1000, 0
    for cod_safra, safra, ano_ini, escala in SAFRAS:
        n_ped = int(820 * escala)
        for _ in range(n_ped):
            cl = random.choices(clientes, [c["porte"] for c in clientes])[0]
            cultura = random.choices(list(CULTIVARES), [70,13,7,10])[0]
            data = nova_data(ano_ini, cultura, hoje)
            id_ped += 1; nr_ped += 1
            canal = random.choice(VENDEDORES[cl["vend"]]) if VENDEDORES[cl["vend"]] and random.random() < 0.35 else None
            op = random.choices(OPERACOES, [o[2] for o in OPERACOES])[0]
            idade = (hoje - data).days
            r = random.random()
            if safra != "2026/2027" and idade > 200: st = "FECHADO" if r < 0.94 else "CANCELADO"
            else: st = "ABERTO" if r < 0.72 else ("FECHADO" if r < 0.94 else "CANCELADO")
            itens, n_it = [], random.choices([1,2,3,4],[50,30,14,6])[0]
            for _ in range(n_it):
                id_item += 1
                cv = CULTIVARES[cultura]
                cultivar, bio, det, obt = random.choices(cv, PESO_CULT_SOJA if cultura=="SOJA" else None)[0]
                if cultura == "SOJA": un = "5MM" if random.random() < 0.68 else "SC200"
                elif cultura == "TRIGO": un = "BB1000" if random.random() < 0.8 else "SC40"
                elif cultura == "AVEIA BRANCA": un = "BB 760" if random.random() < 0.75 else "SC40"
                else: un = "60M"
                base = {"5MM":(3,40),"SC200":(25,280),"BB1000":(2,18),"SC40":(10,140),"BB 760":(2,14),"60M":(5,70)}[un]
                qtd = round(min(base[1]*3, random.uniform(*base) * (0.6+cl["porte"]*0.5)))
                qtd = max(qtd, base[0])
                pmin, pmax, (tmin, tmax) = PRECO[un]
                preco = round(random.uniform(pmin, pmax) * (1 + 0.06*(ano_ini-2023)), 2)
                if op[1] == "BONIFICAÇÃO": preco = 0.0
                rec = random.choices(RECEITAS, PESO_REC)[0] if tmax else "SEM TRATAMENTO"
                vtsi_un = round(random.uniform(tmin, tmax),2) if rec != "SEM TRATAMENTO" else 0.0
                if st == "FECHADO": fat = qtd if random.random() < 0.85 else round(qtd*random.uniform(0.6,0.95))
                elif st == "ABERTO": fat = round(qtd * min(1, max(0, (idade/120) * random.uniform(0.2,1.1))))
                else: fat = 0
                kg_un = UNID[un][1]
                itens.append(dict(cultivar=cultivar,bio=bio,det=det,obt=obt,un=un,qtd=qtd,preco=preco,rec=rec,
                                  vtsi_un=vtsi_un,fat=fat,kg=kg_un,id_item=id_item))
            total_ped = round(sum(i["qtd"]*(i["preco"]+i["vtsi_un"]) for i in itens),2)
            for i in itens:
                q, f = i["qtd"], i["fat"]
                afat = q - f
                aberto = st == "ABERTO"
                vsem = round(q*i["preco"],2); vtsi = round(q*i["vtsi_un"],2)
                linhas.append({
                 "ID_PEDIDO_INTERNO":id_ped,"N_PEDIDO":nr_ped,"STATUS_PEDIDO":st,"STATUS_ITEM":st[0],
                 "DATA_PEDIDO":data.isoformat(),"PREV_RETIRADA":(data+dt.timedelta(days=random.randint(20,90))).isoformat(),
                 "COD_EMPRESA":cl["emp"][0],"EMPRESA":cl["emp"][1],"TIPO_EMPRESA":cl["emp"][2],
                 "COD_VENDEDOR":cods_vend[cl["vend"]],"GRUPO_VENDEDOR":cl["vend"].upper(),
                 "VENDEDOR":canal or cl["vend"].upper(),"VENDEDOR_RESPONSAVEL":canal or cl["vend"].upper(),
                 "COD_CLIENTE":cl["cod"],"CLIENTE":cl["nome"],"CIDADE_CLIENTE":cl["cid"],"UF_CLIENTE":cl["uf"],
                 "LOCALIDADE_UF":f'{cl["cid"]}-{cl["uf"]}',"GRUPO_DE_PESSOA":cl["gp"],
                 "ID_PRODUTO":zlib.crc32(i["cultivar"].encode())%90000+1000,"CULTIVAR":i["cultivar"],
                 "COD_CULTURA":list(CULTIVARES).index(cultura)+1,"NOME_CULTURA":cultura,"COD_SAFRA":cod_safra,
                 "SAFRA_PEDIDO":safra,"SAFRA_ITEM":safra,"CATEGORIA":random.choices(["S1","S2","C1","C2"],[45,30,15,10])[0],
                 "PENEIRA":random.choice(["5.5","6.0","6.5","7.0"]) if cultura=="SOJA" else "ÚNICA","TRATAMENTO":i["rec"],
                 "FAIXA_PMS":random.choice(["140 - 160","160 - 180","180 - 200"]),"BIOTECNOLOGIA":i["bio"],"DETENTOR":i["det"],
                 "COD_GRUPO_CULTIVAR":10+["GENÉTICA ALFA","AGROBASE","SEMEAR GENÉTICA","TERRA NOVA","VERTENTE"].index(i["obt"]),
                 "GRUPO_CULTIVAR":i["obt"],"TIPO_DE_VENDA":"Entrega Futura" if op[0]==5102 else "Venda Padrão",
                 "COD_OPERACAO":op[0],"OPERACAO":op[1],"FRETE_POR_CONTA":random.choice(["EMITENTE","DESTINATÁRIO"]),
                 "VL_FRETE":0,"OBSERVACAO_PEDIDO":"","MOEDA":"1-R$","ID_UNIDADE":UNID[i["un"]][0],
                 "UNIDADE_ORIGINAL":i["un"],"QUANTIDADE_ORIGINAL":q,"QUANTIDADE":q,"QTD_PEDIDA_SACASPADRAO":round(q*i["kg"],4),
                 "QTD_FATURADA":f,"QTD_A_FATURAR":afat,"QTD_ENTREGUE":f,"QTD_A_ENTREGAR":afat,
                 "QTD_FATURADA_SACASPADRAO":round(f*i["kg"],4),"QTD_A_FATURAR_SACASPADRAO":round(afat*i["kg"],4) if aberto else 0,
                 "QTD_ENTREGUE_SACASPADRAO":round(f*i["kg"],4),"QTD_A_ENTREGAR_SACASPADRAO":round(afat*i["kg"],4) if aberto else 0,
                 "VALOR_UN_SEMENTE":i["preco"],"VL_TOTAL_SEM":vsem,"VL_UNIT_TSI":i["vtsi_un"],"VALOR_TSI":vtsi,
                 "VALOR_COMISSAO":round(vsem*0.03,2),"VALOR_COMISSAO_TSI":round(vtsi*0.02,2),"VALOR_FATURADO":vsem,
                 "TOTAL_PEDIDO":total_ped})
    with open(SAIDA, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(linhas[0]), delimiter=";")
        w.writeheader(); w.writerows(linhas)
    return linhas

if __name__ == "__main__":
    l = gerar(); print(len(l), "linhas ->", SAIDA)
