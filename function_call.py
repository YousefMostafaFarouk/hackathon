import json
import pandas as pd
from pandasql import sqldf
from google import genai
import os
import sys
import functions
from functions import write_to_html, get_data_by_attribute_function, early_stage_investment_volume, get_deal_data_by_attribute


# Configuration for the client; your functions are provided as tools.
config = {
    "tools": [get_data_by_attribute_function, write_to_html, early_stage_investment_volume, get_deal_data_by_attribute]
}

client = genai.Client(api_key="AIzaSyB57DPx67DwuoetWePSm7eabr5Rw7U-RPE")

# Get user query from stdin or command line or environment variable
user_prompt = ""
if not sys.stdin.isatty():  # Check if data is being piped in
    user_prompt = sys.stdin.read().strip()
else:
    user_prompt = os.environ.get('USER_QUERY', '')
    if not user_prompt:
        user_prompt = input("Put in your question: ")

try:
    # Get current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    system_prompt_path = os.path.join(script_dir, "alt_prompt.txt")
    
    # Check if file exists in current directory
    if not os.path.exists(system_prompt_path):
        print(f"System prompt not found at {system_prompt_path}, checking react-ui directory...")
        # Try react-ui directory as fallback
        system_prompt_path = os.path.join(script_dir, "react-ui", "system_prompt.txt")
        
    # If still not found, try absolute path
    if not os.path.exists(system_prompt_path):
        print(f"System prompt not found at {system_prompt_path}, trying one more location...")
        # Try one more location
        system_prompt_path = os.path.abspath("system_prompt.txt")
        
    # Final check
    if not os.path.exists(system_prompt_path):
        print(f"Error: System prompt file not found at any location. Last tried: {system_prompt_path}")
        sys.exit(1)
    
    print(f"Using system prompt from: {system_prompt_path}")
    with open(system_prompt_path, "r", encoding="utf-8") as file:
        system_prompt = file.read()
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=system_prompt +"\n \n \n and now comes the user prompt: \n" + user_prompt,
        config=config
    )
    
    print(response.text)
except Exception as e:
    print(f"Error: {str(e)}")
    sys.exit(1)

