import pandas as pd
from app.api.services.folders_service import FolderService


async def get_folder_content(projectId, folderId, folderService: FolderService):
    try:
        folder_content_df = await folderService.get_folder_content(
            project_id=projectId, folder_id=folderId
        )
        return folder_content_df
    except Exception as error:
        print(error)


async def get_top_folders(hubId, projectId, folderService: FolderService):
    top_foders_df = pd.DataFrame(await folderService.get_top_folders(hubId, projectId))
    return top_foders_df
