import pandas as pd
from pandasql import sqldf
from google import genai
import os
import functions
from functions import get_data_by_attribute_function

def write_to_html(text: str):
    """
    This function writes the text to an HTML file.
    Args:
        text (str): The text to write to the HTML file.
    Returns:
        nothing, just write the text to the html file
    """
    with open("output.html", "w") as file:
        file.write(text)


# Configuration for the client; your functions are provided as tools.
config = {
    "tools": [get_data_by_attribute_function, write_to_html ]
}

client = genai.Client(api_key="AIzaSyB57DPx67DwuoetWePSm7eabr5Rw7U-RPE")
# Example query: make sure your SQL query is valid. Here, we assume the 'df' table contains
# a column that might refer to the city or location to filter startups in Zurich.
user_prompt = input("Put in youre question: ")
with open("system_prompt.txt", "r", encoding="utf-8") as file:
    system_prompt = file.read()
response = client.models.generate_content(
    model="gemini-1.5-pro",
    contents= system_prompt+ user_prompt,
    config=config
)
#print(response)
print(response.text)
#print(response.function_response.response) #what are other thing I can use for the response other than text? 
