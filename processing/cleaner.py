import re
import unicodedata

def clean_text(text: str)-> str:
  if not text:
    return ""

  text= unicodedata.normalize("NFKC", text)
  text= re.sub(r"http\S+|www\S+", "", text)
  text= re.sub(r"\s+", " ", text)
  text= text.lower().strip()

  return text


