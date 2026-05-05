import streamlit as st
from supabase import create_client
import os
import re  # Importante para a máscara do CPF

# --- CONFIGURAÇÕES DE SEGURANÇA ---
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

if URL and KEY:
    supabase = create_client(URL, KEY)
else:
    st.error("Erro: Chaves de API não configuradas no Render.")


# --- FUNÇÃO DE MÁSCARA (PADRONIZAÇÃO) ---
def formatar_cpf(cpf_bruto):
    # Remove tudo que não é número
    numeros = re.sub(r"\D", "", cpf_bruto)
    # Verifica se tem os 11 dígitos
    if len(numeros) != 11:
        return None
    # Retorna no formato 000.000.000-00
    return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"


# --- PADRONIZAÇÃO DOS CURSOS ---
CURSOS = [
    "Análise e Desenvolvimento de Sistemas",
    "Ciência da Computação",
    "Engenharia de Software",
    "Gestão de Tecnologia da Informação",
]
SEMESTRES = [f"{i}º Semestre" for i in range(1, 9)]

# --- INTERFACE ---
st.set_page_config(page_title="Check-in Tech Uniceplac", page_icon="💻")

# Esconde menus do Streamlit para segurança e estética
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📝 Registro de Presença")
st.markdown("### Área de Tecnologia - Uniceplac")

with st.form("form_registro", clear_on_submit=True):
    nome = st.text_input("Nome Completo")
    # max_chars=11 impede o aluno de digitar números a mais
    cpf_input = st.text_input(
        "CPF (Apenas os 11 números)",
        max_chars=11,
        help="Digite apenas os números do seu CPF",
    )

    col1, col2 = st.columns(2)
    with col1:
        curso = st.selectbox("Curso", CURSOS)
        periodo = st.selectbox("Período", ["Matutino", "Noturno"])
    with col2:
        semestre = st.selectbox("Semestre", SEMESTRES)
        turma = st.text_input("Turma (Ex: A, B ou Única)")

    botao = st.form_submit_button("Registrar Presença")

    if botao:
        cpf_limpo = formatar_cpf(cpf_input)

        if not nome or not cpf_input:
            st.warning("Por favor, preencha o Nome e o CPF!")
        elif not cpf_limpo:
            st.error("CPF Inválido! Digite exatamente os 11 números.")
        else:
            try:
                dados = {
                    "nome_completo": nome.strip().upper(),
                    "cpf": cpf_limpo,  # Salva como 000.000.000-00
                    "curso": curso,
                    "semestre": semestre,
                    "turma": turma.strip().upper(),
                    "periodo": periodo,
                }

                supabase.table("presencas").insert(dados).execute()
                st.success(f"Tudo certo, {nome.split()[0]}! Presença registrada.")
                st.balloons()
            except Exception as e:
                # Agora a trava unique_cpf_dia_tech vai funcionar!
                if "unique_cpf_dia_tech" in str(e) or "23505" in str(e):
                    st.error("⚠️ Você já registrou presença hoje!")
                else:
                    st.error(f"Erro ao salvar: {e}")
