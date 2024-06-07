from fastapi import FastAPI, HTTPException, Depends
import httpx
from app.urls import urls  
from app.api.services.auth_service import AuthModule  
import pandas as pd
app = FastAPI()

class ItemsService:
    """
        get_item_metadata recupera os metadados de um item.
        get_item_version recupera as versoes dos items sendo o índice 0 o mais recente
    params:
        item_id > obtido no folder service folder_content service
        project_id > obtido no project service 
    """
    def __init__(self):
        self.base_url = urls['APS_HOST_BASE_URL']
        self.get_data_from_folders_url = urls['GET_DATA_FROM_FOLDERS_URL']
        self.auth_module = AuthModule()  # Assuming AuthModule handles token authentication

    async def get_item_metadata(self, project_id: str, item_id: str):
        url = f"{self.base_url}{self.get_data_from_folders_url}/{project_id}/items/{item_id}"
        token = await self.auth_module.get_token()
        if not token or not token.get('token'):
            raise HTTPException(status_code=400, detail="Failed to retrieve token")
        
        headers = {'Authorization': f"{token['token']}"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=60.0)
               
                response.raise_for_status()
              
                return pd.json_normalize(response.json().get('data'))
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail=str(e))

    async def get_item_version(self, project_id: str, item_id: str):
        url = f"{self.base_url}{self.get_data_from_folders_url}/{project_id}/items/{item_id}/versions"
        token = await self.auth_module.get_token()
        if not token or not token.get('token'):
            raise HTTPException(status_code=400, detail="Failed to retrieve token")
        
        headers = {'Authorization': f"{token['token']}"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=60.0)
                response.raise_for_status()
                return pd.json_normalize(response.json().get('data'))
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail=str(e))

items_service = ItemsService()
