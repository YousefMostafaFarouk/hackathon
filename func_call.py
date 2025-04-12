# we want a function that  column name from a csv file and return the name from the table   
import pandas as pd
from google import genai
import os
import httpx


def get_column_name_function(csv_file : str) -> list[str]:
    """
    This function is used to get the column name from the csv file

    Args:
        csv_file (str): The csv file to get the column name from

    Returns:
        list[str]: The column name from the csv file
    """
    # read the csv file
    df = pd.read_csv(csv_file)
    # get the column name
    column_names = df.columns
    return column_names.tolist()

def get_data_by_attribute_function(csv_file : str, attributes : list[str]) -> list[str]:
    """
    This function is used to get the data from the csv file by the attribute

    Args:
        csv_file (str): The csv file to get the data from
        attribute (list[str]): The attribute to get the data from

    Returns:
        list[list[str]]: A list containing the data for each requested attribute
    """
    # read the csv file
    df = pd.read_csv(csv_file)
    # get the data by the attributes
    result = []
    for attribute in attributes:
        data = df[attribute].tolist()
        result.append(data)
    return result

config = genai.types.GenerateContentConfig(tools=[get_column_name_function, get_data_by_attribute_function])

client = genai.Client(api_key=("AIzaSyB57DPx67DwuoetWePSm7eabr5Rw7U-RPE"))

contents = [genai.types.Content(role="user", parts=[genai.types.Part(text="What is the column names of 'Data-startupticker.csv' file?")])]

response = client.models.generate_content(model="gemini-2.0-flash", contents="what are the names of the columns in the 'Data-startupticker.csv' file?", config=config)

print(response.candidates[0].content.parts[0].function_call)
tool_call = response.candidates[0].content.parts[0].function_call
print(response.text)





