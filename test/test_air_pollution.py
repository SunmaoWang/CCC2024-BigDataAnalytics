import unittest
import requests
from unittest.mock import patch

class HTTPSession:
    def __init__(self, protocol, hostname, port):
        self.session = requests.Session()
        self.base_url = f'{protocol}://{hostname}:{port}'

    def get(self, path):
        return self.session.get(f'{self.base_url}{path}')

    def post(self, path, data):
        return self.session.post(f'{self.base_url}{path}', json=data)

    def put(self, path, data):
        return self.session.put(f'{self.base_url}{path}', json=data)

    def delete(self, path):
        return self.session.delete(f'{self.base_url}{path}')

class TestAirPolFunction(unittest.TestCase):

    def setUp(self):
        self.test_request = HTTPSession('http', 'localhost', 9090)

    @patch('requests.get')
    def test_get_all_environmental_data(self, mock_get):
        print("Running test_get_all_environmental_data")
        
        # Mock response from the function
        mock_response = [
            {
                "siteID": "c69ed768-34d2-4d72-86f3-088c250758a8",
                "siteName": "Alphington",
                "lga_code": "21890",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        145.0306,
                        -37.7784081
                    ]
                },
                "parameters": [
                    {
                        "name": "SO2",
                        "timeSeriesReadings": [
                            {
                                "timeSeriesName": "1HR_AV",
                                "readings": [
                                    {
                                        "since": "2024-05-15T17:00:00.000Z",
                                        "until": "2024-05-15T18:00:00.000Z",
                                        "averageValue": 0.41,
                                        "unit": "ppb",
                                        "confidence": 108,
                                        "totalSample": 13,
                                        "healthAdvice": "Good",
                                        "healthAdviceColor": "#42A93C",
                                        "healthCode": "1011"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "siteID": "ee780b50-0240-4c7e-99f8-0df759caf3a3",
                "siteName": "Churchill",
                "lga_code": "23810",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        146.414932,
                        -38.3043137
                    ]
                },
                "parameters": [
                    {
                        "name": "PM10",
                        "timeSeriesReadings": [
                            {
                                "timeSeriesName": "1HR_AV",
                                "readings": [
                                    {
                                        "since": "2024-05-15T17:00:00.000Z",
                                        "until": "2024-05-15T18:00:00.000Z",
                                        "averageValue": 14.72,
                                        "unit": "&micro;g/m&sup3;",
                                        "confidence": 108,
                                        "totalSample": 13,
                                        "healthAdvice": "Good",
                                        "healthAdviceColor": "#42A93C",
                                        "healthCode": "1016"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        response = self.test_request.get('/airpol')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print("Received data:", data)
        
        expected_data = [
            {
                "siteID": "c69ed768-34d2-4d72-86f3-088c250758a8",
                "siteName": "Alphington",
                "lga_code": "21890"
            },
            {
                "siteID": "ee780b50-0240-4c7e-99f8-0df759caf3a3",
                "siteName": "Churchill",
                "lga_code": "23810"
            }
        ]
        # Extract only the siteID, siteName, and lga_code fields from the response data
        extracted_data = [{"siteID": site["siteID"], "siteName": site["siteName"], "lga_code": site["lga_code"]} for site in data[:2]] # limit to 2 sites for comparison
        self.assertEqual(extracted_data, expected_data)

    @patch('requests.get')
    def test_get_specific_environmental_data(self, mock_get):
        print("Running test_get_specific_environmental_data")
        
        # Mock response from the function
        mock_response = [
            {
                "siteID": "c69ed768-34d2-4d72-86f3-088c250758a8",
                "siteName": "Alphington",
                "lga_code": "21890",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        145.0306,
                        -37.7784081
                    ]
                },
                "parameters": [
                    {
                        "name": "SO2",
                        "timeSeriesReadings": [
                            {
                                "timeSeriesName": "1HR_AV",
                                "readings": [
                                    {
                                        "since": "2024-05-15T17:00:00.000Z",
                                        "until": "2024-05-15T18:00:00.000Z",
                                        "averageValue": 0.41,
                                        "unit": "ppb",
                                        "confidence": 108,
                                        "totalSample": 13,
                                        "healthAdvice": "Good",
                                        "healthAdviceColor": "#42A93C",
                                        "healthCode": "1011"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        response = self.test_request.get('/airpol?lga_code=21890')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print("Received data:", data)
        
        expected_data = [
            {
                "siteID": "c69ed768-34d2-4d72-86f3-088c250758a8",
                "siteName": "Alphington",
                "lga_code": "21890"
            }
        ]
        # Extract only the siteID, siteName, and lga_code fields from the response data
        extracted_data = [{"siteID": site["siteID"], "siteName": site["siteName"], "lga_code": site["lga_code"]} for site in data]
        self.assertEqual(extracted_data, expected_data)

if __name__ == '__main__':
    unittest.main()
