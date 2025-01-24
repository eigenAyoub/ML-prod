import pickle
import os

with open("all_paragraphs.pkl", 'rb') as f:
    all_paragraphs = pickle.load(f)

print(f"Number of paragraphs {len(all_paragraphs)}")

#x = sum([len(i.split(" ")) for i in all_paragraphs])/len(all_paragraphs)
#print(f"Avr number of words per paragraphs {x}")


import chromadb

chroma_client = chromadb.Client()


my_wiki = chroma_client.create_collection(name="my_wiki_01")

my_wiki.add(
    documents = all_paragraphs,
    ids = [f"id_{i}" for i in range(len(all_paragraphs))]
    )


