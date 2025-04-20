import spacy
from neo4j import GraphDatabase
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Neo4j credentials
uri = "neo4j+s://3d12b880.databases.neo4j.io"
username = "neo4j"
password = st.secrets["password"]

# Load spaCy
nlp = spacy.load("en_core_web_sm")

# Color mapping
ENTITY_COLORS = {
    "PERSON": "skyblue",
    "ORG": "lightcoral",
    "LOC": "lightgreen",
    "GPE": "lightsalmon",
    "PRODUCT": "lightcyan",
    "EVENT": "lavender",
    "WORK_OF_ART": "lightgoldenrodyellow",
    "LAW": "thistle",
    "LANGUAGE": "palegreen",
    "DATE": "wheat",
    "TIME": "mistyrose",
    "PERCENT": "lightsteelblue",
    "MONEY": "honeydew",
    "QUANTITY": "navajowhite",
    "ORDINAL": "lightgray",
    "CARDINAL": "whitesmoke",
    "FAC": "powderblue",
}
DEFAULT_NODE_COLOR = "lightblue"

def normalize_entity(entity_text):
    return entity_text.strip()

def get_node_color(node_group):
    return ENTITY_COLORS.get(node_group.upper(), DEFAULT_NODE_COLOR)

def clear_graph():
    driver = GraphDatabase.driver(uri, auth=(username, password))

    def clear(tx):
        tx.run("MATCH (e:Entity)-[r]->() DELETE r")
        tx.run("MATCH (e:Entity) DELETE e")

    with driver.session() as session:
        session.execute_write(clear)
    driver.close()

def create_entity_node(tx, entity_text, entity_type):
    query = """
    MERGE (e:Entity {name: $name})
    ON CREATE SET e.type = $type
    RETURN id(e) AS node_id
    """
    result = tx.run(query, name=entity_text, type=entity_type.upper())
    record = result.single()
    return record["node_id"] if record else None

def create_relationship(tx, id1, relationship_type, id2):
    if id1 is not None and id2 is not None and id1 != id2:
        query = f"""
        MATCH (a), (b)
        WHERE id(a) = $id1 AND id(b) = $id2
        MERGE (a)-[:{relationship_type.upper()}]->(b)
        """
        tx.run(query, id1=id1, id2=id2)

def process_book(book_text):
    clear_graph()  
    driver = GraphDatabase.driver(uri, auth=(username, password))

    def create_graph(tx):
        doc = nlp(book_text)
        for sent in doc.sents:
            entity_nodes = {}
            for ent in sent.ents:
                ent_text = normalize_entity(ent.text)
                if ent_text not in entity_nodes:
                    node_id = create_entity_node(tx, ent_text, ent.label_)
                    if node_id:
                        entity_nodes[ent_text] = node_id
            entity_ids = list(entity_nodes.values())
            for i in range(len(entity_ids)):
                for j in range(i + 1, len(entity_ids)):
                    create_relationship(tx, entity_ids[i], "MENTIONED_WITH", entity_ids[j])

    with driver.session() as session:
        session.execute_write(create_graph)

    driver.close()
    st.success("✅ Knowledge graph creation complete!")

def fetch_graph_data():
    driver = GraphDatabase.driver(uri, auth=(username, password))

    def get_data(tx):
        query = """
        MATCH (n:Entity)
        OPTIONAL MATCH (n)-[r]->(m:Entity)
        RETURN id(n) AS id, n.name AS name, n.type AS type,
               id(r) AS rel_id, type(r) AS rel_type, id(startNode(r)) AS source, id(endNode(r)) AS target
        """
        result = tx.run(query)
        nodes = {}
        edges = []
        for record in result:
            node_id = record["id"]
            if node_id not in nodes:
                nodes[node_id] = {
                    "id": node_id,
                    "name": record["name"],
                    "group": record["type"] or "Entity"
                }
            if record["rel_id"] is not None:
                edges.append({
                    "id": record["rel_id"],
                    "source": record["source"],
                    "target": record["target"],
                    "label": record["rel_type"].replace("_", " ").title()
                })
        return {"nodes": list(nodes.values()), "edges": edges}

    with driver.session() as session:
        graph_data = session.execute_read(get_data)
    driver.close()
    return graph_data

def create_graph_from_json(json_data):
    G = nx.Graph()
    node_labels = {}
    node_colors = {}
    for node in json_data['nodes']:
        node_id = node['id']
        node_name = node.get('name', 'Unnamed Node')
        node_group = node.get('group', 'Entity')
        G.add_node(node_id)
        node_labels[node_id] = node_name
        node_colors[node_id] = get_node_color(node_group)

    edge_labels = {}
    for edge in json_data['edges']:
        G.add_edge(edge['source'], edge['target'])
        edge_labels[(edge['source'], edge['target'])] = edge.get('label', '')

    return G, node_labels, node_colors, edge_labels

def draw_graph(G, labels, node_colors, edge_labels):
    pos = nx.spring_layout(G, k=1.4, iterations=75)
    plt.figure(figsize=(14, 12))
    ax = plt.gca()

    nx.draw_networkx_edges(G, pos, alpha=0.5, edge_color="#555555", width=0.8)
    nodes = nx.draw_networkx_nodes(G, pos, node_size=3500, node_color=list(node_colors.values()), alpha=0.9)
    nodes.set_edgecolor('black')

    nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_weight="bold", font_color="black")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, label_pos=0.5, alpha=0.7)

    ax.set_title("Sentence-Level Co-occurrence Knowledge Graph", fontsize=18)
    ax.axis("off")
    plt.tight_layout()
    st.pyplot(plt)

# def app():
#     st.title("Your Own Textbot")
#     st.subheader("Extract relationships based on co-occurrence within sentences.")

#     book_text = st.text_area("Paste text for analysis:", height=250, value="""
# Harry Potter saw Professor Dumbledore at Hogwarts. Dumbledore smiled kindly.
# Ron Weasley and Hermione Granger were studying nearby. They were reading a book.
# Voldemort was plotting his return. His followers were gathering.
# """)

#     if st.button("Process Text"):
#         with st.spinner("Analyzing text and creating graph..."):
#             process_book(book_text)

#     if st.button("Visualize Graph"):
#         with st.spinner("Fetching and rendering graph data..."):
#             graph_data = fetch_graph_data()
#             if graph_data["nodes"]:
#                 graph, node_labels, node_colors, edge_labels = create_graph_from_json(graph_data)
#                 draw_graph(graph, node_labels, node_colors, edge_labels)
#             else:
#                 st.warning("No entities or relationships found. Please process some text.")
