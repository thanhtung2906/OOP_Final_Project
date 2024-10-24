import requests
from bs4 import BeautifulSoup
import pandas as pd
articles = []
df = pd.read_csv(r"D:\Phenikaa\Python\Final_OOP_Project\OOP_Project\database\vnexpress_database_link.csv")


from link_import_vnexpress import scrape_articles

scrape_articles()

for i in range(len(df)):
    data = requests.get(df.at[i,"Link"])
    categories = df.at[i,"Category"]
    soup =  BeautifulSoup(data.text,'html.parser')
#Description 
    description_soup = soup.find_all('p',class_='description')
    
    description = [tag.get_text(strip=True) for tag in description_soup]
#Content
    content_soup = soup.find_all('p',class_='Normal')
    
    content = [tag.get_text(strip=True) for tag in content_soup]
#Title
    title_soup = soup.find_all('h1',class_='title-detail')
    
    title = [tag.get_text(strip=True) for tag in title_soup]
#Author
    
    author_soup = soup.find('p', class_="Normal",style="text-align:right;")
    
    if author_soup:
        author = author_soup.text
    else:
        author = "Unknown"
    


    articles.append({"Category":categories,"Author":author,"Title":title,"Description":description,"Content":content})


df = pd.DataFrame(articles)
df.to_csv(r"D:\Phenikaa\Python\Final_OOP_Project\OOP_Project\database\vnexpress_database_article.csv", index=False,header=True, encoding='utf-8-sig')
print("Vnexpress article imported sucessfully")
