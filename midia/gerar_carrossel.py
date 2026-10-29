# Gera midia/carrossel_linkedin.pdf (1080x1350) a partir das imagens da pasta imagens/
import sys
from PIL import Image, ImageDraw, ImageFont
fd=sys.argv[1]; W,H=1080,1350
B=lambda s:ImageFont.truetype(fd+"/Carlito-Bold.ttf",s); R=lambda s:ImageFont.truetype(fd+"/Carlito-Regular.ttf",s)
PET,DARK,CORAL,BG,TXT,LINE="#1F6F8B","#16425B","#EF7D62","#F5F8FA","#5B6B78","#D2DFE6"
logo=Image.open("Pedidos_Sementes.Report/StaticResources/RegisteredResources/logo_lumina_sementes.png")
def wrap(d,text,font,maxw):
    out=[];line=""
    for w in text.split():
        t=(line+" "+w).strip()
        if d.textlength(t,font=font)<=maxw: line=t
        else: out.append(line); line=w
    out.append(line); return out
slides=[("Visão Geral","Valor total, fechado × aberto e preço médio por bag. Ranking de cultivares, obtentores, biotecnologias, receitas de TSI e vendedores. Um clique filtra o painel inteiro.","01_visao_geral.png"),
("Detalhe por Cultivar","Clique direito → Detalhar: KPIs da cultivar, embalagens dos pedidos convertidas para bag, vendedores e clientes com e sem TSI.","02_detalhe_cultivar.png"),
("Detalhe por Obtentor","A mesma lógica para cada obtentor: cultivares, tecnologia × TSI, receitas de tratamento e ranking de clientes.","03_detalhe_obtentor.png"),
("Vendedor × Embalagem","Quantidades na embalagem original do pedido (bag ou saca de 200 mil): entregue, saldo a carregar e preço por embalagem.","04_detalhe_vendedor_embalagem.png"),
("Cultivar × TSI × Embalagem","Matriz por cliente pedida pelo comercial: cultivar por receita de tratamento, em bag, saca e total convertido.","05_cultivar_tsi_embalagem.png")]
T=len(slides)+3
def base(n):
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,14],fill=PET); d.rectangle([0,14,W*n//T,22],fill=CORAL)
    d.text((60,H-70),"César Barth · Análise de Dados",font=R(30),fill=TXT)
    d.text((W-60,H-70),f"{n}/{T}",font=B(30),fill=PET,anchor="ra"); return im,d
pages=[]
im,d=base(1); lg=logo.resize((640,int(640*logo.height/logo.width))); im.paste(lg,(60,140),lg); y=400
for l in wrap(d,"Painel de Pedidos de Sementes",B(92),960): d.text((60,y),l,font=B(92),fill=DARK); y+=100
y+=20
for l in wrap(d,"Do relatório estático a um painel interativo em Power BI, com drill-through, regras de negócio validadas com o ERP e conversão de embalagens.",R(42),940): d.text((60,y),l,font=R(42),fill=TXT); y+=54
d.rounded_rectangle([60,y+40,560,y+110],radius=35,fill=CORAL); d.text((310,y+75),"Arraste para o lado →",font=B(36),fill="white",anchor="mm")
d.text((60,H-140),"Dados 100% fictícios · empresa, clientes e valores inventados",font=R(28),fill=TXT); pages.append(im)
for k,(tit,txt,f) in enumerate(slides,2):
    im,d=base(k); d.text((60,80),tit,font=B(68),fill=DARK); y=175
    for l in wrap(d,txt,R(38),960): d.text((60,y),l,font=R(38),fill=TXT); y+=50
    sc=Image.open("imagens/"+f).convert("RGB"); sw=W-60; sh=int(sc.height*sw/sc.width); sc=sc.resize((sw,sh),Image.LANCZOS)
    top=max(y+40,(H-sh)//2+80); d.rounded_rectangle([24,top-6,W-24,top+sh+6],radius=14,fill="white",outline=LINE,width=3)
    im.paste(sc,(30,top)); pages.append(im)
# roadmap
im,d=base(T-1); d.text((60,80),"Parte 1 de uma série",font=B(68),fill=DARK); y=175
for l in wrap(d,"Este painel é o primeiro módulo de um BI gerencial integrado: as áreas da empresa num mesmo modelo de dados, com dimensões compartilhadas.",R(38),960): d.text((60,y),l,font=R(38),fill=TXT); y+=50
etapas=[("Comercial · pedidos de sementes","pronto"),("Contratos de grãos","em validação"),("Lavoura · plantio e colheita","em validação"),("Beneficiamento e estoque","próximo"),("Financeiro","próximo"),("DRE gerencial","próximo")]
y+=50; x=110
d.line([(x,y+30),(x,y+30+(len(etapas)-1)*130)],fill=LINE,width=8)
for i,(n,st) in enumerate(etapas):
    yy=y+i*130; cor=CORAL if st=="pronto" else (PET if st=="em validação" else "#AAB7C0")
    d.ellipse([x-26,yy+4,x+26,yy+56],fill=cor,outline="white",width=5)
    d.text((x+60,yy),n,font=B(44),fill=DARK if st!="próximo" else TXT)
    d.text((x+60,yy+52),st,font=R(32),fill=cor)
pages.append(im)
im,d=base(T); d.text((60,140),"Por trás do painel",font=B(72),fill=DARK); y=270
for b in ["Power BI em PBIP/TMDL, versionado no Git","DAX: formato dinâmico, títulos dinâmicos, total em SVG","Power Query + SQL (Firebird) no projeto real","Conversão de embalagens para bag por cultura","Regras validadas número a número com o ERP","Python para gerar esta base fictícia"]:
    ls=wrap(d,b,R(42),880); d.ellipse([60,y+12,84,y+36],fill=CORAL)
    for i,l in enumerate(ls): d.text((110,y+i*52),l,font=R(42),fill=TXT)
    y+=52*len(ls)+34
d.rounded_rectangle([60,y+40,W-60,y+230],radius=24,fill=PET)
d.text((W//2,y+100),"Código completo no GitHub",font=B(48),fill="white",anchor="mm")
d.text((W//2,y+170),"link no primeiro comentário",font=R(38),fill="#DDEBF1",anchor="mm"); pages.append(im)
pages[0].save("midia/carrossel_linkedin.pdf",save_all=True,append_images=pages[1:],resolution=150)
print(len(pages),"páginas")
