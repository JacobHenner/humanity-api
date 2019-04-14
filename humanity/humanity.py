#!/bin/env python3

import requests
import arrow


class Humanity:
    OAUTH_URL = "https://www.humanity.com/oauth2/token.php"
    API_URL = "https://www.humanity.com/api/v2/"

    def __init__(self, username, password, client_id, client_secret):
        """Initialize Humanity API object
        
        Args:
            username (str): Humanity username
            password (str): Humanity password
            client_id (str): Humanity application ID
            client_secret (str): Humanity application secret
        """

        self._client_id = client_id
        self._client_secret = client_secret

        r = requests.post(
            self.OAUTH_URL,
            data={
                "username": username,
                "password": password,
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "grant_type": "password",
            },
        )
        r.raise_for_status()
        r = r.json()
        self._process_authn_response(r)

    def _verify_authn(self):
        if self._expiration < arrow.now():
            r = requests.post(
                self.OAUTH_URL,
                data={
                    "refresh_token": self._refresh_token,
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                    "grant_type": "refresh_token",
                },
            )
            r.raise_for_status()
            r = r.json()
            self._process_authn_response(r)

    def _process_authn_response(self, response):
        self._token = response["access_token"]
        self._refresh_token = response["refresh_token"]
        # Set expiration to be premature by 60 seconds to avoid lapses
        self._expiration = arrow.now().shift(seconds=response["expires_in"] - 60)

    def get(self, endpoint):
        """Sends a GET to the Humanity API at the given endpoint, returning the results
        
        Args:
            endpoint (str): API endpoint (e.g. "me")
        
        Returns:
            dict: Decoded JSON response
        """

        self._verify_authn()
        r = requests.get(f"{self.API_URL}{endpoint}?access_token={self._token}")
        r.raise_for_status()
        return r.json()
