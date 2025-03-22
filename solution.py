# Brandon Dionisio
# Conductor AI take-home project

from pypdf import PdfReader
import spacy
import re
from decimal import Decimal, InvalidOperation

PDF_URL = "demo.pdf"

# loading the SpaCy NLP model
nlp = spacy.load("en_core_web_sm")

# initialize the pdf reader to extract text from the pdf
reader = PdfReader(PDF_URL)

# storing all the parsed numbers in a list
all_numbers = []

# using regex to help determine multiplied numbers (ex. $100 billion = 100,000,000,000)
scaling_keywords = {
    "trillion": 1_000_000_000_000,
    "trillions": 1_000_000_000_000,
    "billion": 1_000_000_000,
    "billions": 1_000_000_000,
    "million": 1_000_000,
    "millions": 1_000_000,
    "K": 1_000,
    "M": 1_000_000,
    "thousand": 1_000,
    "thousands": 1_000
}

def extract_scaled_value(text):
    # regex to match any potentially scalable numbers (unfortunately didn't get functionality with tables)
    # group 1: currency symbol like $, €, £ and optional space
    # group 2: the number itself (e.g., 733.2 or 3,000) and another optional space
    # group 3: optional scale words
    match = re.search(r'([\$€£]?)\s?([\d,.]+)\s?(trillion|trillions|billion|billions|million|millions|thousand|thousands|K|M)?', text.lower())
    if not match:
        return None
    
    # removing any commas from the number
    num_str = match.group(2).replace(",", "")

    # adding any scaling words
    scale = match.group(3)
    try:
        # applying the scalar if it exists
        value = Decimal(num_str)
        multiplier = scaling_keywords.get(scale, 1)
        return value * multiplier
    except InvalidOperation:
        return None

# looping through each page of the pdf
print("Scanning PDF...")
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if not text:
        continue

    # using the SpaCy NLP on the page to extract the named entities
    doc = nlp(text)

    for ent in doc.ents:
        # for each of the number-related entities...
        if ent.label_ in ["MONEY", "CARDINAL", "QUANTITY", "PERCENT"]:
            # extract the value and add it to the number list
            scaled = extract_scaled_value(ent.text)
            if scaled is not None:
                all_numbers.append(scaled)

# find the largest value
if all_numbers:
    max_value = max(all_numbers)
    print(f"Largest number found: {max_value:,}")
else:
    print("No numbers found :(")
