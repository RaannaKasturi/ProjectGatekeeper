import os
import json  # Import json to parse the string
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud.security.publicca import PublicCertificateAuthorityServiceClient

def gen_google_eab_data():
    load_dotenv()
    data = {
        "type": "service_account",
        "project_id": os.getenv("PROJECT_ID"),
        "private_key_id": os.getenv("PRIVATE_KEY_ID"),
        "private_key": os.getenv("PRIVATE_KEY").replace("\\n", "\n"),  # Ensure proper formatting
        "client_email": os.getenv("CLIENT_EMAIL"),
        "client_id": os.getenv("CLIENT_ID"),
        "auth_uri": os.getenv("AUTH_URI"),
        "token_uri": os.getenv("TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
        "universe_domain": os.getenv("UNIVERSE_DOMAIN")
    }
    return data

def gen_google_eab():
    service_account_info = gen_google_eab_data()
    if service_account_info is None:
        return None, None
    try:
        credentials = service_account.Credentials.from_service_account_info(service_account_info)
        client = PublicCertificateAuthorityServiceClient(credentials=credentials)
        project_id = service_account_info['project_id']
        parent = f"projects/{project_id}"
        
        # Call the method to create an external account key
        response = client.create_external_account_key(parent=parent)
        kid = response.key_id
        hmac = response.b64_mac_key
        return kid, hmac.decode()
    except Exception as e:
        print(f"Error generating Google EAB: {e}")
        return None, None  # Or appropriate error handling

# Example usage
if __name__ == "__main__":
    kid, hmac = gen_google_eab()
    if kid and hmac:
        print(f"KID: {kid}, HMAC: {hmac}")
    else:
        print("Failed to generate KID and HMAC.")
