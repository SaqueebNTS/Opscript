from dotenv import load_dotenv
import os

load_dotenv()

ISSUE_KEY = "TMG-3690"

# Figma Configuration
FIGMA_ACCESS_TOKEN = os.environ['FIGMA_ACCESS_TOKEN']
FIGMA_FILE_KEY = 'your-figma-file-key'
FIGMA_API_BASE_URL='https://api.figma.com/v1/files'



# Jira Configuration
JIRA_DOMAIN = os.environ['JIRA_DOMAIN']
JIRA_EMAIL = os.environ['JIRA_EMAIL']
JIRA_API_TOKEN = os.environ['JIRA_API_TOKEN']
JIRA_PROJECT_KEY = 'PROJECTKEY'
