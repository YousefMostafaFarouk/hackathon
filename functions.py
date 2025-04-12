import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

#maps to clean the data
canton_map = {
    "Zürich": "ZH", "ZH": "ZH", "Winterthur": "ZH",
    "Bern": "BE", "BE": "BE",
    "Luzern": "LU", "Lucerne": "LU", "LU": "LU",
    "Uri": "UR", "UR": "UR",
    "Schwyz": "SZ", "SZ": "SZ",
    "Obwalden": "OW", "OW": "OW",
    "Nidwalden": "NW", "NW": "NW",
    "Glarus": "GL", "GL": "GL",
    "Zug": "ZG", "ZG": "ZG",
    "Fribourg": "FR", "Freibourg": "FR", "Fribourg / Freiburg": "FR", "FR": "FR",
    "Solothurn": "SO", "SO": "SO",
    "Basel-Stadt": "BS", "BS": "BS",
    "Basel-Landschaft": "BL", "BL": "BL",
    "Schaffhausen": "SH", "SH": "SH",
    "Appenzell Innerrhoden": "AI", "AI": "AI",
    "Appenzell Ausserrhoden": "AR", "AR": "AR",
    "St. Gallen": "SG", "SG": "SG",
    "Graubünden": "GR", "GR": "GR",
    "Aargau": "AG", "AG": "AG",
    "Thurgau": "TG", "TG": "TG",
    "Ticino": "TI", "TI": "TI",
    "Vaud": "VD", "VD": "VD", "Lausanne": "VD",
    "Valais": "VS", "Wallis": "VS", "Valais / Wallis": "VS", "VS": "VS",
    "Neuchâtel": "NE", "NE": "NE",
    "Genève": "GE", "GE": "GE",
    "Jura": "JU", "JU": "JU",
    "Zentralschweiz: Luzern, Uri, Schwyz, Ob‐ und Nidwalden": "LU",
    "Abroad": "ABROAD"
}
industry_map = {
    "biotech": "Biotech",
    "cleantech": "Cleantech",
    "ICT": "ICT",
    "ICT (fintech)": "ICT",
    "healthcare IT": "Medtech",
    "medtech": "Medtech",
    "Life-Sciences": "Biotech",
    "micro / nano": "Micro/Nano",
    "consumer products": "Consumer Products",
    "Impact": "Impact",
    "Deep Tech": "Other",
    "Interdisciplinary": "Other"
}
city_map = {
    "Fribourg": "Freiburg",
    "Bienne": "Biel",
    "Lucerne": "Luzern",
    "Genève": "Genf",
    "Neuchâtel": "Neuenburg",
    "Sankt Gallen": "St. Gallen",
    "St Gallen": "St. Gallen",
    "Gallen": "St. Gallen",
    "Sion": "Sitten",
    "Tumegl": "Tomils",
    "Zurich": "Zürich"
}

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

def get_company_df():
    # read the data
    df = pd.read_excel("Data-startupticker.xlsx", sheet_name="Companies")

    #handeling problematic data
    df['Canton'] = df['Canton'].map(canton_map)
    df["Industry"] = df["Industry"].map(industry_map)
    df["Spin-offs"] = df['Spin-offs'].apply(lambda x: x.split(",") if isinstance(x, str) else [])
    df["City"] = df["City"].str.replace(r"\s*\([^)]*\)", "", regex=True)
    df["City"] = df["City"].apply(lambda s: s.split("/")[0].strip() if isinstance(s, str) else s)
    df["City"] = df["City"].apply(lambda x: city_map.get(x, x) if isinstance(x, str) else x)  #

    return df

