# we want a function that  column name from a csv file and return the name from the table   
import pandas as pd
from google import genai
import os
import httpx

get_column_name = {
    "name": "get_column_name_function",
    "description": "Get the column name from the csv file",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "csv_file": {"type": "string", "description": "The csv file to get the column name from"}
        },
        "required": ["csv_file"]
    }
}
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



config = genai.types.GenerateContentConfig(tools=[get_column_name_function])

client = genai.Client(api_key=("AIzaSyB57DPx67DwuoetWePSm7eabr5Rw7U-RPE"))

contents = [genai.types.Content(role="user", parts=[genai.types.Part(text="What is the column names of 'Data-startupticker.csv' file?")])]

response = client.models.generate_content(model="gemini-2.0-flash", contents="what are the names of the columns in the 'Data-startupticker.csv' file?", config=config)

print(response.candidates[0].content.parts[0].function_call)
tool_call = response.candidates[0].content.parts[0].function_call
print(response.text)





