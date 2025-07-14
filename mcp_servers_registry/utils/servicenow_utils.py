import os


import requests
from typing import Dict, Any




class ServiceNowUtils:
    
    # Configuration
    SERVICENOW_BASE_URL = "https://dev275342.service-now.com/api/now"
    SERVICENOW_USER = os.getenv("SERVICENOW_USER", "admin")
    SERVICENOW_PASSWORD = os.getenv("SERVICENOW_PASSWORD", "hgIJzVs@W4!8")


    def _make_servicenow_request(self, endpoint: str, params: Dict[str, str] = None, method: str = "GET", data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make HTTP request to ServiceNow API
        """
        url = f"{self.SERVICENOW_BASE_URL}{endpoint}"
        auth = (self.SERVICENOW_USER, self.SERVICENOW_PASSWORD)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        try:
            if method == "GET":
                response = requests.get(url, params=params, auth=auth, headers=headers, timeout=30)
            elif method == "POST":
                response = requests.post(url, json=data, auth=auth, headers=headers, timeout=30)
            elif method == "PUT":
                response = requests.put(url, json=data, auth=auth, headers=headers, timeout=30)
            elif method == "PATCH":
                response = requests.patch(url, json=data, auth=auth, headers=headers, timeout=30)
            else:
                raise Exception(f"Unsupported HTTP method: {method}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": True, "message": str(e)}


    
    def get_servicenow_incidents(self, query: str = "active=true") -> Dict[str, Any]:
        """
        Fetch incidents from ServiceNow.
        Args:
            query: ServiceNow query string (default: active incidents)
        Returns:
            Dictionary containing incidents
        """
        endpoint = f"/table/incident"
        params = {"sysparm_query": query}
        return self._make_servicenow_request(endpoint, params=params)


    
    def create_servicenow_incident(self, short_description: str, description: str = "") -> Dict[str, Any]:
        """
        Create a new incident in ServiceNow.
        Args:
            short_description: Short description for the incident
            description: Detailed description
        Returns:
            Dictionary containing the created incident
        """
        endpoint = f"/table/incident"
        data = {"short_description": short_description, "description": description}
        return self._make_servicenow_request(endpoint, method="POST", data=data)


    def update_servicenow_incident(self, incident_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing incident in ServiceNow.
        Args:
            incident_id: The sys_id of the incident to update
            update_data: Dictionary containing fields to update (e.g., state, priority, assigned_to, etc.)
        Returns:
            Dictionary containing the updated incident
        """
        endpoint = f"/table/incident/{incident_id}"
        return self._make_servicenow_request(endpoint, method="PUT", data=update_data)


    def get_servicenow_incident_by_id(self, incident_id: str) -> Dict[str, Any]:
        """
        Get a specific incident from ServiceNow by its sys_id.
        Args:
            incident_id: The sys_id of the incident to retrieve
        Returns:
            Dictionary containing the incident details
        """
        endpoint = f"/table/incident/{incident_id}"
        return self._make_servicenow_request(endpoint)


    def servicenow_incident_add_comment(self, incident_id: str, comment: str, comment_type: str = "work_notes") -> Dict[str, Any]:
        """
        Add a comment or work note to an existing ServiceNow incident.
        Args:
            incident_id: The sys_id of the incident to add comment to
            comment: The comment text to add
            comment_type: Type of comment - either "work_notes" (internal) or "comments" (customer visible)
        Returns:
            Dictionary containing the updated incident
        """
        if comment_type not in ["work_notes", "comments"]:
            return {"error": True, "message": "comment_type must be either 'work_notes' or 'comments'"}
        
        endpoint = f"/table/incident/{incident_id}"
        update_data = {comment_type: comment}
        return self._make_servicenow_request(endpoint, method="PUT", data=update_data)


    def servicenow_resolve_incident(self, incident_id: str, resolution_notes: str, close_code: str = "Solved (Permanently)") -> Dict[str, Any]:
        """
        Resolve a ServiceNow incident by setting it to resolved state.
        Args:
            incident_id: The sys_id of the incident to resolve
            resolution_notes: Notes describing how the incident was resolved
            close_code: The close code for the incident (default: "Solved (Permanently)")
        Returns:
            Dictionary containing the updated incident
        """
        endpoint = f"/table/incident/{incident_id}"
        update_data = {
            "state": "6",  # 6 = Resolved state in ServiceNow
            "close_notes": resolution_notes,
            "close_code": close_code,
            "resolved_at": "javascript:gs.nowDateTime()",  # Current timestamp
            "work_notes": f"Incident resolved: {resolution_notes}"
        }
        return self._make_servicenow_request(endpoint, method="PUT", data=update_data)


    def check_servicenow_health(self) -> Dict[str, Any]:
        """
        Check if the ServiceNow API is reachable.
        Returns:
            Dictionary containing health status
        """
        try:
            result = self._make_servicenow_request("/stats/incident")
            if "result" in result:
                return {"status": "healthy", "details": result}
            return {"status": "unhealthy", "details": result}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}