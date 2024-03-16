"""Taller Presencial Evaluable"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def load_affiliations():
    """Carga el archivo scopus-papers.csv y retorna un dataframe con la columna 'Affiliations'"""
    dataframe = pd.read_csv(
        "https://raw.githubusercontent.com/jdvelasq/datalabs/master/datasets/scopus-papers.csv",
        sep=",",
        index_col=None,
    )[["Affiliations"]]
    return dataframe

def remove_na_rows(affiliations):
    """Elimina las filas con valores nulos en la columna 'Affiliations'"""

    affiliations = affiliations.copy()
    affiliations = affiliations.dropna(subset=["Affiliations"])

    return affiliations


def add_countries_column(affiliations):
    """Transforma la columna 'Affiliations' a una lista de paises."""

    affiliations = affiliations.copy()
    affiliations["countries"] = affiliations["Affiliations"].copy()
    affiliations["countries"] = affiliations["countries"].str.split("; ")
    affiliations["countries"] = affiliations["countries"].map(
        lambda x: [y.split(", ") for y in x]
    )
    affiliations["countries"] = affiliations["countries"].map(
        lambda x: [y[-1].strip() for y in x]
    )
    affiliations["countries"] = affiliations["countries"].map(set)
    affiliations["countries"] = affiliations["countries"].str.join(", ")

    return affiliations


def count_country_frequency(affiliations):
    """Cuenta la frecuencia de cada país en la columna 'countries'"""

    countries = affiliations["countries"].copy()
    countries = countries.str.split(", ")
    countries = countries.explode()
    countries = countries.value_counts()
    countries.to_csv("countries.csv")
    return countries

def select_most_frequent_countries(countries,n_countries):
    """Selecciona los n_countries paises mas frecuentes"""
    countries = countries.copy()
    countries = countries.head(n_countries)
    return countries

def compute_co_occurrences(affiliations,most_frequent_countries):
    """Cuenta la frecuencia de co-ocurrencia de paises"""
    affiliations = affiliations.copy()
    # Se copia la columna de paises
    co_occurrences = affiliations[["countries"]].copy()
    # Se renombra la columna a node_a
    co_occurrences = co_occurrences.rename(columns={"countries":"node_a"})
    # Se crea una nueva columna con el mismo contenido
    co_occurrences["node_b"] = co_occurrences["node_a"]

    # Se convierte la columna node_a en una lista
    co_occurrences['node_a'] = co_occurrences['node_a'].str.split(", ")
    # Se crea un registro por cada pais en node_a
    co_occurrences = co_occurrences.explode("node_a")

    # Se convierte la columna node_b en una lista
    co_occurrences['node_b'] = co_occurrences['node_b'].str.split(", ")
    # Se crea un registro por cada pais en node_b
    co_occurrences = co_occurrences.explode("node_b")

    # Se filtra el dataframe para que node_b solo contenga los paises mas frecuentes
    co_occurrences = co_occurrences[
        co_occurrences['node_b'].isin(most_frequent_countries.index)
    ]
    # Se filtra el dataframe para que node_a sea diferente de node_b (no tiene sentido contar la co-ocurrencia de un pais consigo mismo)
    co_occurrences = co_occurrences[
        co_occurrences['node_a']!=co_occurrences['node_b']
    ]

    co_occurrences = co_occurrences.groupby(["node_a","node_b"],as_index=False).size()

    co_occurrences.to_csv("co_occurrences.csv")

    return co_occurrences

def plot_country_collaboration(countries,co_occurrences):

    #Se crea un grafico usando networkx
    G = nx.Graph()

    for _,row in co_occurrences.iterrows():
        G.add_edge(row["node_a"],row["node_b"],weight=row["size"])

    pos = nx.spring_layout(G)

    countries_list = list(G)

    node_size = countries[countries_list].values

    nx.draw(
        G,
        pos,
        with_labels=False,
        node_size=node_size,
        node_color="gray",
        edge_color="lightgray",
        font_size=8,
        alpha=0.4,
    )

    for country in pos.keys():
        x,y = pos[country]
        plt.text(x,y,country,fontsize=7,ha="center",va="center")

    plt.savefig("network.png")

def main(n_countries):
    """Función principal"""

    affiliations = load_affiliations()
    affiliations = remove_na_rows(affiliations)
    affiliations = add_countries_column(affiliations)
    countries = count_country_frequency(affiliations)
    most_frequent_countries = select_most_frequent_countries(countries,n_countries)
    co_occurrences = compute_co_occurrences(affiliations,most_frequent_countries)
    plot_country_collaboration(countries,co_occurrences)
if __name__ == "__main__":
    main(n_countries=20)



