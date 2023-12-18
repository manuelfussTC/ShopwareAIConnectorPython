import time
import requests
import json
from typing import List, Dict
import numpy as np


class EmbeddingGenerator:
    def __init__(self, api_key, model="text-embedding-ada-002", max_retries=3, retry_delay=5):
        self.api_key = api_key
        self.model = model
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def generate_embeddings(self, texts):
        url = "https://api.openai.com/v1/embeddings"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        embeddings = []
        for text in texts:
            print(f"Generiere Embedding für Text: {text}")  # Debugging-Info
            data = json.dumps({"input": text, "model": self.model})
            retries = 0
            while retries <= self.max_retries:
                response = requests.post(url, headers=headers, data=data)
                print(f"HTTP-Statuscode: {response.status_code}")  # Debugging-Info
                if response.status_code == 200:
                    decoded_response = response.json()
                    if 'data' in decoded_response and len(decoded_response['data']) > 0 and 'embedding' in \
                            decoded_response['data'][0]:
                        embeddings.append(decoded_response['data'][0]['embedding'])
                    break
                elif response.status_code == 503 and retries < self.max_retries:
                    print("503 Fehler - Wiederholung des Versuchs")  # Debugging-Info
                    retries += 1
                    time.sleep(self.retry_delay)
                else:
                    print(f"Fehler bei der Generierung von Embeddings: HTTP-Statuscode {response.status_code}")
                    print(
                        f"Response-Inhalt: {response.text}")  # Zeigt den Inhalt der Antwort an, wenn ein Fehler auftritt

        return embeddings


class EmbeddingProcessor:
    def __init__(self, embedding_generator):
        self.embedding_generator = embedding_generator

    def get_embedding_for_prompt(self, prompt):
        embeddings = self.embedding_generator.generate_embeddings([prompt])
        return embeddings[0] if embeddings else None  # Gib None zurück, wenn keine Embeddings vorhanden sind

    def find_most_similar_endpoints(self, prompt_embedding, endpoint_embeddings):
        if not isinstance(endpoint_embeddings, dict):
            print("endpoint_embeddings ist kein Dictionary.")
            return []
        if prompt_embedding is None:
            print("Prompt-Embedding ist None.")  # Debugging-Info
            return []

        similarities = {}

        for endpoint, embeddings in endpoint_embeddings.items():
            embedding = embeddings.get('get') or embeddings.get('post') or embeddings.get('put') or embeddings.get(
                'delete')
            if embedding is None:
                print(f"Kein Embedding für Endpunkt: {endpoint}")  # Debugging-Info
                continue

            similarity = self.cosine_similarity(prompt_embedding, embedding)
            similarities[endpoint] = similarity

        sorted_endpoints = sorted(similarities, key=similarities.get, reverse=True)
        return sorted_endpoints[:10]

    def cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        if not vec_a or not vec_b:
            print(f"Eines der Vektoren ist None oder leer: vec_a={vec_a}, vec_b={vec_b}")
            return 0

        if len(vec_a) != len(vec_b):
            print(f"Vektoren haben unterschiedliche Längen: vec_a={len(vec_a)}, vec_b={len(vec_b)}")
            return 0

        a = np.array(vec_a)
        b = np.array(vec_b)

        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)

        # Debugging-Ausgaben


        if norm_a == 0 or norm_b == 0:
            print("Einer der Vektoren hat eine Norm von 0")
            return 0

        similarity = dot_product / (norm_a * norm_b)
        return similarity
