import requests
from bs4 import BeautifulSoup
import pandas as pd

articles = []
# Load the CSV file containing links and categories
df = pd.read_csv(r"D:\Phenikaa\Python\Final OOP Project\OOP - Project\Import data into database\dantri_database_link.csv")

# Iterate through the DataFrame
for i in range(len(df)):  # Use len(df) to avoid KeyError
    try:
        data = requests.get(df.at[i, "Link"])
        categories = df.at[i, "Category"]
        soup = BeautifulSoup(data.text, 'html.parser')

        # Title
        soup_title = soup.find('h1', class_='title-page detail')
        title = soup_title.get_text(strip=True) if soup_title else "No title found"

        # Description
        soup_description = soup.find('h2', class_='singular-sapo')
        description = soup_description.get_text(strip=True) if soup_description else "No description found"

        # Content
        soup_content = soup.find_all('p')
        content = ' '.join(tag.get_text(strip=True) for tag in soup_content)  # Join paragraphs into one string

        # Author
        soup_author = soup.find('div', class_="author-wrap")
        author = soup_author.find('b').get_text(strip=True) if soup_author and soup_author.find('b') else "Unknown"

        # Append extracted data
        articles.append({"Category": categories, "Author": author, "Title": title, "Description": description, "Content": content})

    except Exception as e:
        print(f"Error processing index {i}: {e}")

# Convert the list of articles to a DataFrame
df_articles = pd.DataFrame(articles)
# Save the articles to a CSV file
df_articles.to_csv(r"D:\Phenikaa\Python\Final OOP Project\OOP - Project\Import data into database\dantri_database_article.csv", index=False, header=True, encoding='utf-8-sig')

print("Data imported successfully")
