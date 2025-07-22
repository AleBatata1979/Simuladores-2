import streamlit as st
import pandas as pd

# Título
st.title("Simulador de Produtos – Recuperação 2º F")
st.subheader("Explore os dados e exporte para reproduzir os cálculos no Excel")

# Carregar os dados do CSV
@st.cache_data
def carregar_dados():
    return pd.read_csv("simulador_2F_streamlit.csv")

df = carregar_dados()

# Filtros interativos
with st.sidebar:
    st.header("🔍 Filtros")
    categoria = st.multiselect("Categoria do Produto", options=sorted(df["Categoria"].unique()), default=sorted(df["Categoria"].unique()))
    regiao = st.multiselect("Região", options=sorted(df["Região"].unique()), default=sorted(df["Região"].unique()))
    preco_min, preco_max = st.slider("Faixa de Preço (R$)", float(df["Preço (R$)"].min()), float(df["Preço (R$)"].max()), (float(df["Preço (R$)"].min()), float(df["Preço (R$)"].max())))

# Aplicar filtros
df_filtrado = df[
    (df["Categoria"].isin(categoria)) &
    (df["Região"].isin(regiao)) &
    (df["Preço (R$)"] >= preco_min) &
    (df["Preço (R$)"] <= preco_max)
]

# Mostrar dados filtrados
st.markdown("### 📋 Dados Filtrados")
st.dataframe(df_filtrado, use_container_width=True)

# Baixar CSV filtrado
csv = df_filtrado.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Baixar dados filtrados como CSV",
    data=csv,
    file_name="dados_filtrados_simulador_2F.csv",
    mime="text/csv"
)

# Orientações ao aluno
st.markdown("---")
st.markdown("### 📝 Instruções para o Aluno")
st.markdown("""
1. Use os filtros para escolher um subconjunto de dados (por categoria, região ou faixa de preço).
2. Clique no botão para baixar o CSV.
3. No Excel, reproduza os seguintes cálculos:
   - Tabela de Frequência Absoluta (FA) por Categoria ou Região
   - Frequência Relativa (FR)
   - Frequência Percentual (FP)
   - Moda (produto ou categoria mais frequente)
   - Mediana dos preços (se aplicável)
4. Salve seu arquivo com seu nome e RA.
""")

# Rodapé
st.markdown("---")
st.caption("Simulador desenvolvido para a disciplina de Matemática Aplicada à Administração – 2º F")