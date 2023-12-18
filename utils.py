import json
import re
from elevenlabstts import ElevenLabsTTS  # Importiere die ElevenLabsTTS Klasse


try:
    with open('config.json') as config_file:
        config = json.load(config_file)
    print("Configuration loaded successfully.")
    tts = ElevenLabsTTS(config['shopware'][
                            'elevenlabs'])  # Erstelle eine Instanz von ElevenLabsTTS mit dem API-Schlüssel aus der Konfiguration

except Exception as e:
    print(f"Error loading configuration: {e}")


def parse_headers(header_string):
    # Entferne Markdown-Codeblöcke, falls vorhanden
    header_string = header_string.replace('```json', '').replace('```', '').strip()

    try:
        # Versuche, den Header-String als JSON zu interpretieren
        headers = json.loads(header_string)
    except json.JSONDecodeError:
        # Fallback für nicht-JSON Header-String
        headers = {}
        # Hier kann deine bestehende Logik für das Parsen der Header eingefügt werden

    return headers



def simplify_schema(schema):
    simplified_schema = {}

    for method in ['get', 'post']:
        if method in schema:
            method_data = schema[method]
            simplified_params = []
            for param in method_data.get('parameters', []):
                param_info = {
                    'name': param.get('name', 'Unnamed'),
                    'description': param.get('description', 'No description')[:30] + '...' if param.get('description', False) else 'No description',
                    'required': param.get('required', False)
                }
                simplified_params.append(param_info)

            simplified_schema[method] = {
                'summary': method_data.get('summary', 'No summary'),
                'description': method_data.get('description', 'No description')[:50] + '...' if method_data.get('description', False) else 'No description',
                'parameters': simplified_params,
                'responses': {str(status_code): {'description': response.get('description', 'No description')[:30] + '...' if response.get('description', False) else 'No description'} for status_code, response in method_data.get('responses', {}).items()}
            }

    return simplified_schema





def get_schemas_for_endpoints(endpoints, prompt):
    with open('apiEndpoints.json', 'r') as file:
        api_endpoints = json.load(file)

    simplified_schemas = {}
    for endpoint in endpoints:
        if endpoint in api_endpoints['paths']:
            schema = api_endpoints['paths'][endpoint]
            simplified_schema = simplify_schema(schema)
            simplified_schemas[endpoint] = simplified_schema

    return build_prompt_with_schemas(simplified_schemas, prompt)





def simplify_parameters(parameters):
    simplified_parameters = []
    for param in parameters:
        name = param.get('name', 'Unnamed')
        description = param.get('description', 'No description')
        if len(description) > 30:
            description = description[:27] + '...'
        simplified_parameters.append({'name': name, 'description': description})
    return simplified_parameters

def simplify_responses(responses):
    simplified_responses = {}
    for status_code, response in responses.items():
        description = response.get('description', 'No description')
        if len(description) > 30:
            description = description[:27] + '...'
        simplified_responses[status_code] = {'description': description}
    return simplified_responses


