import json
import pandas as pd
from pandasql import sqldf
from google import genai
import os
import functions
from functions import write_to_html, get_data_by_attribute_function, early_stage_investment_volume, get_deal_data_by_attribute



# Configuration for the client; your functions are provided as tools.
config = {
    "tools": [get_data_by_attribute_function, write_to_html, early_stage_investment_volume, get_deal_data_by_attribute]
}

client = genai.Client(api_key="AIzaSyAbIqSSiCZZEa5SMqVQ43ut6q30nKOhcvQ")

user_prompt = input("Put in youre question: ")
with open("/Users/leifmaurer/Documents/Programmieren/swisshacks/hackathon/system_prompt.txt", "r", encoding="utf-8") as file:
    system_prompt = file.read()
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents= system_prompt + "\n \n \n and now comes the user prompt: \n" + user_prompt,
    config=config
)
print(response.text)
