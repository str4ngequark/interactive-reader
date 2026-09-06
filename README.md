# Interactive Reader

An interactive reading tool for Brazilian Portuguese learners, demonstrated on Fernando Pessoa's *O Livro do Desassossego* (The Book of Disquiet).

## Overview

The reader automatically identifies difficult words based on frequency analysis and provides inline translations using the Helsinki-NLP/opus-mt-ROMANCE-en model. Each section displays three views:
- **Annotated Portuguese**: Original text with translations of uncommon words
- **English translation**: Full paragraph translation for context
- **Clean Portuguese**: Original text without annotations

Live demo: https://interactive-reader.streamlit.app

## How It Works

1. **Frequency Analysis**: Uses a Portuguese word frequency dictionary to identify the most common words
2. **Lemmatization**: spaCy extracts the base form of each word for accurate translation lookup
3. **Translation**: The model translates uncommon words while preserving context
4. **Display**: Results are formatted with inline translations in italics


## Coming Soon

- Improved verb conjugation handling
- Progressive difficulty adjustment based on learner level
- Better parallel text alignment between Portuguese and English editions
- Support for additional Portuguese texts

## Setup

```bash
# Clone the repository
git clone [repo-url]
cd reader

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download pt_core_news_sm

# Run the application
streamlit run app.py
