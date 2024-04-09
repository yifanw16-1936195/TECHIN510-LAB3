import os
from dataclasses import dataclass
import datetime

import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

con = psycopg2.connect(os.getenv("DATABASE_URL"), cursor_factory=RealDictCursor)
cur = con.cursor()

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
        if submitted and title and prompt_text:  
            return Prompt(title, prompt_text, is_favorite)
        elif submitted:
            st.error("Both title and prompt must be filled.")

st.title("Promptbase")
st.subheader("A simple app to store and retrieve prompts")

# Filtering and sorting options
date_filter = st.selectbox(
    'Filter by date',
    ('All Time', 'Today', 'This Week', 'This Month', 'This Year')
)

if date_filter == 'Today':
    start_date = datetime.date.today()
elif date_filter == 'This Week':
    start_date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
elif date_filter == 'This Month':
    start_date = datetime.date.today().replace(day=1)
elif date_filter == 'This Year':
    start_date = datetime.date.today().replace(month=1, day=1)
else:
    start_date = None

filter_favorite = st.checkbox('Show only favorites')

# Applying the filter and sort query
if start_date:
    cur.execute("""
        SELECT * FROM prompts 
        WHERE created_at >= %s
        AND (%s OR is_favorite = true)
        ORDER BY created_at DESC""", 
        (start_date, not filter_favorite))
else:
    cur.execute("""
        SELECT * FROM prompts 
        WHERE %s OR is_favorite = true
        ORDER BY created_at DESC""", 
        (not filter_favorite,))

prompts = cur.fetchall()

# Displaying prompts with improved favorite visibility
for p in prompts:
    favorite_status = "❤️" if p['is_favorite'] else "🖤"
    with st.expander(f"{favorite_status} {p['title']} (created on {p['created_at'].date()})"):
        st.code(p['prompt'])
        if st.button("Toggle Favorite", key=f"fav-{p['id']}"):
            cur.execute("UPDATE prompts SET is_favorite = NOT is_favorite WHERE id = %s", (p['id'],))
            con.commit()
            st.experimental_rerun()
        if st.button("Delete", key=f"del-{p['id']}"):
            cur.execute("DELETE FROM prompts WHERE id = %s", (p['id'],))
            con.commit()
            st.experimental_rerun()

prompt = prompt_form()
if prompt:
    cur.execute("INSERT INTO prompts (title, prompt, is_favorite) VALUES (%s, %s, %s)", 
                (prompt.title, prompt.prompt, prompt.is_favorite))
    con.commit()
    st.success("Prompt added successfully!")
    st.experimental_rerun()
