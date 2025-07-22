
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulador 2º F", layout="wide")

st.title("📊 Simulador de Produtos – Recuperação 2º F")
st.subheader("Explore os dados, filtre por critérios e baixe para usar no Excel")

# Carregar os dados
@st.cache_data
def carregar_dados():
    return pd.read_csv("simulador_2F_streamlit.csv")

df = carregar_dados()

# Filtros
with st.sidebar:
    st.header("🎯 Filtros Interativos")
    categoria = st.multiselect("📦 Categoria do Produto", options=sorted(df["Categoria"].unique()), default=sorted(df["Categoria"].unique()))
    regiao = st.multiselect("🌎 Região", options=sorted(df["Região"].unique()), default=sorted(df["Região"].unique()))
    preco_min, preco_max = st.slider("💰 Faixa de Preço (R$)", float(df["Preço (R$)"].min()), float(df["Preço (R$)"].max()), (float(df["Preço (R$)"].min()), float(df["Preço (R$)"].max())))

# Aplicar filtros
df_filtrado = df[
    (df["Categoria"].isin(categoria)) &
    (df["Região"].isin(regiao)) &
    (df["Preço (R$)"] >= preco_min) &
    (df["Preço (R$)"] <= preco_max)
]

st.markdown("### 📋 Resultados Filtrados")
st.dataframe(df_filtrado, use_container_width=True)

# Botão de download
csv = df_filtrado.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Baixar dados filtrados como CSV",
    data=csv,
    file_name="dados_filtrados_simulador_2F.csv",
    mime="text/csv"
)

# Instruções
st.markdown("---")
st.markdown("### 🧭 Instruções para o Aluno")
st.markdown("""
1. Use os filtros para montar um conjunto de dados com base nos critérios que quiser.
2. Baixe o arquivo CSV e abra no Excel.
3. Reproduza:
   - Frequência Absoluta (FA) por categoria ou região
   - Frequência Relativa (FR)
   - Frequência Percentual (FP)
   - Moda da categoria
   - Mediana dos preços
4. Salve seu arquivo com nome completo e RA.
""")

# Seção de senha para liberar conferência
st.markdown("---")
st.markdown("### 🔐 Área do Professor")
senha = st.text_input("Digite a senha para liberar o botão de conferência:", type="password")

if senha == "professor2F":
    st.success("Acesso liberado. Clique para calcular os dados de conferência abaixo.")

    if st.button("📊 Mostrar Frequências e Medidas"):
        st.markdown("### ✅ Frequência por Categoria")
        freq_categoria = df_filtrado["Categoria"].value_counts().reset_index()
        freq_categoria.columns = ["Categoria", "Frequência Absoluta"]
        st.dataframe(freq_categoria)

        st.markdown("### ✅ Moda da Categoria")
        moda = df_filtrado["Categoria"].mode()
        st.write("Moda:", ", ".join(moda))

        st.markdown("### ✅ Mediana dos Preços")
        st.write("Mediana (R$):", round(df_filtrado["Preço (R$)"].median(), 2))

        st.markdown("### ✅ Frequência Percentual por Região")
        freq_regiao = df_filtrado["Região"].value_counts(normalize=True).mul(100).round(2).reset_index()
        freq_regiao.columns = ["Região", "Frequência Percentual (%)"]
        st.dataframe(freq_regiao)

else:
    st.info("Digite a senha correta para liberar os cálculos de conferência.")
