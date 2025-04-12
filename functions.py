import pandas as pd
import numpy as np

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
                                   Funded : int) -> list[str]:
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

    Returns:
        list[dict]: A list of dictionaries, each representing a company that matches all given filters.
    """
    import pandas as pd

    # read the data
    df = pd.read_excel("Data-startupticker.xlsx", sheet_name="Companies")

    df = get_company_df
    
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
    df = df[(df[list(features.index)] == features).all(axis=1)].fillna("null")
    return df.to_dict(orient="records")


def early_stage_investment_volume(Industry) -> float:
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
early_stage_investment_volume()

