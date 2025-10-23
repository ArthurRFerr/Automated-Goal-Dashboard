import streamlit as st
import pandas as pd
import locale
from babel.numbers import format_currency
from datetime import datetime
from pathlib import Path
import base64
from calendar import monthrange
import gspread
from oauth2client.service_account import ServiceAccountCredentials


img_path = Path("TrioCIDG.jpg")

# 5️⃣ Função para converter em base64
def get_base64_of_image(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_base64 = get_base64_of_image(img_path)

#---------------------------------------------------
# 3️⃣ Aplica fundo no Streamlit
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        width: 100%;
        height: 100%;
        background-position: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)



#st.title(f"📊Acompanhamento de Vendas Outubro")
st.markdown(
        f"""
        <div style="text-align: center, font-size: 80px">
            <h1>📊Acompanhamento de Vendas Outubro</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

try:
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")  # Linux/Mac
except:
    locale.setlocale(locale.LC_TIME, "portuguese")

# Meses (Setembro + 3 meses à frente)
meses = pd.date_range(start="2025-09-01", periods=4, freq="MS")
meses = [mes.strftime("%B/%Y").capitalize() for mes in meses]

# Estado inicial
if "dados" not in st.session_state:
    st.session_state["dados"] = {mes: {"meta": 10000, "realizado": 0, "vendas": []} for mes in meses}
else:
    for mes in meses:
        if "vendas" not in st.session_state["dados"][mes]:
            st.session_state["dados"][mes]["vendas"] = []
        else: 
            novas_vendas = []
            for v in st.session_state["dados"][mes]["vendas"]:
                if isinstance(v, (int, float)):
                    novas_vendas.append({"valor": v, "hora": datetime.now()})
                else:
                    novas_vendas.append(v)
                st.session_state["dados"][mes]["vendas"] = novas_vendas
# ---------------- Sidebar ----------------
st.sidebar.header("⚙️ Configurações")

# Seleção de mês no sidebar
mes_atual = st.sidebar.selectbox("Selecione o mês:", meses)

# Entrada de meta no sidebar
meta = st.sidebar.number_input(
    f"Meta de {mes_atual}", 
    min_value=0, 
    value=st.session_state["dados"][mes_atual]["meta"], 
    key=f"meta_{mes_atual}"
)

# Entrada de valor realizado no sidebar
realizado = st.sidebar.number_input(
    f"Adicionar valor realizado em {mes_atual}", 
    min_value=0.0, 
    step=0.01, 
    format="%.2f",
    key=f"add_{mes_atual}"
)

# Botão de registrar no sidebar
if st.sidebar.button(f"Registrar em {mes_atual}", key=f"btn_{mes_atual}"):
    st.session_state["dados"][mes_atual]["meta"] = meta

    valor_antigo = st.session_state["dados"][mes_atual]["realizado"]
    novo_valor = valor_antigo + realizado
    st.session_state["dados"][mes_atual]["realizado"] = novo_valor
    
    # Calcula a venda (diferença)
    venda = novo_valor - valor_antigo
    if venda > 0:
        st.session_state["dados"][mes_atual]["vendas"].append(venda)

# ---------------- Painel principal ----------------

 
meta_valor = st.session_state["dados"][mes_atual]["meta"]
realizado_valor = st.session_state["dados"][mes_atual]["realizado"]

if meta_valor > 0:
    progresso = min(realizado_valor / meta_valor, 1.0)

    # Barra de progresso
    #st.progress(progresso)

    # Formatar valores em moeda
    meta_fmt = format_currency(meta_valor, "BRL", locale="pt_BR")
    realizado_fmt = format_currency(realizado_valor, "BRL", locale="pt_BR")

    #st.subheader(f"Meta: {meta_fmt} ")
    st.markdown(    
            f"""
        <div style="text-align: center; font-size: 50px; font-weight:; color: white;">
            Meta: {meta_fmt}
        </div>
        """,
        unsafe_allow_html=True
    )

    # KPI estilizado com HTML
    st.markdown(
        f"""
        <div style="text-align: center; font-size: 65px; font-weight: bold;
                    color: {'lightgreen' if progresso >= 1 else 'orange' if progresso >= 0.5 else 'red'};">
            {progresso*100:.2f}%
        </div>
        <div style="text-align: center; font-size: 70px;">
             Realizado: {realizado_fmt} 
        </div> 
        """,
        unsafe_allow_html=True
    )
   

    hoje = datetime.now()
    ano, mes = hoje.year, hoje.month
    dias_no_mes = monthrange(ano, mes)[1]
    dia_atual = hoje.day

    progresso_tempo = dia_atual / dias_no_mes
    progresso_vendas = realizado_valor / meta_valor
    faltante = max(meta_valor - realizado_valor, 0)
    progresso_faltante =  faltante / meta_valor

    #st.subheader("Comparativo:")

# KPIs lado a lado
    col1, col2, col3  = st.columns(3)
    with col1:
        st.markdown(
        f"""
        <div style="text-align: right;">
            <h2>Tempo decorrido</h2>
            <p style="font-size:50px; font-weight:; color:white;">
                {progresso_tempo*100:.1f}%
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    with col3:
        st.markdown(
        f"""
        <div style="text-align: left;">
            <h2>Valor para atingir meta</h2>
            <p style="font-size:50px; font-weight:; color:white;">
                {format_currency(faltante, "BRL", locale="pt_BR")}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
        

    # Barras de progresso
    #st.write("### Progresso")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <style = "font-size: 40px;">
        .stProgress > div > div > div > div {{
         background-color: white;
        }}
        </style>
        """, unsafe_allow_html=True)
        
    with col2:
        #st.write("Tempo do mês")
        st.markdown(f"""
        <div style ="text-align: left; font-size: 40px;">
            <h2>Tempo do mês</h2>
        </div>
        """, unsafe_allow_html=True)
        st.progress(progresso_tempo)
        #st.write("Vendas realizadas")
        st.markdown(f"""
        <div style ="text-align: left; font-size: 40px;">
            <h2>Vendas Realizadas</h2>
        </div>
        """, unsafe_allow_html=True)
        st.progress(progresso_vendas)
else:
    st.warning("Defina uma meta para começar 🚀")