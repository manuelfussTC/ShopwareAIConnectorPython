import json
import os
import sys

from dotenv import load_dotenv
from auth import ShopwareAuthenticator
from api_communication import ShopwareAPI
from gpt_communication import GPTCommunicator
from embedding_processing import EmbeddingProcessor, EmbeddingGenerator
from utils import get_schemas_for_endpoints, process_gpt_response_to_extract_headers
from elevenlabstts import ElevenLabsTTS  # Importiere die ElevenLabsTTS Klasse
from asr import ASR
from speech_input import SpeechInput



try:
    with open('config.json') as config_file:
        config = json.load(config_file)
    print("Configuration loaded successfully.")
    tts = ElevenLabsTTS(config['shopware'][
                            'elevenlabs'])  # Erstelle eine Instanz von ElevenLabsTTS mit dem API-Schlüssel aus der Konfiguration

except Exception as e:
    print(f"Error loading configuration: {e}")

try:
    with open(os.path.join(os.getcwd(), 'embeddings.json')) as embeddings_file:
        endpoint_embeddings = json.load(embeddings_file)
    print("Embeddings loaded successfully.")
except Exception as e:
    print(f"Error loading embeddings: {e}")

if endpoint_embeddings is None:
    raise Exception('Error loading embeddings from embeddings.json file.')

authenticator = ShopwareAuthenticator(config['shopware']['client_id'], config['shopware']['client_secret'],
                                      config['shopware']['api_url'])
api_key = config['shopware']['OPENAI_API_KEY']
shopware_api = ShopwareAPI(authenticator)
gpt_communicator = GPTCommunicator(api_key)
embedding_generator = EmbeddingGenerator(api_key)
embedding_processor = EmbeddingProcessor(embedding_generator)

# prompt = "Return all items in my store with name and price and articlenumber, limit 4"
#prompt = "Show all categories in my store with name and type, limit 4"
# prompt = "Show all salechannels in my store with name and id"
# prompt = "Return all customers and show me only first name and last name in the result"
# prompt = "Return all customers with a first name 'Emil' or 'Martina'  and show me only first name and last name and id and street in the result"

openai_api_key = config['shopware']['OPENAI_API_KEY']
# Erstelle eine Instanz von SpeechInput mit dem API-Key
speech_input = SpeechInput(openai_api_key)

# Spracheingabe für den Prompt
print("Bitte geben Sie den Prompt per Sprache ein:")
prompt = speech_input.get_transcription()
print(f"Empfangener Prompt: {prompt}")

try:
    prompt_embedding = embedding_processor.get_embedding_for_prompt(prompt)
    print(f"Embedding für Prompt '{prompt}' erstellt: {prompt_embedding}")
    message1 = "Der Prompt lautet " + prompt + ". Ich habe ein Embedding für den Prompt erstellt."
    #tts.synthesize(message1)  # Nutze die synthesize Methode für Sprachausgabe

    most_similar_endpoints = embedding_processor.find_most_similar_endpoints(prompt_embedding, endpoint_embeddings)
    print(f"Am meisten ähnliche Endpunkte für das Embedding gefunden: {most_similar_endpoints}")
    message2 = "Ich habe die am meisten ähnlichen Endpunkte gefunden."
    #tts.synthesize(message2)  # Nutze die synthesize Methode für Sprachausgabe

    enhanced_prompt = get_schemas_for_endpoints(most_similar_endpoints, prompt)
    print(f"Verbesserter GPT-Prompt: {enhanced_prompt[:200]}...")
    message3 = "Ich habe den GPT-Prompt verbessert."
    #tts.synthesize(message3)  # Nutze die synthesize Methode für Sprachausgabe

    gpt_response = gpt_communicator.send_gpt_request(enhanced_prompt)
    print("Antwort von GPT erhalten.")
    message4 = "Ich habe eine Antwort von GPT erhalten."
    #tts.synthesize(message4)  # Nutze die synthesize Methode für Sprachausgabe

    headers = process_gpt_response_to_extract_headers(gpt_response)
    print(f"Headers aus der GPT-Antwort extrahiert: {headers}")
    message5 = "Ich habe die Header aus der GPT-Antwort extrahiert."
    #tts.synthesize(message5)  # Nutze die synthesize Methode für Sprachausgabe

    api_responses = []
    for header_info in headers:
        endpoint = header_info['endpoint']
        headers_json = json.dumps(header_info['headers'])
        method = header_info['method']
        print(f'Making API call to {endpoint} with headers: {headers_json} and method {method}')
        api_response = shopware_api.execute_api_call_with_headers(endpoint, headers_json, prompt, method)
        api_responses.append(api_response)
        print(f'Received response from {endpoint}')

    # Verarbeiten und Zusammenfassen der API-Antworten
    combined_responses = {"responses": api_responses}

    # Erstellen eines neuen Prompts für GPT
    new_prompt = {
        "original_prompt": prompt,
        "api_responses": combined_responses
    }
    enhanced_gpt_prompt = json.dumps(new_prompt, indent=2)
    # print("Sending to GPT:", enhanced_gpt_prompt)


    # Senden des neuen Prompts an GPT
    gpt_response = gpt_communicator.send_gpt_request(enhanced_gpt_prompt)

    # Ausgabe nur des 'content'-Teils der GPT-Antwort
    gpt_content = gpt_response['choices'][0]['message']['content']
    print("GPT Content Response:", gpt_content)
    #message6 = "Ich habe eine Antwort von GPT erhalten. Hier ist der Inhalt: " + gpt_content
    tts.synthesize(gpt_content)  # Nutze die synthesize Methode für Sprachausgabe

except Exception as e:
    print(f"Ein Fehler ist aufgetreten: {e}")
