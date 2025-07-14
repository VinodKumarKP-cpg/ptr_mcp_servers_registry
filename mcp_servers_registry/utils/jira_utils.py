import os
import base64
import requests
from typing import Dict, Any, List, Optional


class JiraUtils:
    
    # Configuration
    JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", "https://capgemini-team-jiraai.atlassian.net/rest/api/3")
    JIRA_USERNAME = os.getenv("JIRA_USERNAME", "senthil.subramanian@capgemini.com")
    JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "ATATT3xFfGF0_qS5YlWhXHfpeANaWVkz7tA-r95DYuSEa_V3mWidVOIIC68Q8NbEPFvONwvFaKDzQOGYYNQAG3VPuD-Y8IUTvCbJVO8NogAIAeuVDTNJVR2mG5SmN8a5VhNPV3acMMS0VIdyVQEY6Zq7_4q_xtZrMC11aATiE06O1-4QhOwAd3w=2FDEE297")
    

    def _get_auth_header(self) -> str:
        """
        Generate Basic Auth header for Jira API
        """
        credentials = f"{self.JIRA_USERNAME}:{self.JIRA_API_TOKEN}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded_credentials}"


    def _make_jira_request(self, endpoint: str, params: Dict[str, Any] = None, method: str = "GET", data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make HTTP request to Jira API
        """
        url = f"{self.JIRA_BASE_URL}/rest/api/3{endpoint}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": self._get_auth_header()
        }
        
        try:
            if method == "GET":
                response = requests.get(url, params=params, headers=headers, timeout=30)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == "PUT":
                response = requests.put(url, json=data, headers=headers, timeout=30)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=30)
            else:
                raise Exception(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            
            # Handle empty responses (e.g., for DELETE operations)
            if response.status_code == 204 or not response.content:
                return {"success": True, "message": "Operation completed successfully"}
            
            return response.json()
        except Exception as e:
            return {"error": True, "message": str(e)}


    def jira_get_issue(self, issue_key: str, expand: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a specific Jira issue by its key.
        Args:
            issue_key: The Jira issue key (e.g., "PROJ-123")
            expand: Optional comma-separated list of fields to expand (e.g., "comments,attachments")
        Returns:
            Dictionary containing the issue details
        """
        endpoint = f"/issue/{issue_key}"
        params = {}
        if expand:
            params["expand"] = expand
        return self._make_jira_request(endpoint, params=params)


    def jira_search(self, jql: str, max_results: int = 50, start_at: int = 0, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Search for Jira issues using JQL (Jira Query Language).
        Args:
            jql: JQL query string (e.g., "project = PROJ AND status = 'To Do'")
            max_results: Maximum number of results to return (default: 50)
            start_at: Starting index for pagination (default: 0)
            fields: Optional list of fields to include in results
        Returns:
            Dictionary containing search results
        """
        endpoint = "/search"
        data = {
            "jql": jql,
            "maxResults": max_results,
            "startAt": start_at
        }
        if fields:
            data["fields"] = fields
        return self._make_jira_request(endpoint, method="POST", data=data)


    def jira_create_issue(self, project_key: str, issue_type: str, summary: str, description: str = "", 
                         priority: Optional[str] = None, assignee: Optional[str] = None, 
                         labels: Optional[List[str]] = None, custom_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new Jira issue.
        Args:
            project_key: The project key (e.g., "PROJ")
            issue_type: Issue type name (e.g., "Bug", "Task", "Story")
            summary: Brief description of the issue
            description: Detailed description (supports Atlassian Document Format)
            priority: Priority name (e.g., "High", "Medium", "Low")
            assignee: Username or account ID of the assignee
            labels: List of labels to add to the issue
            custom_fields: Dictionary of custom field values
        Returns:
            Dictionary containing the created issue details
        """
        endpoint = "/issue"
        
        # Build issue data
        issue_data = {
            "fields": {
                "project": {"key": project_key},
                "issuetype": {"name": issue_type},
                "summary": summary
            }
        }
        
        if description:
            # Use Atlassian Document Format for description
            issue_data["fields"]["description"] = {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description
                            }
                        ]
                    }
                ]
            }
        
        if priority:
            issue_data["fields"]["priority"] = {"name": priority}
        
        if assignee:
            issue_data["fields"]["assignee"] = {"accountId": assignee}
        
        if labels:
            issue_data["fields"]["labels"] = labels
        
        if custom_fields:
            issue_data["fields"].update(custom_fields)
        
        return self._make_jira_request(endpoint, method="POST", data=issue_data)


    def jira_update_issue(self, issue_key: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing Jira issue.
        Args:
            issue_key: The Jira issue key (e.g., "PROJ-123")
            update_data: Dictionary containing fields to update
        Returns:
            Dictionary containing the result of the update operation
        """
        endpoint = f"/issue/{issue_key}"
        
        # Wrap update data in the required format
        formatted_data = {"fields": update_data}
        
        return self._make_jira_request(endpoint, method="PUT", data=formatted_data)


    def jira_transition_issue(self, issue_key: str, transition_id: str, comment: Optional[str] = None, 
                             fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Transition a Jira issue to a different status.
        Args:
            issue_key: The Jira issue key (e.g., "PROJ-123")
            transition_id: ID of the transition to perform
            comment: Optional comment to add during transition
            fields: Optional fields to update during transition
        Returns:
            Dictionary containing the result of the transition
        """
        endpoint = f"/issue/{issue_key}/transitions"
        
        transition_data = {
            "transition": {"id": transition_id}
        }
        
        if comment:
            transition_data["update"] = {
                "comment": [
                    {
                        "add": {
                            "body": {
                                "type": "doc",
                                "version": 1,
                                "content": [
                                    {
                                        "type": "paragraph",
                                        "content": [
                                            {
                                                "type": "text",
                                                "text": comment
                                            }
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                ]
            }
        
        if fields:
            transition_data["fields"] = fields
        
        return self._make_jira_request(endpoint, method="POST", data=transition_data)


    def jira_add_comment(self, issue_key: str, comment: str, visibility: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Add a comment to a Jira issue.
        Args:
            issue_key: The Jira issue key (e.g., "PROJ-123")
            comment: The comment text to add
            visibility: Optional visibility settings (e.g., {"type": "role", "value": "Administrators"})
        Returns:
            Dictionary containing the created comment details
        """
        endpoint = f"/issue/{issue_key}/comment"
        
        comment_data = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": comment
                            }
                        ]
                    }
                ]
            }
        }
        
        if visibility:
            comment_data["visibility"] = visibility
        
        return self._make_jira_request(endpoint, method="POST", data=comment_data)


    def get_jira_transitions(self, issue_key: str) -> Dict[str, Any]:
        """
        Get available transitions for a Jira issue.
        Args:
            issue_key: The Jira issue key (e.g., "PROJ-123")
        Returns:
            Dictionary containing available transitions
        """
        endpoint = f"/issue/{issue_key}/transitions"
        return self._make_jira_request(endpoint)


    def check_jira_health(self) -> Dict[str, Any]:
        """
        Check if the Jira API is reachable and credentials are valid.
        Returns:
            Dictionary containing health status
        """
        try:
            result = self._make_jira_request("/myself")
            if "accountId" in result:
                return {"status": "healthy", "user": result.get("displayName", "Unknown"), "details": result}
            return {"status": "unhealthy", "details": result}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}