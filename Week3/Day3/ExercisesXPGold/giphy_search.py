#giphy_search.py

import requests

# API parameters
API_KEY = "hpvZycW22qCjn5cRM1xtWB8NKq4dQ2My"
SEARCH_TERM = "hilarious"
RATING = "g"
LIMIT = 10  # Get only the first 10 gifs

# Build the URL using f-string
url = f"https://api.giphy.com/v1/gifs/search?q={SEARCH_TERM}&rating={RATING}&limit={LIMIT}&api_key={API_KEY}"

# Send the GET request
response = requests.get(url)

# Step 1: Check if status code is 200 (OK)
if response.status_code == 200:
    data = response.json()

    # Step 2: Filter gifs with height > 100
    big_gifs = []
    for gif in data["data"]:
        height = int(gif["images"]["original"]["height"])
        if height > 100:
            big_gifs.append(gif)

    # Step 3: Print results
    print(f"\nTotal gifs received: {len(data['data'])}")
    print(f"Gifs with height > 100: {len(big_gifs)}\n")

    # Step 4: Print the first 10 gif URLs
    print("First 10 filtered gifs:")
    for i, gif in enumerate(big_gifs[:10]):
        print(f"{i+1}. {gif['url']}")
else:
    print("Error fetching gifs from Giphy API. Status code:", response.status_code)
