import enum
from typing import Any, Optional
import requests as re
import os
import time


class HttpMethods(enum.Enum):

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class APIHandler:

    virusTotalUrlScanEndpoint = "https://www.virustotal.com/api/v3/urls"
    virusTotalUrlAnalysesEndpoint = "https://www.virustotal.com/api/v3/analyses"
    virusTotalApiKey = os.getenv("VIRUS_TOTAL_API_KEY")

    def _makeRequest(
        self,
        url: str,
        method: HttpMethods,
        data: Optional[Any] = None,
        headers: Optional[Any] = None,
    ):

        try:
            response = None
            if method.value == "GET":
                response = re.get(url=url, headers=headers)
            elif method.value == "POST":
                response = re.post(url=url, data=data, headers=headers)
            elif method.value == "PUT":
                response = re.put(url=url, data=data, headers=headers)
            elif method.value == "DELETE":
                response = re.delete(url=url, data=data, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method.value}")

            return response

        except Exception as e:
            print("Error in _makeRequest")
            print(e)

    def checkSecureUrl(self, url: str):

        urlScanResponse = self._makeRequest(
            self.virusTotalUrlScanEndpoint,
            HttpMethods.POST,
            data={"url": url},
            headers={"x-apikey": self.virusTotalApiKey},
        )

        if urlScanResponse and urlScanResponse.status_code >= 400:
            print("Error in scanning url")
            print(urlScanResponse)
            return None
        elif urlScanResponse:
            jsonResponse = urlScanResponse.json()
            print(jsonResponse)
            id = jsonResponse["data"]["id"]
            scanReportResponse = self._makeRequest(
                f"{self.virusTotalUrlAnalysesEndpoint}/{id}",
                HttpMethods.GET,
                headers={"x-apikey": self.virusTotalApiKey},
            )

            if scanReportResponse and scanReportResponse.status_code >= 400:
                print("Error in getting scan report")
                print(scanReportResponse)
                return None

            while True:
                if scanReportResponse:
                    scanReport = scanReportResponse.json()
                    status = scanReport["data"]["attributes"]["status"]
                    if status == "completed":
                        return scanReport["data"]["attributes"]["stats"]
                    elif status == "queued":
                        time.sleep(1)
                    else:
                        print("Some error occured in fetching scan results")
                        print(scanReport)
                        return None
