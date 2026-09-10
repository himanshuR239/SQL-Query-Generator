# 🤖 AI-Powered SQL Query Generator & Executor

An intelligent full-stack SQL query generation, execution, and explanation platform powered by **Google Gemini AI**, **FastAPI**, **Streamlit**, and **SQLAlchemy**.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **Natural Language to SQL** | Converts everyday English questions into optimized SQLite queries |
| 💡 **AI Query Explanation** | Step-by-step plain-English explanation of how your SQL query works |
| 🚀 **Interactive Execution** | Runs queries safely and renders results in a Pandas DataFrame table |
| 📥 **CSV Export** | Export and download query result sets in CSV format with a single click |
| 📂 **Custom Database Upload** | Upload your own SQLite `.db` or `.sqlite` file and hot-swap connections instantly |
| 🔍 **Schema Exploration** | Browse available tables, view column schemas, and preview the first 5 rows |
| 📜 **Rolling Query History** | Retains the last 5 executed queries in session state for quick re-execution |
| 🛡️ **Security Guardrails** | Enforces read-only operations (SELECT, WITH, PRAGMA) and blocks destructive commands |

---

## 📁 Project Structure

```
AI-Powered-SQL-Query-Generator/
│
├── app.py               # FastAPI backend REST API routes
├── database.py          # Database connection management & schema reflection
├── query_generator.py   # Gemini AI query generation, parsing & execution logic
├── ui.py                # Streamlit interactive frontend application
├── chinook.db           # Default sample SQLite database (Music store)
├── requirements.txt     # Project dependencies
├── .env                 # Environment configuration (API keys & DB path)
└── .gitignore
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────┐
│        Streamlit UI (ui.py)     │  ← User interacts here
│  - Natural language input       │
│  - DB upload & schema explorer  │
│  - Results table + CSV export   │
└────────────┬────────────────────┘
             │ HTTP (requests)
             ▼
┌─────────────────────────────────┐
│      FastAPI Backend (app.py)   │  ← 7 REST endpoints
│  /generate_sql  /execute_sql    │
│  /explain_sql   /upload_db      │
│  /list_databases/tables/columns │
└──────┬─────────────┬────────────┘
       │             │
       ▼             ▼
┌────────────┐  ┌──────────────────────────┐
│ database.py│  │   query_generator.py     │
│ SQLAlchemy │  │ Gemini AI + sqlparse     │
│ Hot-swap   │  │ Safety validator         │
└────────────┘  └──────────────────────────┘
```

---

## ⚡ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/himanshuR239/SQL-Query-Generator.git
cd SQL-Query-Generator
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY="your-google-gemini-api-key"
SQLITE_DB_PATH="chinook.db"
```
> Get your free Gemini API key at [Google AI Studio](https://aistudio.google.com/apikey)

### 4. Run FastAPI Backend
```bash
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```
Swagger API docs: **http://127.0.0.1:8000/docs**

### 5. Run Streamlit UI
In a **second terminal**:
```bash
streamlit run ui.py
```
App opens at: **http://localhost:8501**

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/list_databases/` | List available databases |
| `GET` | `/list_tables/{database_name}` | List tables in a database |
| `GET` | `/list_columns/{database_name}/{table_name}` | List columns in a table |
| `POST` | `/generate_sql/` | Generate SQL from natural language |
| `POST` | `/execute_sql/` | Execute SQL and return results |
| `POST` | `/upload_db/` | Upload and hot-swap a SQLite database |
| `POST` | `/explain_sql/` | Get AI explanation of a SQL query |

---

## 🛡️ Security

- All queries are validated before execution
- Only **SELECT**, **WITH**, and **PRAGMA** statements are allowed
- Destructive commands (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`) are **blocked at the code level**

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend API | FastAPI + Uvicorn |
| AI / NLP | Google Gemini 1.5 Flash |
| DB Abstraction | SQLAlchemy |
| SQL Validation & Formatting | sqlparse |
| Sample Database | Chinook SQLite (Music Store) |
| Config | python-dotenv |

---

## 📊 Sample Queries to Try

With the default `chinook.db` loaded, try these natural language queries:
- *"Show me the top 5 customers by total purchase amount"*
- *"List all tracks in the Rock genre with their album names"*
- *"Which artists have more than 5 albums?"*
- *"Show total sales by country"*

---

## 👤 Author

**Himanshu R** — [GitHub](https://github.com/himanshuR239)
