import os


import requests
from typing import Dict, Any




class ServiceNowUtils:
    
    # Configuration
    SERVICENOW_BASE_URL = "https://dev203813.service-now.com/api/now"
    SERVICENOW_USER = os.getenv("SERVICENOW_USER", "admin")
    SERVICENOW_PASSWORD = os.getenv("SERVICENOW_PASSWORD", "Pc8KAa$j0z-W")


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
        return self.__dict___make_servicenow_request(endpoint, method="POST", data=data)


   
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