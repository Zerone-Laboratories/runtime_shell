import spacy
from textblob import TextBlob
import sys
from concurrent.futures import ThreadPoolExecutor

def process_statement(statement):
    # Load spaCy model
    nlp = spacy.load("en_core_web_sm")

    # Tokenization
    tokens = nlp(statement)

    # # Named Entity Recognition (NER)
    # entities = [(ent.text, ent.label_) for ent in tokens.ents]

    # Part-of-Speech (POS) Tagging
    pos_tags = [(token.text, token.pos_) for token in tokens]

    # # Dependency Parsing
    # dep_tree = [(token.text, token.dep_, token.head.text) for token in tokens]

    # # Sentiment Analysis
    # sentiment = TextBlob(statement).sentiment

    return pos_tags

def main():
    # Input natural language statement
    statement = sys.argv[1]

    # Number of workers
    num_workers = int(open("/home/zerone/Projects/runtime2/sysFiles/workers.zttf","r").read().replace("\n",""))

    # Using ThreadPoolExecutor to run tasks concurrently
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future = executor.submit(process_statement, statement)
        result = future.result()

    # Print results
    print("POS Tags:", result)

if __name__ == "__main__":
    main()
