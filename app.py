import os
from dataclasses import dataclass, field

import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

# Initialize database connection
con = psycopg2.connect(os.getenv("DATABASE_URL"), cursor_factory=RealDictCursor)
cur = con.cursor()

# Create table if it doesn't exist
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS prompts (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        prompt TEXT NOT NULL,
        is_favorite BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
)
con.commit()

@dataclass
class Prompt:
    title: str
    prompt: str
    is_favorite: bool = False

def prompt_form(prompt=Prompt("", "", False)):
    with st.form(key="prompt_form", clear_on_submit=True):
        title = st.text_input("Title", value=prompt.title)
        prompt_text = st.text_area("Prompt", height=200, value=prompt.prompt)
        is_favorite = st.checkbox("Favorite", value=prompt.is_favorite)
        submitted = st.form_submit_button("Submit")
        if submitted and title and prompt_text:  # Ensure fields are filled
            return Prompt(title, prompt_text, is_favorite)
        elif submitted:
            st.error("Both title and prompt must be filled.")

st.title("Promptbase")
st.subheader("A simple app to store and retrieve prompts")

# Form for new or updated prompts
prompt = prompt_form()
if prompt:
    cur.execute("INSERT INTO prompts (title, prompt, is_favorite) VALUES (%s, %s, %s)", 
                (prompt.title, prompt.prompt, prompt.is_favorite))
    con.commit()
    st.success("Prompt added successfully!")
    st.experimental_rerun()

# Search bar
search_query = st.text_input("Search prompts")
if search_query:
    cur.execute("SELECT * FROM prompts WHERE title ILIKE %s OR prompt ILIKE %s ORDER BY created_at DESC", 
                ('%' + search_query + '%', '%' + search_query + '%'))
else:
    cur.execute("SELECT * FROM prompts ORDER BY created_at DESC")

prompts = cur.fetchall()

# Display prompts
for p in prompts:
    with st.expander(f"{p['title']} (created on {p['created_at'].date()})"):
        st.code(p['prompt'])
        if st.button("Toggle Favorite", key=f"fav-{p['id']}"):
            cur.execute("UPDATE prompts SET is_favorite = NOT is_favorite WHERE id = %s", (p['id'],))
            con.commit()
            st.experimental_rerun()
        if st.button("Delete", key=f"del-{p['id']}"):
            cur.execute("DELETE FROM prompts WHERE id = %s", (p['id'],))
            con.commit()
            st.experimental_rerun()