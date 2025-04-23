
#  Harry Potter Wiki — Interactive Knowledge System

A custom-built, interactive Harry Potter knowledge platform using natural language processing and knowledge graphs. This project extracts and structures data from the Harry Potter book series, enabling chatbot conversations, character relationship analysis, event timelines, and contradiction detection within the Wizarding World.

---

##  Tech Stack

- **Python 3.12**
- **Streamlit** — For interactive web app UI
- **Chroma DB** — Lightweight embedding database for NLP storage
- **Pandas, NumPy** — Data manipulation
- **NetworkX** — Knowledge graph creation and visualization
- **Matplotlib** — Data plotting
- **Custom NLP pipelines** for chatbot interaction, contradiction detection, and event analysis

---

##  Project Structure

```
harrypotterwiki/
├── app.py
├── models/
├── data/
├── harry_potter_chroma_db/
├── static/
├── alt/
├── .streamlit/
└── .gitignore
```

---

##  Installation & Running the Project Locally

### 1️1. Clone the Repository

```bash
git clone https://github.com/yourusername/harrypotterwiki.git
cd harrypotterwiki
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
add secrets.toml in .streamlit folder with a gemini api key and also password for your neo4j aura
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

### 5. Access the Web App

Visit `http://localhost:8501/` in your browser.

---

##  Features

-  Chatbot with contextual awareness from book data
-  Character relationship knowledge graph
-  Event timeline generation
-  Contradiction detection in narrative events
-  Embedding-based search via Chroma DB

---

##  Notes

- Ensure your Python version is **3.12** or compatible.
- Preloaded datasets include book text files and character/event information.
- Chroma DB is initialized locally, no cloud credentials required.

---
##  Contributors

- [Swayam Kelkar](https://github.com/Ecstaticvanilla)
- [Mithilesh Deshmukh](https://github.com/blast678)
- [Rachel Fernandes](https://github.com/Rachelferns)
- [Nitin Gawde](https://github.com/NitinGawde26)

---
##  Contributing

Pull requests and suggestions are welcome! If you encounter any bugs or have feature requests, feel free to open an issue.
