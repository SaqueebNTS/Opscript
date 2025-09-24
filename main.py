from utils import FigmaUtils, JiraUtils
import config
import re



def fetch_figma_data(figma_file_id,nodes_id=None):
    figma = FigmaUtils(file_id=figma_file_id, nodes_id=nodes_id)
    figma_data = figma.fetch_figma_response()

def fetch_jira_data():
    jira = JiraUtils(config.ISSUE_KEY)
    figma_url_list = jira.fetch_issue_data(config.ISSUE_KEY)
    figma_info = {} 
    for url in figma_url_list:
        print("Figma URL found:", url)
        pattern = r"https://www\.figma\.com/design/([A-Za-z0-9]+).*\?node-id=([0-9]+-[0-9]+)"
        match = re.match(pattern, url)
        
        if match:
            file_id = match.group(1)
            node_id = match.group(2) 
            print (f"Extracted File ID: {file_id}, Node ID: {node_id}")
            figma_info[config.ISSUE_KEY] = {'file_id': file_id, 'node_id': node_id}
    return figma_info

def main():
    figma_info = fetch_jira_data()
    for issue_key, data in figma_info.items():
        file_id = data.get('file_id')
        node_id = data.get('node_id')
        
        fetch_figma_data(file_id, node_id)
    

if __name__ == "__main__":
    main()
    
