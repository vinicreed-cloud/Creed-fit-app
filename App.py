import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="MyFitnessPy", layout="wide")

# Inicialização de "Banco de Dados" simples (em memória)
if 'alimentos' not in st.session_state:
    st.session_state.alimentos = pd.DataFrame(
        [{"nome": "Arroz Integral", "calorias_100g": 110},
         {"nome": "Peito de Frango", "calorias_100g": 165}],
        columns=["nome", "calorias_100g"]
    )

if 'receitas' not in st.session_state:
    st.session_state.receitas = {}

# --- INTERFACE ---
st.title("🍎 MyFitnessPy - Contador e Receitas")

aba1, aba2, aba3 = st.tabs(["Diário", "Cadastrar Alimento", "Criar Receita"])

# --- ABA 1: DIÁRIO (Visualização) ---
with aba1:
    st.header("Seu Consumo")
    if not st.session_state.alimentos.empty:
        st.table(st.session_state.alimentos)
    else:
        st.write("Nenhum alimento cadastrado.")

# --- ABA 2: CADASTRO DE ALIMENTOS ---
with aba2:
    st.header("Novo Alimento")
    with st.form("form_alimento"):
        nome = st.text_input("Nome do Alimento")
        cals = st.number_input("Calorias por 100g", min_value=0)
        enviar = st.form_submit_button("Salvar Alimento")
        
        if enviar and nome:
            novo_item = pd.DataFrame([{"nome": nome, "calorias_100g": cals}])
            st.session_state.alimentos = pd.concat([st.session_state.alimentos, novo_item], ignore_index=True)
            st.success(f"{nome} adicionado!")

# --- ABA 3: CRIAR RECEITA (Sua funcionalidade extra) ---
with aba3:
    st.header("Gerador de Receitas")
    nome_receita = st.text_input("Nome da Receita (ex: Shake de Proteína)")
    
    # Seleção múltipla de alimentos já cadastrados
    ingredientes = st.multiselect("Selecione os ingredientes", st.session_state.alimentos["nome"].tolist())
    
    total_receita = 0
    if ingredientes:
        st.write("### Ajuste as quantidades (gramas)")
        for ing in ingredientes:
            # Busca a caloria/100g do alimento selecionado
            cal_base = st.session_state.alimentos.loc[st.session_state.alimentos["nome"] == ing, "calorias_100g"].values[0]
            peso = st.number_input(f"Gramas de {ing}", min_value=0, key=f"peso_{ing}")
            
            cal_calculada = (peso / 100) * cal_base
            total_receita += cal_calculada
            st.caption(f"Subtotal {ing}: {cal_calculada:.2f} kcal")

        st.divider()
        st.metric("Calorias Totais da Receita", f"{total_receita:.2f} kcal")
        
        if st.button("Salvar Receita"):
            st.session_state.receitas[nome_receita] = total_receita
            st.balloons()
            st.success(f"Receita '{nome_receita}' salva com sucesso!")
            
