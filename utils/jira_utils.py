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

        attachments = fields.get("attachment", [])
        for att in attachments:
            result["attachments"].append({
                "filename": att.get("filename"),
                "url": att.get("content")
            })

        
        comments = fields.get("comment", {}).get("comments", [])
        for c in comments:
            result["comments"].append({
                "author": c.get("author", {}).get("displayName"),
                "body": c.get("body"),
                "created": c.get("created")
            })
        
        
        # for key, value in fields.items():
        #     if key.startswith("customfield") and value:
        #         try:
        #             # If value is a string that looks like JSON or contains PR summary, keep it
        #             if isinstance(value, str) and ("pullrequest" in value or "github" in value.lower()):
        #                 result["customfields"][key] = value
        #             elif isinstance(value, dict) or isinstance(value, list):
        #                 result["customfields"][key] = value
        #         except Exception as e:
        #             print(f"Failed parsing custom field {key}: {e}")

        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"✅ Jira issue details saved to {self.output_file}")
        print(self.extract_figma_links(result))
        return self.extract_figma_links(result)
        