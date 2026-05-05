import streamlit as st
from supabase import create_client

# --- CONFIGURAÇÕES DO SUPABASE ---
# Pegue esses dados em: Settings > API
URL = "https://nrvshjkwlfmskzgorzxq.supabase.co"
KEY = "sb_publishable_dRq1Kp9Q3WT0N34B0kmK9w_YWvx6jPi"
supabase = create_client(URL, KEY)

# --- PADRONIZAÇÃO DOS DADOS ---
CURSOS = [
    "Análise e Desenvolvimento de Sistemas",
    "Ciência da Computação",
    "Engenharia de Software",
    "Gestão de Tecnologia da Informação",
]

SEMESTRES = [f"{i}º Semestre" for i in range(1, 9)]

# --- INTERFACE ---
st.set_page_config(page_title="Check-in Tech Uniceplac", page_icon="💻")

# Como você é designer, aqui você pode colocar o link de uma imagem/logo
st.title("📝 Registro de Presença")
st.markdown("### Área de Tecnologia - Uniceplac")

with st.form("form_registro", clear_on_submit=True):
    nome = st.text_input("Nome Completo")
    cpf = st.text_input("CPF (Apenas números)")

    col1, col2 = st.columns(2)
    with col1:
        curso = st.selectbox("Curso", CURSOS)
        periodo = st.selectbox("Período", ["Matutino", "Noturno"])
    with col2:
        semestre = st.selectbox("Semestre", SEMESTRES)
        turma = st.text_input("Turma (Ex: A, B ou Única)")

    botao = st.form_submit_button("Registrar Presença")

    if botao:
        if not nome or not cpf:
            st.warning("Preencha o Nome e o CPF!")
        else:
            try:
                # Envia para a tabela 'presencas_tech'
                dados = {
                    "nome_completo": nome.strip().upper(),
                    "cpf": cpf.strip(),
                    "curso": curso,
                    "semestre": semestre,
                    "turma": turma.strip().upper(),
                    "periodo": periodo,
                }

                supabase.table("presencas").insert(dados).execute()
                st.success(f"Tudo certo, {nome.split()[0]}! Presença registrada.")
                st.balloons()
            except Exception as e:
                # Aqui o Python identifica se o CPF foi repetido no dia
                if "unique_cpf_dia_tech" in str(e):
                    st.error("Ops! Você já registrou presença hoje.")
                else:
                    st.error(f"Erro ao salvar: {e}")
