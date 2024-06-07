import httpx
from app.api.services.auth_service import AuthModule
from app.urls import urls
import pandas as pd


class VersionService:
    def __init__(self):
        self.base_url = urls["APS_HOST_BASE_URL"]
        self.get_data_from_folders_url = urls["GET_DATA_FROM_FOLDERS_URL"]
        self.auth_module = AuthModule()

    async def get_versions(self, project_id: str, version_id: str):
        url = f"{self.base_url}{self.get_data_from_folders_url}/{project_id}/versions/{version_id}"

        token = await self.auth_module.get_token()
        if not token or not token.get("token"):
            raise Exception(status_code=400, detail="Failed to retrieve token")

        headers = {"Authorization": f"{token['token']}"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=60.0)
                response.raise_for_status()

                pd.json_normalize(response.json().get("data"))
            except httpx.HTTPStatusError as e:

                raise Exception(status_code=e.response.status_code, detail=str(e))


version_service = VersionService()
