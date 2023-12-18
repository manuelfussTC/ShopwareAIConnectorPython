import requests
import json
import urllib.parse

class ShopwareAPI:
    def __init__(self, authenticator):
        self.authenticator = authenticator

    def execute_api_call_with_headers(self, endpoint, headers, prompt, method='GET'):
        print(f"API-Aufruf mit Endpunkt: {endpoint}, Method: {method}")
        if not self.authenticator.access_token:
            self.authenticator.authenticate()

        endpoint = endpoint.replace('`', '')
        full_url = self.authenticator.api_url.rstrip('/') + '/' + endpoint.lstrip('/')

        if isinstance(headers, str):
            try:
                headers = json.loads(headers)
            except json.JSONDecodeError:
                print("Error parsing headers from string to dictionary")
                headers = {}

        query_components = []
        if method.upper() == 'GET':
            for key, value in headers.items():
                if key.lower() == 'filter':
                    for i, filter_condition in enumerate(value):
                        for filter_key, filter_value in filter_condition.items():
                            query_components.append(f'filter[{i}][{filter_key}]={urllib.parse.quote(str(filter_value))}')
                elif key.lower() in ['sort', 'associations', 'includes', 'aggregations', 'grouping', 'fields', 'post-filter']:
                    for i, item in enumerate(value):
                        query_components.append(f'{key}[{i}]={urllib.parse.quote(str(item))}')
                elif key.lower() == 'total-count-mode':
                    query_components.append(f'{key}={value}')
                else:
                    query_components.append(f'{key}={urllib.parse.quote(str(value))}')

            query_string = '&'.join(query_components)
            full_url += f"?{query_string}" if query_string else ""

        auth_header = {'Authorization': f'Bearer {self.authenticator.access_token}'}

        try:
            print(f"API-Aufruf an {full_url} mit Methode {method} und Headern {auth_header}")
            response = requests.request(method, full_url, headers=auth_header)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Fehler während des API-Aufrufs: {e}")
            return None

    def prepare_headers(self, header_string):
        if not isinstance(header_string, str):
            raise ValueError("header_string must be a string")

        try:
            headers = json.loads(header_string)
        except json.JSONDecodeError:
            raise ValueError("header_string is not a valid JSON string")

        processed_headers = {}
        for key, value in headers.items():
            if isinstance(value, (str, bytes)):
                processed_headers[key.strip()] = value.strip()
            else:
                processed_headers[key.strip()] = str(value)

        return processed_headers
