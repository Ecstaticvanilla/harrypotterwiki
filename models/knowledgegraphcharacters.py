import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

house_themes = {
    "Gryffindor": {"primaryColor": "#FCD116", "backgroundColor": "#FFF5E1", "textColor": "#D62828"},
    "Ravenclaw":  {"primaryColor": "#F4A261", "backgroundColor": "#E0E7FF", "textColor": "#264653"},
    "Hufflepuff": {"primaryColor": "#F4D35E", "backgroundColor": "#FAF9F6", "textColor": "#1C1C1C"},
    "Slytherin":  {"primaryColor": "#E9C46A", "backgroundColor": "#E9F5EC", "textColor": "#2A9D8F"}
}

def _draw_graph(G, pos, theme, title):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_facecolor(theme["backgroundColor"])
    ax.axis("off")

    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=600, node_color=theme["primaryColor"], edgecolors="white", linewidths=1.5)
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#555", width=1.5)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, font_color=theme["textColor"], font_family="sans-serif")

    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, font_color=theme["textColor"], label_pos=0.5)

    ax.set_title(title, fontsize=14, fontweight="bold", color=theme["textColor"], pad=10)
    return fig

def plot_character_graph(top_n=20, house="Gryffindor"):
    theme = house_themes.get(house, house_themes["Gryffindor"])
    relationships = pd.read_csv('data/graphingrelationships.csv').head(top_n)

    G = nx.DiGraph()
    for _, row in relationships.iterrows():
        G.add_edge(row['Source'], row['Target'], label=row['RelationshipType'])

    k_value = 1 + top_n * 0.02
    pos = nx.spring_layout(G, k=k_value, seed=42)
    return _draw_graph(G, pos, theme, f"{house} Knowledge Graph – Top {top_n} Relationships")

def plot_loyalty_graph(house="Gryffindor"):
    theme = house_themes.get(house, house_themes["Gryffindor"])
    relationships = pd.read_csv('data/loyalty.csv')

    G = nx.DiGraph()
    for _, row in relationships.iterrows():
        G.add_edge(row['Source'], row['Target'], label=row['Loyalty'])

    k_value = 1 + len(relationships) * 0.02
    pos = nx.spring_layout(G, k=k_value, seed=42)
    return _draw_graph(G, pos, theme, f"{house} Loyalty Knowledge Graph")

def plot_character_relationships(character, house="Gryffindor"):
    theme = house_themes.get(house, house_themes["Gryffindor"])
    relationships = pd.read_csv('data/graphingrelationships.csv')
    filtered = relationships[(relationships['Source'] == character) | (relationships['Target'] == character)]

    if filtered.empty:
        st.warning(f"No relationships found for {character}")
        return None

    G = nx.DiGraph()
    for _, row in filtered.iterrows():
        G.add_edge(row['Source'], row['Target'], label=row['RelationshipType'])

    pos = nx.spring_layout(G, k=1, seed=42)
    return _draw_graph(G, pos, theme, f"{house} – Relationships of {character}")

def plot_character_loyalties(character, house="Gryffindor"):
    theme = house_themes.get(house, house_themes["Gryffindor"])
    loyalties = pd.read_csv('data/loyalty.csv')
    filtered = loyalties[loyalties['Source'] == character]

    if filtered.empty:
        st.warning(f"No loyalty affiliations found for {character}")
        return None

    G = nx.DiGraph()
    for _, row in filtered.iterrows():
        G.add_edge(row['Source'], row['Target'], label=row['Loyalty'])

    pos = nx.spring_layout(G, k=1, seed=42)
    return _draw_graph(G, pos, theme, f"{house} – Loyalty of {character}")


def plot_location_graph(house="Gryffindor"):
    theme = house_themes.get(house, house_themes["Gryffindor"])
    locations = pd.read_csv('data/locations.csv')  
    G = nx.DiGraph()
    for _, row in locations.iterrows():
        G.add_edge(row['Source'], row['Target'], label=row['Relationship'])  

    pos = nx.spring_layout(G, k=1, seed=42)
    title = f"Wizarding Worlds  Location Map"
    return _draw_graph(G, pos, theme, title)
