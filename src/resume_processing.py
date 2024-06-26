import re
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag
from src.database import create_sb_client

      
def nltk_to_wordnet_pos(nltk_tag):
    """
    Descr: Convert NLTK POS tag to WordNet POS tag.
    Input: nltk_tag
    Output: wordnet_pos
    """
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

      
def clean_and_lemmatize_resume(resume_data: str):
  """
  Descr: Clean text data by removing punctuation, stopwords, and converting to lowercase.
          Additionally, perform lemmatization on the cleaned text.
  Input: data (text)
  Output: cleaned and lemmatized text
  """
  stop_words = set(stopwords.words('english'))
  lemmatizer = WordNetLemmatizer() 
  clean_and_lemmatized_data  = []
  
  clean_data = re.sub(r"\{\{.*?\}\}", "", resume_data)
  clean_data = word_tokenize(clean_data)
  clean_data = [w.lower() for w in clean_data]
  clean_data = [word for word in clean_data if word.isalpha()]
  clean_data = [word for word in clean_data if word not in stop_words]

  tokens = word_tokenize(' '.join(clean_data))
  pos_tags = pos_tag(tokens)
  lemmatized_resume = [] 
  
  for word, tag in pos_tags:
    wn_tag = nltk_to_wordnet_pos(tag)
    if wn_tag is None: 
      lemmatized_word = lemmatizer.lemmatize(word)
    else:
      lemmatized_word = lemmatizer.lemmatize(word, pos=wn_tag)
    lemmatized_resume.append(lemmatized_word)  
  return ' '.join(lemmatized_resume)  
