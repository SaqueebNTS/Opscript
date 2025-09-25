import requests
from requests.auth import HTTPBasicAuth
import json
import os
import config
import re
from jsonpath_ng import parse

class JiraUtils:
    JIRA_DOMAIN = config.JIRA_DOMAIN
    JIRA_EMAIL = config.JIRA_EMAIL
    JIRA_API_TOKEN = config.JIRA_API_TOKEN

    HEADERS = {"Accept": "application/json"}
    AUTH = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

    def __init__(self, issue_key):
        self.output_file = f"{issue_key}.json"
        self.url = f"https://{self.JIRA_DOMAIN}/rest/api/3/issue/{issue_key}"

    @staticmethod   
    def extract_figma_links(json_data):
        jsonpath_expr = parse('$..*')
    
        all_strings = [match.value for match in jsonpath_expr.find(json_data) if isinstance(match.value, str)]

        pattern = r'https?://(?:www\.)?figma\.com/[\w/?=&.-]+'

        figma_urls = []
        for s in all_strings:
            matches = re.findall(pattern, s)
            if matches:
                figma_urls.extend(matches)

        return list(set(figma_urls))

    def fetch_issue_data(self, ISSUE_KEY):
        response = requests.get(self.url, headers=self.HEADERS, auth=self.AUTH)
        if response.status_code != 200:
            print(f"❌ Failed to fetch issue: {response.status_code}")

        data = response.json()
        fields = data.get("fields", {})

        result = {
            "issue_key": ISSUE_KEY,
            "summary": fields.get("summary"),
            "description": fields.get("description", "No description"),
            "status": fields.get("status", {}).get("name"),
            "labels": fields.get("labels", []),
            "attachments": [],
            "comments": []
        }

        # Extracting attachments
        attachments = fields.get("attachment", [])
        for att in attachments:
            result["attachments"].append({
                "filename": att.get("filename"),
                "url": att.get("content")
            })

        # Extracting comments and filtering out non-text content
        comments = fields.get("comment", {}).get("comments", [])
        for c in comments:
            # Extract text from body and ignore non-text elements (e.g., media files)
            body = c.get("body", {})
            text_content = self.extract_text_from_body(body)

            result["comments"].append({
                "author": c.get("author", {}).get("displayName"),
                "body": text_content,  # Only the extracted text
                "created": c.get("created")
            })
        
        # Saving the result to a file
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        
        print(f"✅ Jira issue details saved to {self.output_file}")
        print(self.extract_figma_links(result))
        return self.extract_figma_links(result)


    def extract_text_from_body(self, body):
        """
        Extracts the text from a Jira comment body (which may include multiple types of content).
        This will traverse the body structure and gather only the text content.
        """
        text_content = ""
        
        # Check if the body is in a structured format with 'content'
        content = body.get("content", [])
        for element in content:
            if element.get("type") == "paragraph":
                # Iterate through the 'content' inside paragraphs to extract text
                for sub_element in element.get("content", []):
                    if sub_element.get("type") == "text":
                        text_content += sub_element.get("text", "")  # Append the text part

        return text_content
