import asyncio
from fastapi import HTTPException
import httpx
from app.urls import urls  
from app.api.services.auth_service import AuthModule  
import pandas as pd

class RetrieveMetadataDerivativeService:
  """ 
    get_list_of_viewables pega as ids de views dos modelos.
    get_object_hierarchy pega a arvore hierarquica de objetos em uma view de um modelo específico
    get_properties volta todas as propriedades de objectos em uma view de modelo
  params:
    urnOfSouce > obtido no Item service
    dv_gui_0 > obtido no get_list_of_viewables
  """
  def __init__(self):
    self.base_url = urls['APS_HOST_BASE_URL']
    self.model_derivative_url = urls['MODEL_DERIVATIVE']
    self.auth_module = AuthModule()
    
    
  async def get_list_of_viewables(self, urnOfSouce):
    url = f"{self.base_url}{self.model_derivative_url}/{urnOfSouce}/metadata"
    token = await self.auth_module.get_token()
    if not token or not token.get('token'):
        raise HTTPException(status_code=400, detail="Failed to retrieve token")
    headers = {'Authorization': f"{token['token']}"}
    params = {'forceget': 'true'}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=60.0, params=params)
            response.raise_for_status()
            return pd.json_normalize(response.json().get('data').get('metadata'))
                     
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

  async def get_object_hierarchy(self, url_safe_urn_of_source, dv_gui_0):
    url = f"{self.base_url}{self.model_derivative_url}/{url_safe_urn_of_source}/metadata/{dv_gui_0}"
    token = await self.auth_module.get_token()
    if not token or not token.get('token'):
        raise HTTPException(status_code=400, detail="Failed to retrieve token")
    if not token or not token.get('token'):
        raise HTTPException(status_code=400, detail="Failed to retrieve token")
    headers = {'Authorization': f"{token['token']}"}
    params = {'forceget': 'true'}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=60.0, params=params)
            response.raise_for_status()
            response_json = pd.json_normalize(response.json().get('data'))
            print(response_json.columns)
            return response_json
            
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
          
  async def get_properties(self, url_safe_urn_of_source, dv_gui_0, objectid):
    url = f"{self.base_url}{self.model_derivative_url}/{url_safe_urn_of_source}/metadata/{dv_gui_0}/properties"
    # 
    token = await self.auth_module.get_token()
    if not token or not token.get('token'):
        raise HTTPException(status_code=400, detail="Failed to retrieve token")
    if not token or not token.get('token'):
        raise HTTPException(status_code=400, detail="Failed to retrieve token")
    headers = {'Authorization': f"{token['token']}"}
    params = {'forceget': 'true'}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=120, params=params)
            response.raise_for_status()
            response_json = pd.json_normalize(response.json().get('data'))
            print(response_json.columns)
            return response_json
            
            
        except httpx.HTTPStatusError as e:
            
            raise HTTPException(status_code=e.response.status_code, detail=str(e))


# for later use if necessary
  async def get_properties_query(self, url_safe_urn_of_source, dv_gui_0, objectid):
    url = f"{self.base_url}{self.model_derivative_url}/{url_safe_urn_of_source}/metadata/{dv_gui_0}/properties:query"
    token = await self.auth_module.get_token()
    if not token or not token.get('token'):
        raise HTTPException(status_code=400, detail="Failed to retrieve token")
    if not token or not token.get('token'):
        raise HTTPException(status_code=400, detail="Failed to retrieve token")
    headers = {'Authorization': f"Bearer {token['token']}", 'Content-Type': 'application/json'}
    body = {
        "query": {"oneOf":["objectid", objectid]
            },
        "fields": [
            "objectid",
            "properties.Element.*",
            "properties.Revit Type.*",
            "properties.Item",
            "BLSMarkupDescricao",
            "name"
            ]
        }
    params = {'forceget': 'true'}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=body, params=params, timeout=120)
           
            response.raise_for_status()
            
            response_df = pd.json_normalize(response.json().get('data'))
            if response_df is None or response_df.empty:
                response_df = pd.json_normalize(response.json().get('data').get('collection'))
            return response_df
            
            
        except httpx.HTTPStatusError as e:
            
            raise HTTPException(status_code=e.response.status_code, detail=str(e))