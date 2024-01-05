"""
This module contains test cases for the app.py module.
It includes tests for functions that process uploaded image files and handle image data.
"""

import pytest
from app import input_image_setup

class MockUploadedFile:
    """
    Mock class for simulating an UploadedFile as expected by Streamlit file uploader.
    This class mimics the necessary methods and attributes of an UploadedFile object.
    """
    # pylint: disable=R0903
    def __init__(self, data, file_type):
        """
        Initialize the mock uploaded file with specified data and file type.

        Args:
            data (bytes): The byte data representing the file content.
            file_type (str): The MIME type of the file.
        """
        self.data = data
        self.type = file_type

    def getvalue(self):
        """
        Return the byte data of the file.

        Returns:
            bytes: The byte data of the file.
        """
        return self.data

def test_input_image_setup():
    """
    Test the input_image_setup function with a mock uploaded file.
    This test checks if the function correctly processes the mock file and 
    returns the expected format.
    """
    # Create a mock uploaded file
    mock_file = MockUploadedFile(b"fake image data", "image/jpeg")

    # Call the function with the mock file
    result = input_image_setup(mock_file)

    # Assert the expected outcome
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]['mime_type'] == "image/jpeg"
    assert result[0]['data'] == b"fake image data"

def test_input_image_setup_no_file():
    """
    Test the input_image_setup function with no file uploaded.
    This test checks if the function raises a FileNotFoundError when no file is provided.
    """
    with pytest.raises(FileNotFoundError):
        input_image_setup(None)
