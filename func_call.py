import pandas as pd
from pandasql import sqldf
from google import genai
import os
import httpx

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


def get_column_name_function(csv_file: str) -> list[str]:
    """
    This function gets the column names from the CSV file.

    Args:
        csv_file (str): The CSV file to get the column names from.

    Returns:
        list[str]: A list of column names from the CSV file.
    """
    # Read the CSV file
    df = pd.read_csv(csv_file)
    # Get the column names and return them as a list
    return df.columns.tolist()

def query_csv_with_pandasql(csv_file: str, sql_query: str) -> dict:
    """
    This function queries the CSV file with the SQL query and returns both column names and results.

    Args:
        csv_file (str): The CSV file to query.
        sql_query (str): The SQL query for filtering the CSV file.

    Returns:
        dict: A dictionary containing:
            - 'columns': list of column names
            - 'results': list of dictionaries containing the query results
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Get column names using the existing function
    column_names = get_column_name_function(csv_file)
    
    # Set up a lambda for pandasql which restricts the scope to the DataFrame
    pysqldf = lambda q: sqldf(q, {"df": df})
    
    # Execute the SQL query
    result_df = pysqldf(sql_query)
    
    # Convert the result DataFrame into a list of dictionaries
    results = result_df.to_dict(orient='records')
    
    return {
        "columns": column_names,
        "results": results
    }

# Configuration for the client; your functions are provided as tools.
config = {
    "tools": [get_column_name_function, query_csv_with_pandasql, write_to_html],
    "system_instruction": " using csv file name = 'Data-startupticker.csv' the name of the table is df, Present your answers in an html file called output.html and use canvasjs to make charts that supports your answer if possible  "
}

client = genai.Client(api_key="AIzaSyB57DPx67DwuoetWePSm7eabr5Rw7U-RPE")

# Example query: make sure your SQL query is valid. Here, we assume the 'df' table contains
# a column that might refer to the city or location to filter startups in Zurich.
prompt = input("")
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents= "make sure to use get_column_name_function first to know the column names "+prompt,
    config=config
)
#print(response)
print(response.text)
#print(response.function_response.response) #what are other thing I can use for the response other than text? 
