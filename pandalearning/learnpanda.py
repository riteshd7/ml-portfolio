import pandas as pd 
print(pd.__version__)

df = pd.read_csv("pandalearning/pokemondata.csv",index_col="Name")

""" print(df.to_string())

print(df["Name"].to_string())
print(df["Height"].to_string()) """

""" print(df[["Name","Height"]].to_string()) 
"""
 
""" print(df.loc["Charizard":"Blastoise",["Height","Weight"]])  """
""" print(df.iloc[0:56:4,0:3]) """


""" 
pokemon = input("Entera pokemon name: ")
try:
    print(df.loc[pokemon])
except KeyError:
    print(f"{pokemon} not found") """

#Filtering = keeping rows that match a condition 

tall_pokemon = df[df["Height"] >= 2]
heavy_pokemon = df[df["Weight"] >= 100]
legendary_pokemon = df[df["Legendary"] == True]
print(legendary_pokemon)

print(df.mean(numeric_only = True))
print(df.sum(numeric_only = True))