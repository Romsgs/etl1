import httpx
from app.api.services.auth_service import AuthModule
from app.urls import urls
import pandas as pd


class ProjectsService:
    def __init__(self):
        self.base_url = urls["APS_HOST_BASE_URL"]
        self.get_hubs_url = urls["GET_HUBS_URL"]
        self.get_projects_url = urls["GET_PROJECTS_URL"]
        self.auth_module = AuthModule()

    async def get_all_projects(self, hub_id: str):
        url = f"{self.base_url}{self.get_hubs_url}/{hub_id}{self.get_projects_url}"
        token = await self.auth_module.get_token()
        if not token or not token.get("token"):
            raise Exception(status_code=400, detail="Failed to retrieve token")

        headers = {"Authorization": f"{token['token']}"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=120.0)
                response.raise_for_status()
                # return [item['id'] for item in response.json().get('data', [])]
                return pd.json_normalize(response.json().get("data", []))
            except httpx.HTTPStatusError as e:
                raise Exception(status_code=e.response.status_code, detail=str(e))

    async def get_specific_project(self, hub_id: str, project_id: str):
        url = f"{self.base_url}{self.get_hubs_url}/{hub_id}{self.get_projects_url}/{project_id}"
        token = await self.auth_module.get_token()
        if not token or not token.get("token"):
            raise Exception(status_code=400, detail="Failed to retrieve token")

        headers = {"Authorization": f"{token['token']}"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=120.0)
                response.raise_for_status()
                pd.json_normalize(response.json().get("data"))
            except httpx.HTTPStatusError as e:
                raise Exception(status_code=e.response.status_code, detail=str(e))


projects_service = ProjectsService()
