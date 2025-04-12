import json
import pandas as pd
import google.generativeai as genai
# I want to fetch the data from the excel file and return a list of dictionaries
def fetchCompanyData():
    df = pd.read_excel("Data-startupticker.xlsx", sheet_name="Companies")
    df = df.astype(str)
    return df.fillna("").to_dict(orient="records")

def fetchDealData():
    df = pd.read_excel("Data-startupticker.xlsx", sheet_name="Deals")
    df = df.astype(str)
    return df.fillna("").to_dict(orient="records")

# Initialize Gemini
genai.configure(api_key="AIzaSyAbIqSSiCZZEa5SMqVQ43ut6q30nKOhcvQ")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-2.0-flash")

def ask_gemini(question: str):
    companies = fetchCompanyData()
    deals = fetchDealData()

    companies_sample = companies[:30]
    deals_sample = deals[:30]

    with open("prompt.txt", "r") as file:
        prompt_template = file.read()

    prompt = prompt_template.format(
        companies=json.dumps(companies_sample),
        deals=json.dumps(deals_sample),
        question=question
    )

    response = model.generate_content(prompt)
    print(response.text.strip())

if __name__ == "__main__":
    user_question = input("Enter your question: ")
    ask_gemini(user_question)