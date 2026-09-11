import os
from google import genai
from google.genai import types
import sqlparse
import re
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import database
from database import list_databases, list_tables, list_columns

# Load environment variables
load_dotenv()

# Configure Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Limits to avoid token limit issues
MAX_TABLES = 15
MAX_COLUMNS_PER_TABLE = 10

# Supported models with fallback resilience (gemini-3.6-flash is active and fast)
MODEL_CANDIDATES = ["gemini-3.6-flash", "gemini-flash-latest", "gemini-3.5-flash"]

def generate_content_with_fallback(prompt: str) -> str:
    """Attempts generation with primary model, falling back to backup models on temporary errors."""
    last_exception = None
    for model_name in MODEL_CANDIDATES:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            last_exception = e
            continue
    if last_exception:
        raise last_exception
    raise RuntimeError("No response from Gemini API.")


def clean_sql_output(response_text):
    """Extracts SQL query from AI response and formats it."""
    clean_query = re.sub(r"```(?:sql)?\s*(.*?)\s*```", r"\1", response_text, flags=re.DOTALL)
    clean_query = clean_query.strip()
    return sqlparse.format(clean_query, reindent=True, keyword_case='upper')


def get_limited_schema():
    """Fetches a reduced database schema to fit within token limits."""
    schema = {}
    databases = list_databases().get("databases", [])
    for db in databases:
        schema[db] = {}
        tables = list_tables(db).get("tables", [])[:MAX_TABLES]
        for table in tables:
            schema[db][table] = list_columns(db, table).get("columns", [])[:MAX_COLUMNS_PER_TABLE]
    return schema

def generate_sql_query(nl_query):
    """Converts a natural language query into an optimized SQL query using Gemini."""
    schema = get_limited_schema()
    schema_text = "\n".join([
        f"{table}: {', '.join(columns)}" for db, tables in schema.items() for table, columns in tables.items()
    ])

    prompt = f"""
You are an SQL expert. Convert the following natural language query into an optimized SQLite query.
- Do NOT use MySQL-specific syntax.
- Use indexing where applicable.
- Prefer JOINS over subqueries.
- Use GROUP BY for aggregations if needed.
- Return ONLY the raw SQL query. Do not explain the query.

Database Schema (Limited View):
{schema_text}

User Query: {nl_query}

SQL Query:
"""

    try:
        raw_sql_query = generate_content_with_fallback(prompt)
        return clean_sql_output(raw_sql_query)

    except Exception as e:
        return f"Error generating SQL query: {e}"

def execute_query(sql_query):
    try:
        # Code-level validation to block destructive non-SELECT queries
        formatted_query = sqlparse.format(sql_query, strip_comments=True).strip().upper()
        if not (formatted_query.startswith("SELECT") or formatted_query.startswith("WITH") or formatted_query.startswith("PRAGMA")):
            return {"error": "Security Block: Only read-only queries (SELECT) are allowed."}

        with database.engine.connect() as connection:
            result = connection.execute(text(sql_query))
            rows = result.fetchall()

            # Get column names
            column_names = result.keys()

            # Convert results into a list of dictionaries
            formatted_results = [dict(zip(column_names, row)) for row in rows]

            return {"results": formatted_results}

    except SQLAlchemyError as e:
        return {"error": str(e)}

def explain_sql_query(sql_query: str) -> str:
    """Generates a plain-English explanation of the SQL query."""
    prompt = f"Explain this SQL query in plain English, step-by-step:\n\n{sql_query}"
    try:
        return generate_content_with_fallback(prompt)
    except Exception as e:
        return f"Error explaining SQL query: {e}"

