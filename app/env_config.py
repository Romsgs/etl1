import os


from dotenv import load_dotenv
load_dotenv()


APS_CLIENT_ID = os.getenv('APS_CLIENT_ID', '')
APS_CLIENT_SECRET = os.getenv('APS_CLIENT_SECRET', '')
SERVER_SESSION_SECRET = os.getenv('SERVER_SESSION_SECRET', '')
EXPRESS_SESSION_SECRET = os.getenv('EXPRESS_SESSION_SECRET', '')
APS_CALLBACK_URL = os.getenv('APS_CALLBACK_URL', '')
PORT = int(os.getenv('PORT', 3001))


FULL_SCOPE = os.getenv('FULL_SCOPE', '')
LOW_SCOPE = os.getenv('LOW_SCOPE', '')


INTERNAL_TOKEN_SCOPES = ["data:read"]
PUBLIC_TOKEN_SCOPES = ["viewables:read"]

BLOB_TOKEN_SAS = os.getenv('BLOB_TOKEN_SAS', '')
URL_SAS_BLOB = os.getenv('URL_SAS_BLOB', '')
BLOB_CONTAINER_NAME = os.getenv('BLOB_CONTAINER_NAME', '')