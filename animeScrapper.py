import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

base_url_english = "https://animeslayer.space/en-anime-letter/"
base_url_arabic = "https://animeslayer.space/ar-anime-letter/"

# Combine English and Arabic alphabets
# English alphabets
alphabets_english = "".join(chr(ord("a") + i) for i in range(26))

# Arabic alphabets (a simplified set for demonstration)
alphabets_arabic = "".join(chr(ord("أ") + i) for i in range(28))


# Initialize empty lists to store data
titles = []
image_srcs = []
statuses = []
descriptions = []
types = []
links = []

# Iterate through English alphabet
for letter in alphabets_english:
    url = base_url_english + letter
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract information from each anime card
        anime_cards = soup.find_all("div", class_="anime-card-container")

        for anime_card in anime_cards:
            # Extract title
            try:
                title = (
                    anime_card.find("div", class_="anime-card-title")
                    .find("a")
                    .text.strip()
                )
            except AttributeError:
                title = None

            # Extract image source
            try:
                image_src = anime_card.find("img", class_="img-responsive")["src"]
            except (AttributeError, TypeError):
                image_src = None

            # Extract status
            try:
                status = (
                    anime_card.find("div", class_="anime-card-status")
                    .find("a")
                    .text.strip()
                )
            except AttributeError:
                status = None

            # Extract description
            try:
                description = anime_card.find("div", class_="anime-card-details").find(
                    "div", class_="anime-card-title"
                )["data-content"]
            except AttributeError:
                description = None

            # Extract type
            try:
                anime_type = (
                    anime_card.find("div", class_="anime-card-type")
                    .find("a")
                    .text.strip()
                )
            except AttributeError:
                anime_type = None

            # Extract link
            try:
                anime_link = anime_card.find("div", class_="anime-card-title").find(
                    "a"
                )["href"]
            except (AttributeError, TypeError):
                anime_link = None

            # Append data to lists
            titles.append(title)
            image_srcs.append(image_src)
            statuses.append(status)
            descriptions.append(description)
            types.append(anime_type)
            links.append(anime_link)
    else:
        print(
            f"Failed to retrieve the page for letter {letter}. Status code: {response.status_code}"
        )

# Iterate through Arabic alphabet
for letter in alphabets_arabic:
    url = base_url_arabic + letter
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract information from each anime card
        anime_cards = soup.find_all("div", class_="anime-card-container")

        for anime_card in anime_cards:
            # Extract title
            try:
                title = (
                    anime_card.find("div", class_="anime-card-title")
                    .find("a")
                    .text.strip()
                )
            except AttributeError:
                title = None

            # Extract image source
            try:
                image_src = anime_card.find("img", class_="img-responsive")["src"]
            except (AttributeError, TypeError):
                image_src = None

            # Extract status
            try:
                status = (
                    anime_card.find("div", class_="anime-card-status")
                    .find("a")
                    .text.strip()
                )
            except AttributeError:
                status = None

            # Extract description
            try:
                description = anime_card.find("div", class_="anime-card-details").find(
                    "div", class_="anime-card-title"
                )["data-content"]
            except AttributeError:
                description = None

            # Extract type
            try:
                anime_type = (
                    anime_card.find("div", class_="anime-card-type")
                    .find("a")
                    .text.strip()
                )
            except AttributeError:
                anime_type = None

            # Extract link
            try:
                anime_link = anime_card.find("div", class_="anime-card-title").find(
                    "a"
                )["href"]
            except (AttributeError, TypeError):
                anime_link = None

            # Append data to lists
            titles.append(title)
            image_srcs.append(image_src)
            statuses.append(status)
            descriptions.append(description)
            types.append(anime_type)
            links.append(anime_link)
    else:
        print(
            f"Failed to retrieve the page for letter {letter}. Status code: {response.status_code}"
        )

# Create a DataFrame from the lists
anime_data = {
    "Title": titles,
    "Image Source": image_srcs,
    "Status": statuses,
    "Description": descriptions,
    "Type": types,
    "Link": links,
}

df_anime = pd.DataFrame(anime_data)

# Get the current working directory
current_directory = os.getcwd()
db_file_path = os.path.join(current_directory, "anime_data.db")
conn = sqlite3.connect(db_file_path)
# Save the anime DataFrame to the SQLite database
df_anime.to_sql("anime_table", conn, index=False, if_exists="replace")
conn.close()

print("End")