def build_prompt_with_schemas(schemas, prompt):
    first_prompt = prompt
    # enhanced_prompt = (f"You are a well-experienced shopware developer with experience in Symfony and who knows "
    #                    f"the Shopware API best for over 20 years. This is my initial prompt: '{prompt}' and these are "
    #                    f"the possible schemas: '{json.dumps(schemas, indent=2)}' from the Shopware API that might help, "
    #                    "getting the data that is asked for within this prompt. "
    #                    "Give me only the exact, direct, clean, and unmodified answer to my question in the following: "
    #                    "I want you to give me the perfect endpoints for this case in a structure like "
    #                    "***endpoint 1*** here the data ***endpoint 1 end***, ***endpoint 2*** here the data ***endpoint 2 end***, "
    #                    "etc., and also the data part as this will be the head data for a cURL PHP call to the API always in JSON format. "
    #                    "If there will be no head with a data part as this is not always necessary, just skip this part and leave the head data part empty. "
    #                    "Use all information from the prompt to cover all parameters in the head also consider associations, "
    #                    "includes, ids, total-count-mode, page, limit, filter, post-filter, query, term, sort, aggregations, grouping. "
    #                    "Do not return complete curl calls, just the post or get content. Also return the CURLOPT_CUSTOMREQUEST method in a separated part like "
    #                    "***requestmethod 1*** here the data ***requestmethod 1 end*** Separate it in your answer like this "
    #                    "{{{head data 1}}} here the data {{{head data 1 end}}}, {{{head data 2}}} here the data {{{head data 2 end}}}, etc. "
    #                    "Please give me the perfect endpoints for this case and spare every additional information as I want to use those endpoints "
    #                    "and head data for a cURL PHP call to the Shopware API.")

    enhanced_prompt = (
        f"You are a well-experienced shopware developer with experience in Symfony and who knows "
        f"the Shopware API best for over 20 years. This is my initial prompt: '{prompt}' and these are "
        f"the possible schemas: '{json.dumps(schemas, indent=2)}' from the Shopware API that might help, "
        "getting the data that is asked for within this prompt. "
        "I want you to give me the perfect endpoints for this case in a structure like:\n"
        "***endpoint 1***\n`/example/endpoint1`\n***endpoint 1 end***\n\n"
        "***requestmethod 1***\n`GET`\n***requestmethod 1 end***\n\n"
        "{{{head data 1}}}\n```json\n{\n  \"example_key\": \"example_value\"\n}\n```\n{{{head data 1 end}}}\n\n"
        "Use all information from the prompt to cover all parameters in the head also consider associations, "
        "includes, ids, total-count-mode, page, limit, filter, post-filter, query, term, sort, aggregations, grouping. "
        "Do not return complete curl calls, just the post or get content. Also return the CURLOPT_CUSTOMREQUEST method in a separated part like:\n"
        "***requestmethod 1***\n`POST`\n***requestmethod 1 end***\n\n"
        "{{{head data 1}}}\nHere the data in JSON format\n{{{head data 1 end}}}\n\n"
        "Please give me the perfect endpoints for this case and spare every additional information as I want to use those endpoints "
        "and head data for a cURL PHP call to the Shopware API."
    )

    return enhanced_prompt


def extract_data_from_response(response, data_type):
    if data_type == 'endpoint':
        pattern = r'\*\*\*([Ee]ndpoint) \d+\*\*\*\s*`([^`]+)`\s*\*\*\*\1 \d+ end\*\*\*'
    elif data_type == 'head data':
        pattern = r'\{\{\{head data \d+\}\}\}\n```json\n(.*?)\n```\n\{\{\{head data \d+ end\}\}\}'
    elif data_type == 'requestmethod':
        pattern = r'\*\*\*requestmethod \d+\*\*\*\s*`([^`]+)`\s*\*\*\*requestmethod \d+ end\*\*\*'

    matches = re.findall(pattern, response, re.DOTALL)
    if data_type in ['endpoint']:
        # Extrahiere nur die relevante Gruppe (zweite Gruppe im Tupel)
        return [match[1] for match in matches]
    elif data_type == 'head data':
        return [match.strip() for match in matches]

    return matches



def process_gpt_response_to_extract_headers(gpt_response):
    print("Verarbeite GPT-Antwort, um Header zu extrahieren.")
    message1 = "Ich verarbeite die Antwort von GPT, um die Header zu extrahieren."
    #tts.synthesize(message1)  # Nutze die synthesize Methode für Sprachausgabe
    response_content = gpt_response['choices'][0]['message']['content']
    print(f'Inhalt der GPT-Antwort: {response_content}')
    endpoints = extract_data_from_response(response_content, 'endpoint')
    head_data = extract_data_from_response(response_content, 'head data')
    request_methods = extract_data_from_response(response_content, 'requestmethod')


    print(f'Gefundene Endpunkte: {endpoints}')
    print(f'Gefundene Header-Daten: {head_data}')
    print(f'Gefundene Requestmethoden: {request_methods}')
    results = []
    for index, endpoint in enumerate(endpoints):
        if index >= len(head_data):
            continue

        try:
            headers = json.loads(head_data[index])
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from head data: {e}")
            headers = {}

        method = request_methods[index] if index < len(request_methods) else 'GET'
        results.append({'endpoint': endpoint, 'headers': headers, 'method': method})

    return results