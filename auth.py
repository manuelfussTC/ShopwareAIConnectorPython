import requests

class ShopwareAuthenticator:
    def __init__(self, client_id, client_secret, api_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_url = api_url
        self.access_token = None

    def authenticate(self):
        url = self.api_url + 'oauth/token'
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        headers = {
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()

            self.access_token = response.json().get('access_token')
            if not self.access_token:
                raise Exception('Authentication failed: access token not received.')

        except requests.RequestException as e:
            raise Exception(f'Error during authentication: {e}')
