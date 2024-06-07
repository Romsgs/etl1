from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

class Blob_Storage_Service():
    def __init__(self, account_url, container_name):
        self.account_url = account_url
        self.container_name = container_name
        self.default_credential = DefaultAzureCredential()
        self.blob_service_client = BlobServiceClient(account_url, credential=self.default_credential)
        
    def upload_to_blob(self, path_to_file):
        try:
            blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=path_to_file)
            with open(path_to_file, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            print(f"File {path_to_file} uploaded successfully.")
        except Exception as e:
            print(f"Failed to upload {path_to_file}: {e}")

# blob_service = Blob_Storage_Service(account_url="https://saengenhariadedados.blob.core.windows.net", container_name="container-blossom")

# file_path = "path/to/your/excel/file.xlsx"
# blob_service.upload_to_blob(file_path)