def get_data_by_attribute_function(Code : str,
                                   Title : str,
                                   Industry : str,
                                   Canton : str,
                                   Spin_offs : str,
                                   City : str,
                                   Year : int,
                                   CEO_Gender : str,
                                   OOB : int,
                                   sort_by : str,
                                   Funded : int) -> dict:
    """
    Retrieves filtered company data from the 'Companies' sheet of the Excel file based on the provided attributes.

    Args:
        Code (str): Unique identifier for the company. Use an empty string ("") to ignore.
        Title (str): Company name. Use an empty string ("") to ignore.
        Industry (str): Industry name (e.g., "Biotech"). Use an empty string ("") to ignore.
        Canton (str): Two-letter Swiss canton code (e.g., "ZH"). Use an empty string ("") to ignore.
        Spin_offs (str): Spin-off institution (e.g., "ETH"). Use an empty string ("") to ignore.
        City (str): Company location. Use an empty string ("") to ignore.
        Year (int): Founding year. Use -1 to ignore.
        CEO_Gender (str): Gender of the CEO ("M", "F", or other). Use an empty string ("") to ignore.
        OOB (int): Out-of-business status. 1 = True, 0 = False, -1 = ignore.
        Funded (int): Funding status. 1 = funded, 0 = not funded, -1 = ignore.
        sort_by (str): Column name to sort the results by. Use "Year" to ignore.

    Returns:
        dict: A dict, representing the companies that matche all given filters.
    """
    import pandas as pd

    # read the data
    df = get_company_df()
    
    # get the data by the attribute
    features = {
        "Code": Code,
        "Title": Title,
        "City": City,
        "Industry": Industry,
        "Canton": Canton,
        "Year": Year,
        "Gender CEO": CEO_Gender,
        "OOB": OOB,
        "Funded": Funded,
    }
    features = pd.Series(features)
    features = features[features != ""]
    features = features[features != -1]

    # filter the data by the attributes
    if Spin_offs != "":
        df = df[df["Spin-offs"].apply(lambda lst: isinstance(lst, list) and Spin_offs in lst)]
    df = df[(df[list(features.index)] == features).all(axis=1)].fillna(-1).sort_values(by=sort_by, ascending=False)
    return df.head(20).to_dict(orient="records")


def get_deal_data_by_attribute(id: str,
                  investor: str,
                  min_amount: int,
                  max_amount: int,
                  confidential: int,
                  min_valuation: int,
                  max_valuation: int,
                  time_start: str,
                  time_end: str,
                  type: str,
                  phase: str,
                  canton: str,
                  company: str,
                  ceo_gender: str,
                  industry : str, 
                  City : str,
                  sort_by: str
                  ) -> dict:
    """
    Filters and returns deal entries from the startup dataset based on investor name, financial thresholds, time range, and company attributes.

    This function merges deal data with company metadata, standardizes canton names, and applies a flexible set of filters.
    String-based attributes (e.g. company name, phase, gender) can be ignored by passing an empty string `""`. 
    Numerical filters (e.g. funding amount, valuation) can be skipped by passing `-1`.

    Args:
        id (str): Exact deal ID to filter by. Use "" to ignore.
        investor (str): Investor name or regex pattern to match in the 'Investors' column. Case-insensitive.
        min_amount (int): Minimum funding amount. Use -1 to ignore.
        max_amount (int): Maximum funding amount. Use -1 to ignore.
        confidential (int): 1 for confidential deals, 0 for public, -1 to ignore.
        min_valuation (int): Minimum company valuation. Use -1 to ignore.
        max_valuation (int): Maximum company valuation. Use -1 to ignore.
        time_start (str): Start date in string format (e.g. "2022-01-01"). Use "" to ignore.
        time_end (str): End date in string format. Use "" to ignore.
        type (str): Deal type (e.g. "Equity", "Grant"). Use "" to ignore.
        phase (str): Startup phase (e.g. "Seed", "Early Stage", "Later Stage"). Use "" to ignore.
        canton (str): Two-letter Swiss canton code (e.g. "ZH"). Use "" to ignore.
        company (str): Company name. Use "" to ignore.
        ceo_gender (str): Gender of the CEO ("Male", "Female", etc.). Use "" to ignore.
        sort_by (str): Column name to sort the results by. Use "Valuation" to ignore.
        industry : str, company industry (e.g. "Biotech"). Use "" to ignore.
        City : str, company location. Use "" to ignore.

    Returns:
        dict: A filtered dict containing all deals that match the given criteria.
    """
    df_deal = pd.read_excel("Data-startupticker.xlsx", sheet_name="Deals")
    df_comp = get_company_df()
    df_comp_subset = df_comp[['Title', 'Industry', 'City']].copy()
    df_deal = df_deal.merge(df_comp_subset, left_on='Company', right_on='Title', how='left')
    df_deal['Canton'] = df_deal['Canton'].map(canton_map)

    #filter for investors
    if investor != "":
        mask = df_deal["Investors"].astype(str).str.contains(investor, case=False, regex=True, na=False)
        df_deal = df_deal[mask]
    
    #filter for discret features
    features = {'Id': id, 'Investor': investor,  'Confidential': confidential,   'Type': type, 'Phase': phase, 'Canton': canton, 'Company': company, 'Gender CEO': ceo_gender, 'Industry': industry, 'City': City}
    features = pd.Series(features)
    features = features[features != ""]
    features = features[features != -1]
    mask = (df_deal[list(features.index)] == features).all(axis=1)
    df_deal = df_deal[mask]

    #filter for continuous features
    if min_amount != -1:
        df_deal = df_deal[df_deal['Amount'] >= min_amount]
    if max_amount != -1:
        df_deal = df_deal[df_deal['Amount'] <= max_amount]
    if min_valuation != -1:
        df_deal = df_deal[df_deal['Valuation'] >= min_valuation]
    if max_valuation != -1:
        df_deal = df_deal[df_deal['Valuation'] <= max_valuation]
    if time_start != "":
        df_deal = df_deal[pd.to_datetime(df_deal['Date of the funding round']) >= pd.to_datetime(time_start)]
    if time_end != "":
        df_deal = df_deal[pd.to_datetime(df_deal['Date of the funding round']) <= pd.to_datetime(time_end)]
    df_deal = df_deal.fillna(-1).sort_values(by=sort_by, ascending=False)
    return df_deal.head(20).to_dict(orient="records")


