"""GitHub Classroom autograding script."""

import os

import pandas as pd

import country_collaboration

country_collaboration.main(20)

#
# Retorna error si la carpeta output/ no existe
if not os.path.exists("countries.csv"):
    raise FileNotFoundError("File 'countries.csv' not found")

#
# Lee el contenido del archivo output.txt
dataframe = pd.read_csv("countries.csv")
dataframe = dataframe.set_index("countries")

assert dataframe["count"]["United States"] == 579
assert dataframe["count"]["China"] == 273
assert dataframe["count"]["India"] == 174
assert dataframe["count"]["United Kingdom"] == 173
assert dataframe["count"]["Italy"] == 112

#
#
if not os.path.exists("co_occurrences.csv"):
    raise FileNotFoundError("File 'co_occurrences.csv' not found")


if not os.path.exists("network.png"):
    raise FileNotFoundError("File 'network.pmg' not found")
