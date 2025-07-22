import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Simulador 2º F", layout="wide")

st.title("📊 Simulador de Produtos – Recuperação 2º F")
st.subheader("Explore os dados, filtre por critérios e baixe para usar no Excel")

@st.cache_data
def carregar_dados():
    return pd.read_excel("simulador_2F_streamlit.xlsx")

df = carregar_dados()

with st.sidebar:
    st.header("🎯 Filtros Interativos")
    categoria = st.multiselect("📦 Categoria do Produto", options=sorted(df["Categoria"].unique()), default=sorted(df["Categoria"].unique()))
    regiao = st.multiselect("🌎 Região", options=sorted(df["Região"].unique()), default=sorted(df["Região"].unique()))
    preco_min, preco_max = st.slider("💰 Faixa de Preço (R$)", float(df["Preço (R$)"].min()), float(df["Preço (R$)"].max()), (float(df["Preço (R$)"].min()), float(df["Preço (R$)"].max())))

df_filtrado = df[
    (df["Categoria"].isin(categoria)) &
    (df["Região"].isin(regiao)) &
    (df["Preço (R$)"] >= preco_min) &
    (df["Preço (R$)"] <= preco_max)
]

st.markdown("### 📋 Resultados Filtrados")
st.dataframe(df_filtrado, use_container_width=True)

output = io.BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df_filtrado.to_excel(writer, index=False, sheet_name="DadosFiltrados")
output.seek(0)

st.download_button(
    label="📥 Baixar dados filtrados como Excel (.xlsx)",
    data=output,
    file_name="dados_filtrados_simulador_2F.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.markdown("---")
st.markdown("### 🧭 Instruções para o Aluno")
st.markdown("""
1. Use os filtros para montar seu conjunto de dados.
2. Baixe o arquivo Excel e monte as análises:
   - Frequência Absoluta (FA) por região e faixa
   - Frequência Relativa e Percentual (FR e FP)
   - Moda da categoria por faixa
   - Mediana dos preços por faixa
3. Salve seu arquivo com nome e RA.

⚠️ IMPORTANTE: As faixas de preço fixas utilizadas pelo simulador na validação automática são:
- Faixa 1: R$ 5,00 a R$ 30,00
- Faixa 2: R$ 31,00 a R$ 80,00
- Faixa 3: R$ 81,00 ou mais
""")

st.markdown("---")
st.markdown("### ✅ Área de Validação Automática")
st.info("Preencha abaixo os dados calculados por você no Excel. O simulador verificará se estão corretos.")
st.markdown("**Faixas fixas utilizadas para validação:**")
st.markdown("- Faixa 1: R$ 5 a R$ 30  
- Faixa 2: R$ 31 a R$ 80  
- Faixa 3: R$ 81 ou mais")

col1, col2, col3 = st.columns(3)
with col1:
    fa_sudeste1 = st.number_input("FA Sudeste – Faixa 1", min_value=0)
with col2:
    moda_faixa2 = st.text_input("Moda Categoria – Faixa 2").strip()
with col3:
    mediana_faixa3 = st.number_input("Mediana Preço – Faixa 3", min_value=0.0, step=0.01)

fp_total = st.number_input("Soma Total da Frequência Percentual (FP)", min_value=0.0, step=0.01)

if st.button("🔍 Validar Meus Cálculos"):
    resultado = []

    sudeste_faixa1 = df_filtrado[
        (df_filtrado["Região"] == "Sudeste") &
        (df_filtrado["Preço (R$)"] >= 5) & (df_filtrado["Preço (R$)"] <= 30)
    ]
    fa_real = len(sudeste_faixa1)

    faixa2_df = df_filtrado[(df_filtrado["Preço (R$)"] >= 31) & (df_filtrado["Preço (R$)"] <= 80)]
    moda_real = faixa2_df["Categoria"].mode().iloc[0] if not faixa2_df.empty else ""

    faixa3_df = df_filtrado[(df_filtrado["Preço (R$)"] >= 81)]
    mediana_real = round(faixa3_df["Preço (R$)"].median(), 2) if not faixa3_df.empty else 0.0

    fp_real = round(100 * len(df_filtrado) / len(df), 2) if len(df) > 0 else 0.0

    resultado.append(("FA Sudeste Faixa 1", fa_sudeste1, fa_real))
    resultado.append(("Moda Categoria Faixa 2", moda_faixa2, moda_real))
    resultado.append(("Mediana Faixa 3", mediana_faixa3, mediana_real))
    resultado.append(("Soma FP Total", fp_total, fp_real))

    st.markdown("### 🧾 Resultado da Validação")
    for item, valor_user, valor_real in resultado:
        if str(valor_user).lower().strip() == str(valor_real).lower().strip():
            st.success(f"{item} ✔️ Correto")
        else:
            st.error(f"{item} ✘ Incorreto (Você: {valor_user} | Correto: {valor_real})")

st.markdown("---")
st.markdown("### 🔐 Área do Professor")
senha = st.text_input("Digite a senha para liberar a análise oficial:", type="password")

if senha == "professor2F":
    st.success("Acesso liberado.")

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
    st.info("Digite a senha correta para liberar a área do professor.")
