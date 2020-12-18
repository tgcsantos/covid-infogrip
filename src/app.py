import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

from time import sleep


@st.cache
def carrega_dados(caminho):

    sleep(10)
    obitos = pd.read_csv(caminho)

    return obitos


def grafico_comparativo(df_2019, df_2020, causa, estado="Brasil"):

    if estado == "Brasil":
        logica = f"tipo_doenca == '{causa}'"

    else:
        logica = f"tipo_doenca == '{causa}' & uf == '{estado}'"

    total_2019 = sum(df_2019.query(logica)["total"])
    total_2020 = sum(df_2020.query(logica)["total"])
    dados = pd.DataFrame({'Total': [total_2019, total_2020],
                          'Ano': [2019, 2020]})
    # TODO gerar os erros com o subplot
    # plt.figure(figsize=(8, 5))
    fig, ax = plt.subplots()
    ax = sns.barplot(x='Ano', y='Total', data=dados)
    ax.set_title(f"Óbitos por {causa} {estado}")

    # plt.title(f"Óbitos por {causa} {estado}")
    return fig


def main():

    st.title("Comparativos de óbitos 2019-2020")
    st.markdown("Este trabalho tem como objetivo comparar\
                ** óbitos 2019-2020 **")

    caminho_dados = ["dados/obitos-2019.csv", "dados/obitos-2020.csv"]
    obitos_2019 = carrega_dados(caminho_dados[0])
    obitos_2020 = carrega_dados(caminho_dados[1])

    doencas = obitos_2020["tipo_doenca"].unique()
    estados = obitos_2020["uf"].unique()

    options_1 = st.sidebar.selectbox(
        "Seleciona a doença?",
        doencas,
    )

    options_2 = st.sidebar.selectbox(
        "Selecione o Estado de Desejo",
        np.append(estados, "Brasil"),
    )

    fig = grafico_comparativo(obitos_2019, obitos_2020, options_1, options_2)
    st.pyplot(fig)

    if st.checkbox("Mostrar DataFrame?"):
        st.header("Obitos 2019")
        st.dataframe(obitos_2019)

        st.header("Óbitos 2020")
        st.dataframe(obitos_2020)


if __name__ == "__main__":

    main()