def early_stage_investment_volume(Industry : str) -> float:
    """
    This function is used to get the early stage investment volume by industry
    Args:
        Industry (str): The industry to get the investment volume from
    Returns:
        float: The investment volume
    """
    import numpy as np
    df_deal = pd.read_excel("Data-startupticker.xlsx", sheet_name="Deals")
    df_comp = get_company_df()
    df_comp_subset = df_comp[['Title', 'Industry', 'Vertical', 'City']].copy()
    df_deal = df_deal.merge(df_comp_subset, left_on='Company', right_on='Title', how='left')

    if Industry != "":
        df_deal = df_deal[df_deal["Industry"] == Industry]
    df_deal = df_deal[(df_deal['Phase'] == 'Early Stage') | (df_deal['Phase'] == 'Seed')]
    return np.sum(df_deal['Amount'])


def custom_sum(data: str, feature: str) -> float:
    """
    Calculates the sum of a specific numerical column from JSON-formatted data.

    Args:
        data (str): A JSON string representing a list of records (e.g., '[{"amount": 10}, {"amount": 20}]').
        feature (str): The key/column name whose values should be summed.

    Returns:
        float: The total sum of all values under the specified feature.
    """
    df = pd.read_json(data).astype(float)
    df = df[df != -1].astype(float)
    if len(df.columns) == 1:
        return float(df.sum())
    return df[feature].astype(float).sum()

def custom_mean(data: str, feature: str) -> float:
    """
    Calculates the mean (average) of a specific numerical column from JSON-formatted data.

    Args:
        data (str): A JSON string representing a list of records (e.g., '[{"amount": 10}, {"amount": 20}]').
        feature (str): The key/column name whose values should be averaged.

    Returns:
        float: The mean of all values under the specified feature.
    """
    df = pd.read_json(data).astype(float)
    df = df[df != -1].astype(float)
    if len(df.columns) == 1:
        return float(df.mean())
    return float(df[feature].mean())

def custom_count(data: str, feature: str) -> int:
    """
    Counts the number of non-missing entries in a specific column from JSON-formatted data.

    Args:
        data (str): A JSON string representing a list of records (e.g., '[{"amount": 10}, {"amount": 20}]').
        feature (str): The key/column name whose non-missing values should be counted.

    Returns:
        int: The number of valid entries in the specified feature column.
    """
    df = pd.read_json(data).astype(float)
    df = df[df != -1]
    if len(df.columns) == 1:
        return int(df.count())
    return int(df[feature].count())


def get_company_feature(feature: str) -> str:
    """
    Retrieves a specific feature (column) from the company dataset.

    Args:
        feature (str): The name of the feature/column to retrieve.

    Returns:
        str: A json string containing the values of the specified feature.
    """
    df = get_company_df()
    return df[feature].astype(str).fillna(-1).replace("", -1).to_json(orient="records")

def get_deal_feature(feature: str) -> pd.DataFrame:
    """
    Retrieves a specific feature (column) from the deal dataset.

    Args:
        feature (str): The name of the feature/column to retrieve.

    Returns:
        pd.Dataframe: A dataframe containing the values of the specified feature.
    """
    df = pd.read_excel("Data-startupticker.xlsx", sheet_name="Deals")
    return df[feature].astype(str).fillna(-1).replace("", -1).to_json(orient="records")

test = get_data_by_attribute_function(
    Code="",
    Title="",
    Industry="Biotech",
    Canton="ZH",
    Spin_offs="ETH",
    City="Zürich",
    Year=-1,
    CEO_Gender="",
    OOB=-1,
    sort_by="Year",
    Funded=1
)
