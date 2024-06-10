import httpx
from app.urls import urls
from app.api.services.auth_service import AuthModule
import pandas as pd


class FolderService:
    """get_top_folders pega as pastas no nível root do sistema de arquivos da APS
    get_folder_content pega o conteúdo de uma pasta
    params:
    hub_id > obtido no hubs service
    project_id > extraído no folder service get_all_projects
    folder_id > obtido no get_top_folders

    """

    def __init__(self):
        self.base_url = urls["APS_HOST_BASE_URL"]
        self.get_hubs_url = urls["GET_HUBS_URL"]
        self.get_projects_url = urls["GET_PROJECTS_URL"]
        self.folders_url = urls["FOLDERS_URL"]
        self.get_data_from_folders_url = urls["GET_DATA_FROM_FOLDERS_URL"]
        self.auth_module = AuthModule()

    async def get_top_folders(self, hub_id: str, project_id: str):
        url = f"{self.base_url}{self.get_hubs_url}/{hub_id}{self.get_projects_url}/{project_id}/topFolders"
        token = await self.auth_module.get_token()
        if not token or not token.get("token"):
            raise Exception(status_code=400, detail="Failed to retrieve token")
        headers = {"Authorization": f"{token['token']}"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=120.0)
                response.raise_for_status()
                response_json = pd.json_normalize(response.json().get("data"))
                return response_json
            except httpx.HTTPStatusError as e:
                raise Exception(status_code=e.response.status_code, detail=str(e))

    async def get_folder_content(self, project_id: str, folder_id: str):

        url = f"{self.base_url}{self.get_data_from_folders_url}/{project_id}{self.folders_url}/{folder_id}/contents"

        token = await self.auth_module.get_token()

        if not token or not token.get("token"):
            raise Exception(status_code=400, detail="Failed to retrieve token")
        headers = {"Authorization": f"{token['token']}"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=120.0)
                response_json = pd.json_normalize(
                    response.json().get("data"), max_level=50
                )
                response.raise_for_status()
                return response_json
            except httpx.HTTPStatusError as e:
                raise Exception(status_code=e.response.status_code, detail=str(e))


folder_service = FolderService()
