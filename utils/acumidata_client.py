import os
from dotenv import load_dotenv
import requests
from typing import Dict, Any, Optional, Literal

# Load environment variables
load_dotenv()

class AcumidataClient:
    def __init__(self, environment: Literal["prod", "uat"] = "uat"):
        """
        Initialize the client with specified environment
        :param environment: "prod" or "uat"
        """
        self.environment = environment
        self.api_key = self._get_api_key()
        self.base_url = ("https://api.acumidata.com" 
                        if environment == "prod" 
                        else "https://uat.api.acumidata.com")
        
    def _get_api_key(self) -> str:
        """Get the appropriate API key based on environment"""
        if self.environment == "prod":
            return os.getenv("ACUMIDATA_PROD_KEY", "")
        return os.getenv("ACUMIDATA_UAT_KEY", "")

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make a GET request to the API"""
        url = f"{self.base_url}/{endpoint}"
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        if params is None:
            params = {}
        
        print("1. Starting request...")
        
        try:
            print(f"2. Making request to: {url}")
            print(f"3. With params: {params}")
            print(f"4. Headers: {headers}")
            
            print("5. Sending request...")
            response = requests.get(
                url=url,
                headers=headers,
                params=params
            )
            print("6. Got response!")
            print(f"7. Status code: {response.status_code}")
            
            if response.status_code != 200:
                print(f"8. Error response: {response.text}")
                return {"error": f"API returned status {response.status_code}"}
            
            print("9. Parsing JSON...")
            return response.json()
        
        except Exception as e:
            print(f"X. Error occurred: {str(e)}")
            return {"error": str(e)}

    def _make_post_request(self, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make a POST request to the API"""
        url = f"{self.base_url}/{endpoint}"
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        if data is None:
            data = {}
        
        print("1. Starting POST request...")
        
        try:
            print(f"2. Making POST request to: {url}")
            print(f"3. With data: {data}")
            print(f"4. Headers: {headers}")
            
            print("5. Sending POST request...")
            response = requests.post(
                url=url,
                headers=headers,
                json=data
            )
            print("6. Got response!")
            print(f"7. Status code: {response.status_code}")
            
            if response.status_code not in [200, 204]:
                print(f"8. Error response: {response.text}")
                return {"error": f"API returned status {response.status_code}"}
            
            print("9. Parsing JSON...")
            if response.status_code == 204:
                return {"message": "No content returned"}
            return response.json()
        
        except Exception as e:
            print(f"X. Error occurred: {str(e)}")
            return {"error": str(e)}

    def get_home_value(self, address: str, city: str, state: str, zip_code: str) -> Dict:
        """
        Call the Acumidata API to get home value and key property data for a given address.
        """
        endpoint = f"{self.base_url}/api/Comps/advantage"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        params = {
            "streetAddress": address,
            "city": city,
            "state": state,
            "zip": zip_code
        }
        try:
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_property_valuation(self, address: str, city: str, state: str, zip_code: str) -> dict:
        """
        Call the /api/Valuation/estimate endpoint to get property valuation data.
        """
        endpoint = "api/Valuation/estimate"
        params = {
            "streetAddress": address,
            "zip": zip_code
        }
        return self._make_request(endpoint, params)

    def get_qvm_simple(self, address: str, city: str, state: str, zip_code: str) -> dict:
        """
        Call the /api/Valuation/qvmsimple endpoint to get Quantarium QVM valuation data.
        """
        endpoint = "api/Valuation/qvmsimple"
        params = {
            "streetAddress": address,
            "zip": zip_code
        }
        return self._make_request(endpoint, params)

    def get_property_advantage(self, address: str, city: str, state: str, zip_code: str) -> dict:
        """
        Call the /api/Comps/advantage endpoint to get rich property and comparable data.
        """
        endpoint = "api/Comps/advantage"
        params = {
            "streetAddress": address,
            "city": city,
            "state": state,
            "zip": zip_code
        }
        return self._make_request(endpoint, params)

    def get_equity_advantage(self, address: str, city: str, state: str, zip_code: str) -> dict:
        """
        Call the /api/Equity/advantage endpoint to get equity calculator report.
        """
        endpoint = "api/Equity/advantage"
        params = {
            "streetAddress": address,
            "city": city,
            "state": state,
            "zip": zip_code
        }
        return self._make_request(endpoint, params)

    def get_monitors_advantage(self, address: str, city: str, state: str, zip_code: str) -> dict:
        """
        Call the /api/Monitors/advantage endpoint to create monitoring portfolio.
        """
        endpoint = "api/Monitors/advantage"
        params = {
            "streetAddress": address,
            "city": city,
            "state": state,
            "zip": zip_code
        }
        return self._make_request(endpoint, params)

    def get_comps_advantage_radius(self, address: str, city: str, state: str, zip_code: str, radius: str = "0.5") -> dict:
        """
        Call the /api/Comps/advantageradius endpoint to get comps within a radius.
        """
        endpoint = "api/Comps/advantageradius"
        params = {
            "StreetAddress": address,
            "City": city,
            "State": state,
            "Zip": zip_code,
            "Radius": radius
        }
        return self._make_request(endpoint, params)

    def get_title_advantage(self, address: str, city: str, state: str, zip_code: str) -> dict:
        """
        Call the /api/Title/advantage endpoint to get title report.
        """
        endpoint = "api/Title/advantage"
        params = {
            "streetAddress": address,
            "city": city,
            "state": state,
            "zip": zip_code
        }
        return self._make_request(endpoint, params)

    def get_valuation_advantage(self, address: str, city: str, state: str, zip_code: str) -> dict:
        """
        Call the /api/Valuation/advantage endpoint to get RELAR Full Report.
        """
        endpoint = "api/Valuation/advantage"
        params = {
            "streetAddress": address,
            "zip": zip_code
        }
        return self._make_request(endpoint, params)

    def get_valuation_simple(self, address: str, city: str, state: str, zip_code: str) -> dict:
        """
        Call the /api/Valuation/simple endpoint to get RELAR Simple Valuation Report.
        """
        endpoint = "api/Valuation/simple"
        params = {
            "streetAddress": address,
            "zip": zip_code
        }
        return self._make_request(endpoint, params)

    def get_listings_by_property(self, address: str, city: str, state: str, zip_code: str, product: str = "advantage") -> dict:
        """
        Call the /api/Listings/{product} endpoint to create listing order for property.
        """
        endpoint = f"api/Listings/{product}"
        params = {
            "streetAddress": address,
            "city": city,
            "state": state,
            "zip": zip_code
        }
        return self._make_request(endpoint, params)

    def get_listings_delta_zip(self, zip_codes: str, start_date: str = None, end_date: str = None, 
                              statuses: str = None, ref_id: str = None) -> dict:
        """
        Call the /api/Listings/delta-zip endpoint to get listings delta report by zip code.
        """
        endpoint = "api/Listings/delta-zip"
        params = {
            "zipCodes": zip_codes
        }
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        if statuses:
            params["statuses"] = statuses
        if ref_id:
            params["refId"] = ref_id
        
        return self._make_request(endpoint, params)

    def get_listings_feed(self, state: str, start_timestamp: int = None, end_timestamp: int = None, 
                         extract_type: str = None) -> dict:
        """
        Call the /api/Listings/feed endpoint to get MLS data feed.
        """
        endpoint = "api/Listings/feed"
        params = {
            "state": state
        }
        if start_timestamp:
            params["startTimeStamp"] = start_timestamp
        if end_timestamp:
            params["endTimeStamp"] = end_timestamp
        if extract_type:
            params["extractType"] = extract_type
        
        return self._make_request(endpoint, params)

    def get_comps_advantage_polygon(self, address: str, city: str, state: str, zip_code: str, 
                                   polygon: str, land_use: str = None, date: str = None, 
                                   include_birdseye: str = None) -> dict:
        """
        Call the /api/Comps/advantagepolygon endpoint to get comps within a polygon.
        """
        endpoint = "api/Comps/advantagepolygon"
        params = {
            "StreetAddress": address,
            "City": city,
            "State": state,
            "Zip": zip_code,
            "Polygon": polygon
        }
        if land_use:
            params["LandUse"] = land_use
        if date:
            params["Date"] = date
        if include_birdseye:
            params["IncludeBirdseye"] = include_birdseye
        
        return self._make_request(endpoint, params)

    def get_valuation_ranged(self, address: str, city: str, state: str, zip_code: str) -> dict:
        """
        Call the /api/Valuation/ranged endpoint to get RELAR Ranged Report.
        """
        endpoint = "api/Valuation/ranged"
        params = {
            "streetAddress": address,
            "zip": zip_code
        }
        return self._make_request(endpoint, params)

    def get_valuation_collateral(self, address: str, city: str, state: str, zip_code: str) -> dict:
        """
        Call the /api/Valuation/collateral endpoint to get Quantarium Collateral Report.
        """
        endpoint = "api/Valuation/collateral"
        params = {
            "streetAddress": address,
            "zip": zip_code
        }
        return self._make_request(endpoint, params)

    def get_listings_delta_fips(self, fips_code: str, start_date: str = None, end_date: str = None, 
                               statuses: str = None, ref_id: str = None) -> dict:
        """
        Call the /api/Listings/delta-fips endpoint to get listings delta report by FIPS code.
        """
        endpoint = "api/Listings/delta-fips"
        params = {
            "fipsCode": fips_code
        }
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        if statuses:
            params["statuses"] = statuses
        if ref_id:
            params["refId"] = ref_id
        
        return self._make_request(endpoint, params)

    def get_listings_feed_enhanced(self, state: str, page_size: int = 100, start_timestamp: int = None, 
                                  end_timestamp: int = None, extract_type: str = None, 
                                  transaction_id: int = None) -> dict:
        """
        Call the /api/Listings/feed endpoint with enhanced parameters including pagination.
        """
        endpoint = "api/Listings/feed"
        params = {
            "state": state,
            "pagesize": page_size
        }
        if start_timestamp:
            params["startTimeStamp"] = start_timestamp
        if end_timestamp:
            params["endTimeStamp"] = end_timestamp
        if extract_type:
            params["extractType"] = extract_type
        if transaction_id:
            params["transactionId"] = transaction_id
        
        return self._make_request(endpoint, params)

    def get_parcels_detail(self, address: str, city: str, state: str, zip_code: str) -> dict:
        """
        Call the /api/Parcels/detail endpoint to get simple parcel details.
        """
        endpoint = "api/Parcels/detail"
        data = {
            "streetAddress": address,
            "city": city,
            "state": state,
            "zip": zip_code
        }
        return self._make_post_request(endpoint, data)
