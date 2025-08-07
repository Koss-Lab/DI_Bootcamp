#giphy_user_search.py

import requests

API_KEY = "hpvZycW22qCjn5cRM1xtWB8NKq4dQ2My"
LIMIT = 10
RATING = "g"

def search_gifs(query):
    """
    Search for gifs using the Giphy API.
    """
    url = f"https://api.giphy.com/v1/gifs/search?q={query}&rating={RATING}&limit={LIMIT}&api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["data"]
    else:
        return []

def get_trending_gifs():
    """
    Get trending gifs from Giphy API.
    """
    url = f"https://api.giphy.com/v1/gifs/trending?rating={RATING}&limit={LIMIT}&api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["data"]
    else:
        return []

def display_gifs(gifs):
    """
    Print the URLs of the gifs.
    """
    if not gifs:
        print("❌ No gifs to display.")
        return

    print(f"\nDisplaying {len(gifs)} gifs:\n")
    for i, gif in enumerate(gifs):
        print(f"{i+1}. {gif['url']}")

def main():
    print("Welcome to the Giphy Search Tool 🌀")
    query = input("Enter a term or phrase to search for gifs: ").strip()

    if not query:
        print("No input provided. Showing trending gifs instead.")
        gifs = get_trending_gifs()
    else:
        gifs = search_gifs(query)
        if not gifs:
            print("No results found for your search. Showing trending gifs instead.")
            gifs = get_trending_gifs()

    display_gifs(gifs)

if __name__ == "__main__":
    main()
