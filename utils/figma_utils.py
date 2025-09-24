import requests
import config
from .save_json import process_figma_response

class FigmaUtils:
    def __init__(self, **kwargs):
        self.access_token = config.FIGMA_ACCESS_TOKEN
        self.file_id = kwargs.get('file_id')
        self.nodes_id = f"nodes?ids={kwargs.get('nodes_id')}" if kwargs.get("nodes_id",None) else ""
        self.base_url = f"{config.FIGMA_API_BASE_URL}/{self.file_id}/{self.nodes_id}"

    def fetch_figma_response(self):
        headers = {
            'X-Figma-Token': config.FIGMA_ACCESS_TOKEN
        }
        response = requests.get(self.base_url, headers=headers)

        if response.status_code == 200:
            process_figma_response(response.json())
        else:
            print(f"Failed to fetch Figma file data. Status code: {response.status_code}")
            print("Response:", response.text)
        
