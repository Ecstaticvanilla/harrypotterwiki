import pandas as pd
import networkx as nx
import plotly.graph_objects as go

def plot_knowledge_graph(top_n=20):
    # Read the data
    df_characters = pd.read_csv('data/graphingcharacters.csv')  
    df_relationships = pd.read_csv('data/graphingrelationships.csv')

    # Character names and houses
    df_characters = df_characters[['Name', 'House']]
    character_houses = pd.Series(df_characters.House.values, index=df_characters.Name).to_dict()

    # House colors
    house_colors = {
        'Gryffindor': 'red',
        'Slytherin': 'green',
        'Hufflepuff': 'yellow',
        'Ravenclaw': 'blue',
    }

    # Create graph and add edges
    edges = df_relationships.to_dict('records')
    G = nx.Graph()

    nodes = df_characters['Name'].tolist()
    G.add_nodes_from(nodes)

    for edge in edges:
        G.add_edge(edge['Source'], edge['Target'], relationship=edge['RelationshipType'])

    # Select the top_n characters by degree (number of connections)
    sorted_nodes = sorted(G.degree(), key=lambda x: x[1], reverse=True)
    top_nodes = [node for node, degree in sorted_nodes[:top_n]]

    # Create a subgraph for the top_n nodes
    G_sub = G.subgraph(top_nodes)

    # Compute the positions for the subgraph nodes
    pos = nx.spring_layout(G_sub)  # This will generate positions for the subgraph
    for node in G_sub.nodes():
        G_sub.nodes[node]['pos'] = pos[node]

    # Assign colors based on houses
    node_colors = [house_colors.get(character_houses.get(node, 'Unknown'), 'grey') for node in G_sub.nodes()]

    # Prepare edge and node data for the plot
    edge_x, edge_y, edge_text = [], [], []
    for edge in G_sub.edges():
        x0, y0 = G_sub.nodes[edge[0]]['pos']
        x1, y1 = G_sub.nodes[edge[1]]['pos']
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_text.append(G_sub[edge[0]][edge[1]]['relationship'])

    node_x, node_y = [], []
    for node in G_sub.nodes():
        x, y = G_sub.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    # Create the plot
    fig = go.Figure()

    # Add edges to the plot
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, line=dict(width=1, color='#888'),
                             hoverinfo='text', mode='lines', text=edge_text))

    # Add nodes to the plot
    fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text', hoverinfo='text',
                             marker=dict(color=node_colors, size=10, line=dict(width=2, color='black')),
                             text=list(G_sub.nodes())))

    # Update plot layout
    fig.update_layout(
        title=f"Top {top_n} Harry Potter Character Relationships",
        title_font=dict(size=24, family="Arial", color="black"),
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
    )

    return fig
