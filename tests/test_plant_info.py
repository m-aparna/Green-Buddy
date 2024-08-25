import pytest
from unittest.mock import patch
from app.utils.plant_info import Plant_Basic_Info
import random

class TestPlantBasicInfo:
    
    # Setup method to initialize the Plant_Basic_Info instance for each test
    def setup_method(self):
        api_keys = ["sk-azQu66ca230abfb3c6610", "sk-WwDa66ca273804e396611", "sk-VFO966ca27c2606466612", "sk-UjRY66ca2860d18ed6613"]
        self.neem_info = Plant_Basic_Info(name="neem", api_key=random.choice(api_keys))
    
    #Tests if the plant_id method correctly retrieves the plant ID.
    def test_plant_id_retrievel(self):
        # Mock response for a successful plant ID retrieval
        mock_response = {
            "data": [
                {"id": 1155, "common_name": "neem"}
            ]
        }
        with patch("requests.get") as Mock:
            Mock.return_value.json.return_value = mock_response
            Mock.return_value.status_code = 200
            plant_id = self.neem_info.plant_id()
            assert plant_id == 1155  # Check that the returned ID is correct

    # Test if the plant not found, plant_id method return None
    def test_plant_id_not_retrievel(self):
        mock_response = {"data": []}
        with patch("requests.get") as Mock:
            Mock.return_value.json.return_value = mock_response
            Mock.return_value.status_code = 200
            plant_id = self.neem_info.plant_id()
            assert plant_id is None  # Check that None is returned when no plant is found
    
    def test_plant_id_request_error(self):
        # Mock an exception during the API call
        with patch("requests.get", side_effect=Exception("Connection error")):
            plant_id = self.neem_info.plant_id()
            assert plant_id is None  # Check that None is returned when an exception occurs

    # Test if the basic_details method correctly retrieves the plant details
    @patch("requests.get")
    def test_basic_details_success(self, Mock):
        # Mock the API response for a successful plant details retrieval
        successfull_mock_response = {
            "common_name": "Neem",
            "scientific_name": "Azadirachta indica",
            "other_name": [],
            "family": "Meliaceae",
            "origin": "India Nepal Pakistan Bangladesh and Sri Lanka",
            "type": "Broadleaf evergreen",
            "description": "The neem tree (Azadirachta indica) is an amazing species of tree.",
            "default_image": {"original_url": "https://perenual.com/storage/species_image/1155_azadirachta_indica/og/31761735438_24132d574f_b.jpg"}        
        }
        Mock.return_value.json.return_value = successfull_mock_response
        Mock.return_value.status_code = 200
        
        # Call the method
        details = self.neem_info.basic_details()
        
        # Assert the returned details match the expected result
        assert details == [
            "Neem", "Azadirachta indica", [], "Meliaceae",
            "India Nepal Pakistan Bangladesh and Sri Lanka", "Broadleaf evergreen",
            "The neem tree (Azadirachta indica) is an amazing species of tree.",
            "https://perenual.com/storage/species_image/1155_azadirachta_indica/og/31761735438_24132d574f_b.jpg"
        ]

    @patch("requests.get") # It instructs the test framework to substitute the requests.get method with a mock object for the duration of this test method
    def test_basic_details_empty(self, Mock):
        # Mock the API response with missing fields
        mock_response = {}
        Mock.return_value.json.return_value = mock_response
        Mock.return_value.status_code = 200
        
        # Call the method
        basic_details = self.neem_info.basic_details()
        
        # Assert the returned details are all default values
        assert basic_details == ['N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']

    def test_basic_details_request_error(self):
        # Mock an exception during the API call
        with patch("requests.get", side_effect=Exception("Connection error")):
            details = self.neem_info.basic_details()
            assert details is None  # Check that None is returned when an exception occurs