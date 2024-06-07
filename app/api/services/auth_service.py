from fastapi import APIRouter, HTTPException
import httpx
import base64
from app.env_config import FULL_SCOPE, APS_CLIENT_ID, APS_CLIENT_SECRET
from app.urls import urls
import time

router = APIRouter()

class AuthModule:
    """
    autenticação do cliente direto na APS.
    is_token_valid checa quanto tempo falta para a expiração do token. ajustar o tempo a mais para atender as necessidades
    """
    def __init__(self):
        self.base_url = urls['APS_HOST_BASE_URL']
        self.get_access_token_endpoint = urls['GET_ACCESS_TOKEN_ENDPOINT']
        self.full_scope = FULL_SCOPE
        self.client_id = APS_CLIENT_ID
        self.client_secret = APS_CLIENT_SECRET
        self.token_cache = {}
        self.set_headers()

    def set_headers(self):
        credentials = f"{self.client_id}:{self.client_secret}"
        authorization = base64.b64encode(credentials.encode()).decode('utf-8')
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Authorization': f'Basic {authorization}'
        }

    def body(self):
        return {
            'grant_type': 'client_credentials',
            'scope': self.full_scope
        }

    async def get_token(self):
        if self.is_token_valid():
            return self.token_cache
        
        url = f"{self.base_url}{self.get_access_token_endpoint}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, data=self.body(), headers=self.headers)
                response.raise_for_status()
                data = response.json()
                self.token_cache = {
                    'access_token': data['access_token'],
                    'token_type': data['token_type'],
                    'expires_in': data['expires_in'],
                    'token': f"{data['token_type']} {data['access_token']}",
                    'expires_at': time.time() + data['expires_in']
                }
                return self.token_cache
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail=str(e))

    def is_token_valid(self):
        segundos_a_mais = 800
        return self.token_cache and time.time() + segundos_a_mais < self.token_cache['expires_at']



















































