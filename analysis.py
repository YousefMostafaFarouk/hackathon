import pandas as pd
from google import genai 
from google import generativeai
import sys
import os


user_prompt = ""
if not sys.stdin.isatty():  # Check if data is being piped in
    user_prompt = sys.stdin.read().strip()
else:
    user_prompt = os.environ.get('USER_QUERY', '')
    if not user_prompt:
        user_prompt = input("Put in your question: ")

def write_to_html(text: str):
    """
    This function writes the javascript code/text to an HTML file.
    Args:
        text (str): The text to write to the HTML file.
    Returns:
        nothing, just write the text to the html file
    """
    with open("react-ui/output.html", "w") as file:
        file.write(text)


def analyze_csv_with_question(question: str) -> str:
    print(question)
    """
    Analyze a CSV file and answer a specific question about its contents using the full data.
    
    Args:
        question (str): Question to ask about the data
        
    Returns:
        str: Answer to the question based on the full data
    """
    csv_path = "./Data-startupticker.csv"
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
    print(full_data_string)
    # Create context for the model, providing the full data as a string
    context = f"""

    I have a CSV file with the following columns: {columns}

    Here is the full data from the CSV file:
    ```csv
    {full_data_string}
    ```
    
    Please analyze this complete data and answer this specific question: {question}
    
    Based *only* on the data provided above, provide a detailed analysis and answer.
    IMPORTANT: DO NOT return code USE THE CODE EXECUTION TOOL. Analyze the data directly and provide a clear, text-based answer.
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
    
            
        # Get user's question
        question = user_prompt
        if not question:
            print("Error: Question cannot be empty")
            return
            
        # Get and display answer
        print("\nAnalyzing...")
        answer = analyze_csv_with_question(question)
        client = genai.Client(api_key="AIzaSyAb96T8pPwY5T7LgX3KabZWtEQFye8gBAY")
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents= answer+ "Write Chart.js code for this and output your code in the output.html file using the write_to_html function ALWAYS USE THE write_to_html function",
        )
        print(answer.text)
        print("\nAnswer:")
        print(response.text)
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()