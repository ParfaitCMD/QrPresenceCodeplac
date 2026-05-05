import streamlit as st
from supabase import create_client
import os
import re

# --- CONFIGURAÇÕES DE SEGURANÇA ---
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

if URL and KEY:
    supabase = create_client(URL, KEY)
else:
    st.error("Erro: Chaves de API não configuradas.")


# --- FUNÇÃO DE MÁSCARA ---
def formatar_cpf(cpf_bruto):
    numeros = re.sub(r"\D", "", cpf_bruto)
    if len(numeros) != 11:
        return None
    return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"


CURSOS = [
    "Análise e Desenvolvimento de Sistemas",
    "Ciência da Computação",
    "Engenharia de Software",
    "Gestão de Tecnologia da Informação",
]
SEMESTRES = [f"{i}º Semestre" for i in range(1, 9)]

# --- INTERFACE ---
st.set_page_config(page_title="Check-in Codeplac", page_icon="💻", layout="centered")

# --- ESTILIZAÇÃO CODEPLAC ---
st.markdown(
    f"""
    <style>
    /* Fundo Principal */
    .stApp {{
        background-color: #000b17;
    }}

    /* Esconder menus */
    #MainMenu, footer, header {{visibility: hidden;}}

    /* Estilização do Card (Formulário) */
    [data-testid="stForm"] {{
        background: rgba(13, 25, 33, 0.4);
        backdrop-filter: blur(15px);
        border: 2px solid #00EAFF;
        border-radius: 25px;
        padding: 30px;
        box-shadow: 0 0 40px rgba(0, 0, 0, 0.5);
    }}

    /* Títulos e Textos */
    h1, h2, h3, p, label, .stMarkdown {{
        color: #fff !important;
        font-family: 'Inter', sans-serif;
    }}

    label p {{
        color: #00d4ff !important;
        font-weight: bold !important;
        letter-spacing: 1px;
    }}

    /* Inputs e Selects */
    input, .stSelectbox div[data-baseweb="select"] {{
        background-color: rgba(0, 20, 30, 0.6) !important;
        border: 1px solid #1a4a5a !important;
        color: white !important;
        border-radius: 10px !important;
    }}

    /* Botão de Registro */
    button[kind="primaryFormSubmit"] {{
        background: #00d4ff !important;
        color: #000 !important;
        border-radius: 50px !important;
        padding: 10px 40px !important;
        font-weight: bold !important;
        width: 100%;
        border: none !important;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.4) !important;
        transition: 0.3s !important;
    }}

    button[kind="primaryFormSubmit"]:hover {{
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(0, 212, 255, 0.6) !important;
    }}

    /* Underline decorativo */
    .title-underline {{
        height: 2px;
        background: linear-gradient(90deg, transparent, #00d4ff, transparent);
        margin-bottom: 20px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Conteúdo Visual
st.markdown(
    "<h1 style='text-align: center; letter-spacing: 2px;'>REGISTRO DE PRESENÇA</h1>",
    unsafe_allow_html=True,
)
st.markdown("<div class='title-underline'></div>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: #00d4ff;'>Área de Tecnologia - Uniceplac</p>",
    unsafe_allow_html=True,
)

with st.form("form_registro", clear_on_submit=True):
    nome = st.text_input("NOME COMPLETO")
    cpf_input = st.text_input("CPF (APENAS NÚMEROS)", max_chars=11)

    col1, col2 = st.columns(2)
    with col1:
        curso = st.selectbox("CURSO", CURSOS)
        periodo = st.selectbox("PERÍODO", ["Matutino", "Noturno"])
    with col2:
        semestre = st.selectbox("SEMESTRE", SEMESTRES)
        turma = st.text_input("TURMA")

    botao = st.form_submit_button("REGISTRAR PRESENÇA")

    if botao:
        cpf_limpo = formatar_cpf(cpf_input)

        if not nome or not cpf_input:
            st.warning("Preencha todos os campos!")
        elif not cpf_limpo:
            st.error("CPF Inválido!")
        else:
            try:
                dados = {
                    "nome_completo": nome.strip().upper(),
                    "cpf": cpf_limpo,
                    "curso": curso,
                    "semestre": semestre,
                    "turma": turma.strip().upper(),
                    "periodo": periodo,
                }
                supabase.table("presencas").insert(dados).execute()
                st.success(f"Sucesso! Presença confirmada para {nome.split()[0]}.")
                st.balloons()
            except Exception as e:
                if "unique_cpf_dia_tech" in str(e) or "23505" in str(e):
                    st.error("⚠️ CPF já registrado hoje!")
                else:
                    st.error(f"Erro no sistema: {e}")
