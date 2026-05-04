import streamlit as st

# --- CONFIGURAÇÕES DE PERFIL (Seus Dados) ---
PESO_ATUAL = 107.5
ALTURA = 186
IDADE = 30
META_CALORICA_BASE = 2100
META_AGUA = 3.7

st.set_page_config(page_title="HealthApp Pro", page_icon="💪", layout="centered")

# --- INICIALIZAÇÃO DO BANCO DE DADOS E MEMÓRIA ---
if 'alimentos' not in st.session_state:
    st.session_state.alimentos = {
        "Arroz Branco": 1.30,
        "Feijão Preto": 0.91,
        "Frango Grelhado": 1.65,
        "Ovo (unidade)": 78.0
    }

if 'consumo_dia' not in st.session_state: st.session_state.consumo_dia = 0.0
if 'treino_dia' not in st.session_state: st.session_state.treino_dia = 0.0
if 'agua_dia' not in st.session_state: st.session_state.agua_dia = 0.0
if 'saldo_devedor' not in st.session_state: st.session_state.saldo_devedor = 0.0

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .stProgress > div > div > div > div { background-color: #2ecc71; }
    div[data-testid="stMetricValue"] { font-size: 24px; }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO E MÉTRICAS ---
st.title("💪 Meu Assistente de Saúde")

meta_ajustada = META_CALORICA_BASE - st.session_state.saldo_devedor
saldo_final = meta_ajustada - st.session_state.consumo_dia + st.session_state.treino_dia

if st.session_state.saldo_devedor > 0:
    st.warning(f"⚠️ Compensando excesso de ontem: -{int(st.session_state.saldo_devedor)} kcal")

col1, col2, col3 = st.columns(3)
col1.metric("Meta Ajustada", f"{int(meta_ajustada)}")
col2.metric("Saldo Atual", f"{int(saldo_final)} kcal")
col3.metric("Água", f"{st.session_state.agua_dia:.1f}/{META_AGUA}L")

# Barra de progresso do consumo
progresso = min(st.session_state.consumo_dia / (meta_ajustada + 0.1), 1.0)
st.progress(progresso)

# --- NAVEGAÇÃO ---
aba_diario, aba_exercicio, aba_config = st.tabs(["🍴 Alimentação", "🏃 Exercícios", "⚙️ Cadastrar Itens"])

# --- ABA 1: ALIMENTAÇÃO ---
with aba_diario:
    st.subheader("Registrar Refeição")
    escolha = st.selectbox("Alimento:", list(st.session_state.alimentos.keys()))
    
    # Verifica se é unidade ou gramas (baseado no nome)
    label_qtd = "Quantas unidades?" if "unidade" in escolha.lower() else "Quantas gramas (g)?"
    qtd = st.number_input(label_qtd, min_value=0.0, step=10.0, value=100.0)
    
    calc_refeicao = qtd * st.session_state.alimentos[escolha]
    st.info(f"Total: **{int(calc_refeicao)} kcal**")
    
    if st.button("Lançar no Diário"):
        st.session_state.consumo_dia += calc_refeicao
        st.toast(f"Adicionado: {int(calc_refeicao)} kcal")

    st.divider()
    st.subheader("💧 Água")
    if st.button("🥤 Beber 500ml"):
        st.session_state.agua_dia += 0.5

# --- ABA 2: EXERCÍCIOS ---
with aba_exercicio:
    st.subheader("Registrar Treino")
    tipo = st.selectbox("Atividade:", ["Musculação", "Caminhada", "Corrida", "Bicicleta"])
    tempo = st.number_input("Duração (minutos):", min_value=1, value=30)
    
    # Fórmulas de MET para o seu peso de 107.5kg
    mets = {"Musculação": 5.0, "Caminhada": 4.0, "Corrida": 8.5, "Bicicleta": 6.5}
    gasto = (mets[tipo] * PESO_ATUAL * (tempo / 60))
    
    st.write(f"Estimativa de queima: **{int(gasto)} kcal**")
    if st.button("Registrar Queima"):
        st.session_state.treino_dia += gasto
        st.success("Exercício contabilizado!")

# --- ABA 3: CONFIGURAÇÃO ---
with aba_config:
    st.subheader("⚙️ Gerenciar Alimentos")
    with st.expander("Adicionar Novo Alimento"):
        nome_novo = st.text_input("Nome (ex: Macarrão Cozido)")
        cal_100g = st.number_input("Calorias em 100g (ver rótulo):", min_value=0.0)
        if st.button("Salvar"):
            st.session_state.alimentos[nome_novo] = cal_100g / 100
            st.success("Salvo!")

    st.divider()
    if st.button("🔄 FINALIZAR DIA (Virar data)"):
        # Se comeu mais do que devia (Meta + Exercício), o saldo vira dívida
        excesso = st.session_state.consumo_dia - (META_CALORICA_BASE + st.session_state.treino_dia)
        st.session_state.saldo_devedor = excesso if excesso > 0 else 0.0
        
        # Reseta os contadores diários
        st.session_state.consumo_dia = 0
        st.session_state.treino_dia = 0
        st.session_state.agua_dia = 0
        st.rerun()

    if st.button("❌ Reset Total (Zerar tudo)", type="secondary"):
        st.session_state.clear()
        st.rerun()
      
