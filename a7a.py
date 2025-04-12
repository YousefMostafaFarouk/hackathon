import pandas as pd
from google import genai 
from google import generativeai
import os


def write_to_html(text: str):
    """
    This function writes the javascript code/text to an HTML file.
    Args:
        text (str): The text to write to the HTML file.
    Returns:
        nothing, just write the text to the html file
    """
    with open("output.html", "w") as file:
        file.write(text)


def analyze_csv_with_question(csv_path: str, question: str) -> str:
    """
    Analyze a CSV file and answer a specific question about its contents using the full data.
    
    Args:
        csv_path (str): Path to the CSV file
        question (str): Question to ask about the data
        
    Returns:
        str: Answer to the question based on the full data
    """
    
    print("Reading first 1000 rows...")
    # Read the first 1000 rows of the CSV
    try:
        df = pd.read_csv(csv_path, nrows=500)
    except FileNotFoundError:
        return f"Error: CSV file not found at '{csv_path}'"
    except pd.errors.EmptyDataError:
        return f"Error: The CSV file at '{csv_path}' is empty."
    except Exception as read_err:
        return f"Error reading CSV file: {read_err}"
    
    # Convert the entire DataFrame to a string
    # Note: This might be very large for huge CSV files and could hit context limits.
    # Consider summarizing or sampling if necessary for extremely large files.
    full_data_string = df.to_string()
    
    # Get column names
    columns = df.columns.tolist()
    
    # Create context for the model, providing the full data as a string
    context = f"""
    I have a CSV file with the following columns: {columns}

    Here is the full data from the CSV file:
    ```csv
    {full_data_string}
    ```
    
    Please analyze this complete data and answer this specific question: {question}
    
    Based *only* on the data provided above, provide a detailed analysis and answer.
    IMPORTANT: Do not return code. Analyze the data directly and provide a clear, text-based answer.
    Include specific numbers and insights derived from the complete data in your response.
    """
    client = genai.Client(api_key="AIzaSyAb96T8pPwY5T7LgX3KabZWtEQFye8gBAY")
    response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=context,
    config=genai.types.GenerateContentConfig(
        tools=[genai.types.Tool(
        code_execution=genai.types.ToolCodeExecution
        )]
    )
    )         
 
    return response.text
        


config = {
    "tools": [ write_to_html ]
}

def main():
    """Main function to handle user interaction."""
    try:
        # Get CSV file path
        csv_path = input("Enter the path to your CSV file: ").strip()
        if not os.path.exists(csv_path):
            print(f"Error: File not found at {csv_path}")
            return
            
        # Get user's question
        question = input("\nWhat would you like to know about the data? ").strip()
        if not question:
            print("Error: Question cannot be empty")
            return
            
        # Get and display answer
        print("\nAnalyzing...")
        answer = analyze_csv_with_question(csv_path, question)
        client = genai.Client(api_key="AIzaSyAb96T8pPwY5T7LgX3KabZWtEQFye8gBAY")
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents= answer+ "You are a helpful assistant that can write canvas.js javascript code to make the data interactive and write the code to an html file (output.html) you don't need to ask for permission PLEASE USE THE write_to_html_function NEVER output the code in the answer",
            config=config
        )
        print(answer)
        print("\nAnswer:")
        print(response.text)
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()