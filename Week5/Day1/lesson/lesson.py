#lesson.py

import pandas as pd

data = {
    'Book Title': ['The Great Gatsby', 'To Kill a Mockingbird', '1984',
                   'Pride and Prejudice', 'The Catcher in the Rye'],
    'Author': ['F. Scott Fitzgerald', 'Harper Lee', 'George Orwell',
               'Jane Austen', 'J.D. Salinger'],
    'Genre': ['Classic', 'Classic', 'Dystopian', 'Classic', 'Classic'],
    'Price': [10.99, 8.99, 7.99, 11.99, 9.99],
    'Copies Sold': [500, 600, 800, 300, 450]
}
df = pd.DataFrame(data)

df.head()
df.describe()
df.info()

df.sort_values(by="Price")
df.sort_values(by="Copies Sold", ascending=False)

df[df["Genre"] == "Classic"]
df[df["Price"] > 10]

df.groupby("Author", as_index=False)["Copies Sold"].sum()


