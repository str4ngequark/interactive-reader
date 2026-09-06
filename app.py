import streamlit as st
import json
import random
from src import NLPProcessor

@st.cache_resource
def load_processor():
    return NLPProcessor()

@st.cache_resource
def load_data():
    with open('data/fragments.json', 'r', encoding='utf-8') as f:
        sections = json.load(f)
    
    with open('data/english_paragraphs.json', 'r', encoding='utf-8') as f:
        english_fragments = json.load(f)
    
    return sections, english_fragments

st.set_page_config(page_title="Reader", layout="wide")

st.title("Reader")
st.markdown("*O Livro do Desassossego* | Portuguese → English")

with st.spinner("Loading NLP models..."):
    processor = load_processor()
    sections, english_fragments = load_data()

# Sidebar
st.sidebar.header("Navigation")

if st.sidebar.button("🎲 Random Fragment"):
    st.session_state.current_section = random.choice(list(sections.keys()))

if 'current_section' not in st.session_state:
    st.session_state.current_section = '1'

section_num = st.session_state.current_section
section = sections[section_num]

st.sidebar.markdown(f"**Fragment {section_num}**")
st.sidebar.markdown(f"**Total:** {len(sections)} fragments")

st.header(f"Fragment {section_num}")

# Get paragraphs
pt_paragraphs = section['paragraphs']
en_key = section_num
en_paragraphs = english_fragments.get(en_key, [])

# Process and display
with st.spinner("Processing text..."):
    # 1. Formatted Portuguese (with paragraph breaks)
    st.subheader("Portuguese (with translations)")
    formatted_text = processor.format_section(pt_paragraphs)
    st.markdown(formatted_text)
    
    st.markdown("---")
    
    # 2. English translation
    st.subheader("English Translation")
    if en_paragraphs:
        # Escape any existing asterisks, then wrap each paragraph in italics
        italic_paragraphs = []
        for para in en_paragraphs:
            # Escape asterisks so they don't interfere with markdown
            escaped_para = para.replace('*', r'\*')
            italic_paragraphs.append(f"*{escaped_para}*")
        english_text = '\n\n'.join(italic_paragraphs)
        st.markdown(english_text)
    else:
        st.markdown("*[Translation not available for this fragment]*")
    
    st.markdown("---")
    
    # 3. Clean Portuguese
    st.subheader("Portuguese (original)")
    clean_text = '\n\n'.join(pt_paragraphs)
    st.markdown(clean_text)

# Navigation
st.sidebar.markdown("---")
col1, col2 = st.sidebar.columns(2)

section_keys = sorted(sections.keys(), key=int)
current_idx = section_keys.index(section_num)

with col1:
    if st.button("← Previous") and current_idx > 0:
        st.session_state.current_section = section_keys[current_idx - 1]
        st.rerun()

with col2:
    if st.button("Next →") and current_idx < len(section_keys) - 1:
        st.session_state.current_section = section_keys[current_idx + 1]
        st.rerun()

st.sidebar.markdown("---")