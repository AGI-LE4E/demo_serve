import json

import pandas as pd
from langchain_core.tools import tool

COLUMNS = ["title", "address", "latitude", "longitude", "phoneno", "repPhoto"]


@tool
def find_location_by_keyword_from_csv(
    keywords: str,
    category: str,
) -> str:
    """Find the location from the keyword.

    Args:
        keyword (str): The keyword to search for.

    Returns:
        str: The location found from the keyword.
    """
    print(keywords, category)
    if "," in keywords:
        keyword_list = [keyword.strip() for keyword in keywords.split(" ")]
    elif " " in keywords:
        keyword_list = [keyword.strip() for keyword in keywords.split(" ")]
    else:
        keyword_list = [keywords.strip()]

    keyword_list = [
        word for word in keyword_list if word != "제주도" and word != "맛집"
    ]

    for keyword in keyword_list:

        df = (
            pd.read_csv("data/visit_jeju_csv_restaurant.csv")
            if category == "RESTAURANT"
            else pd.read_csv("data/visit_jeju_csv_tour_spot.csv")
        )
        filtered_data = df[df["alltag"].str.contains(keyword)][COLUMNS]
        if filtered_data.empty:
            return "No location found."
        else:
            final_format = ""
            for index, row in filtered_data.iterrows():
                title = row["title"] if "title" in row else ""
                address = row["address"] if "address" in row else ""
                latitude = row["latitude"] if "latitude" in row else ""
                longitude = row["longitude"] if "longitude" in row else ""
                phoneno = row["phoneno"] if "phoneno" in row else ""
                repPhoto = row["repPhoto"] if "repPhoto" in row else ""
                try:
                    repPhoto = json.loads(repPhoto.replace("'", '"'))["photoid"][
                        "imgpath"
                    ]
                except:
                    repPhoto = "-"
                information_format = f"""
                        Title: {title}
                        Address: {address}
                        Latitude: {latitude}
                        Longitude: {longitude}
                        Phone Number: {phoneno}
                        repPhoto: {repPhoto}
                """
                final_format += information_format
                final_format += "\n"

            return final_format
