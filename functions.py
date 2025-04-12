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
    This function is used to get the data from the excel sheet  by the attribute

    Args:
        csv_file (str): The csv file to get the data from
        attribute (list[str]): The attribute to get the data from

    Returns:
        list[list[str]]: A list containing the data for each requested attribute
    """
    import pandas as pd

    # read the data
    df = pd.read_excel("Data-startupticker.xlsx", sheet_name="Companies")

    #handeling problematic data
    df['Canton'] = df['Canton'].map(canton_map)
    df["Industry"] = df["Industry"].map(industry_map)
    df["Spin-offs"] = df['Spin-offs'].apply(lambda x: x.split(",") if isinstance(x, str) else [])
    df["City"] = df["City"].str.replace(r"\s*\([^)]*\)", "", regex=True)
    df["City"] = df["City"].apply(lambda s: s.split("/")[0].strip() if isinstance(s, str) else s)
    df["City"] = df["City"].apply(lambda x: city_map.get(x, x) if isinstance(x, str) else x)    
    
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
