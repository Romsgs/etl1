from fastapi import FastAPI, HTTPException, Depends
import httpx
import json
from app.api.services.auth_service import AuthModule  
from app.urls import urls  
import pandas as pd
app = FastAPI()

class HubsService:
    """
    atualmente busca um unico Hub.
    """
    def __init__(self):
        self.base_url = urls['APS_HOST_BASE_URL']
        self.get_hubs_url = urls['GET_HUBS_URL']
        self.auth_module = AuthModule()  

    async def get_all_hubs(self):
        url = f"{self.base_url}{self.get_hubs_url}"
        token = await self.auth_module.get_token()
        if not self.auth_module.is_token_valid():
            token = await self.auth_module.get_token()
            self.get_hubs_url(self)
        headers = {'Authorization': f"{token['token']}"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=60.0)
                response.raise_for_status()
                hubs_id_list = [item['id'] for item in response.json().get('data', [])]
                return hubs_id_list
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail=str(e))

    async def get_specific_hub(self, hub_id: str):
        url = f"{self.base_url}{self.get_hubs_url}/{hub_id}"
        token = await self.auth_module.get_token()
        if not token or not token.get('token'):
            raise HTTPException(status_code=400, detail="Failed to retrieve token")
        
        headers = {'Authorization': f"{token['token']}"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=60.0)
                response.raise_for_status()
                pd.json_normalize(response.json().get('data'))
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail=str(e))

