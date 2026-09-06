import spacy
import torch
from transformers import MarianTokenizer, MarianMTModel
import json
import warnings

class NLPProcessor:
    def __init__(self):
        """Initialize all NLP resources."""
        warnings.filterwarnings("ignore", message=".*unauthenticated requests.*")
        
        self.nlp = spacy.load("pt_core_news_sm")
        
        model_name = "Helsinki-NLP/opus-mt-ROMANCE-en"
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name)
        
        with open('data/pt_br_frequency.json', 'r', encoding='utf-8') as f:
            full_freq_dict = json.load(f)
        
        threshold_count = 2000
        sorted_words = sorted(full_freq_dict.items(), key=lambda x: x[1], reverse=True)
        top_n_words = [word for word, freq in sorted_words[:threshold_count]]
        self.common_words_set = set(top_n_words)
    
    def translate_word(self, word, lemma):
        """Translate a Portuguese word to English using its lemma."""
        try:
            inputs = self.tokenizer(lemma, return_tensors="pt", padding=True)
            with torch.no_grad():
                outputs = self.model.generate(**inputs, max_length=50)
            translation = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
            
            if word[0].islower():
                translation = translation.lower()
            
            return translation
        except Exception:
            return word
    
    def format_paragraph(self, text):
        """Format a single paragraph with inline translations."""
        doc = self.nlp(text)
        result = []
        
        for sent in doc.sents:
            sent_result = []
            
            for token in sent:
                if token.is_space or token.is_punct:
                    sent_result.append(token.text)
                    continue
                
                lemma = token.lemma_.lower()
                
                should_translate = (
                    lemma not in self.common_words_set and
                    len(lemma) > 3 and
                    lemma.isalpha()
                )
                
                if should_translate:
                    translation = self.translate_word(token.text, lemma)
                    sent_result.append(f"{token.text} *({translation})*")
                else:
                    sent_result.append(token.text)
            
            # Join with proper spacing
            formatted_sentence = ""
            for i, word in enumerate(sent_result):
                if i == 0:
                    formatted_sentence = word
                elif word in [".", ",", ";", ":", "!", "?", ")", "]", "}"]:
                    formatted_sentence += word
                else:
                    formatted_sentence += " " + word
                    
            result.append(formatted_sentence)
        
        return " ".join(result)
    
    def format_section(self, paragraphs):
        """Format all paragraphs in a section, preserving paragraph breaks."""
        formatted_paragraphs = []
        for para in paragraphs:
            formatted = self.format_paragraph(para)
            formatted_paragraphs.append(formatted)
        
        return "\n\n".join(formatted_paragraphs)