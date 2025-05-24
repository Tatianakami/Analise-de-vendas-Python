import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Vendas", page_icon="📊", layout="wide")

st.title("📊 Dashboard de Vendas")

# Upload de arquivo CSV
st.sidebar.header("Configurações")
arquivo = st.sidebar.file_uploader("Escolha o arquivo CSV", type="csv")

if arquivo is not None:
    df = pd.read_csv(arquivo)
else:
    st.caption("📂 Dados carregados do arquivo padrão 'vendas.csv'.")

    try:
        df = pd.read_csv("vendas.csv")
    except FileNotFoundError:
        st.error("❌ Arquivo 'vendas.csv' não encontrado. Faça o upload na barra lateral.")
        st.stop()

# Verificar se há dados
if df.empty:
    st.warning("⚠️ O arquivo CSV está vazio.")
    st.stop()

# Mostrar os dados
st.subheader("📄 Dados de Vendas")
st.dataframe(df)

# Calcular Faturamento
df["Faturamento"] = df["Quantidade Vendida"] * df["Preco Unitario"]

# Filtro por loja
lojas = df["Loja"].unique()
loja_selecionada = st.sidebar.selectbox("Filtrar por loja", options=["Todas"] + list(lojas))

if loja_selecionada != "Todas":
    df_filtrado = df[df["Loja"] == loja_selecionada]
else:
    df_filtrado = df

# Agrupar dados
tabela_lojas = df_filtrado.groupby("Loja").sum(numeric_only=True)[["Faturamento"]].sort_values("Faturamento", ascending=False).reset_index()

# Gráfico
fig = px.bar(
    tabela_lojas,
    x="Loja",
    y="Faturamento",
    title="Faturamento por Loja",
    labels={"Faturamento": "Faturamento (R$)", "Loja": "Lojas"},
    color="Loja",
    color_discrete_sequence=px.colors.qualitative.Safe
)

fig.update_layout(
    xaxis_title="Lojas",
    yaxis_title="Faturamento (R$)",
    showlegend=False,
    template="plotly_white"
)

st.subheader("📈 Gráfico de Faturamento por Loja")
st.plotly_chart(fig, use_container_width=True)

st.sidebar.success("Análise gerada com sucesso!")


