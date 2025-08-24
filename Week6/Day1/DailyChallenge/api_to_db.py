import psycopg2
import requests
import random

DB_NAME = "postgres"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT
    )

# Try official API first, fallback to GitHub mirror
urls = [
    "https://restcountries.com/v3.1/all",
    "https://restcountries.com/v2/all",
    "https://raw.githubusercontent.com/mledoze/countries/master/countries.json"
]

response = None
for url in urls:
    try:
        print(f"Trying {url} ...")
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, verify=False)
        if response.status_code == 200:
            print("Success ✅")
            break
    except Exception as e:
        print(f"Error with {url}:", e)

if not response or response.status_code != 200:
    raise Exception("Could not fetch countries data from any source.")

all_countries = response.json()
random_countries = random.sample(all_countries, 10)

conn = get_connection()
cur = conn.cursor()

for country in random_countries:
    # Handle both formats (restcountries vs github dataset)
    name = country.get("name", {}).get("common") if isinstance(country.get("name"), dict) else country.get("name", "Unknown")
    if not name:
        name = "Unknown"

    capital = country.get("capital")
    if isinstance(capital, list):
        capital = capital[0] if capital else "Unknown"
    elif isinstance(capital, str):
        capital = capital
    else:
        capital = "Unknown"

    flag = country.get("flags", {}).get("png") if isinstance(country.get("flags"), dict) else country.get("flag", "")
    if not flag:
        flag = ""

    subregion = country.get("subregion", "Unknown")
    population = country.get("population", 0)

    cur.execute(
        """
        INSERT INTO countries (name, capital, flag, subregion, population)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (name, capital, flag, subregion, population)
    )

conn.commit()
cur.close()
conn.close()

print("10 random countries successfully inserted ✅")