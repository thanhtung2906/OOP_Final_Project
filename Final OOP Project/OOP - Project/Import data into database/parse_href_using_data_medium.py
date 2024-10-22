from bs4 import BeautifulSoup
import requests
import pandas as pd
urls = []
soups = []
hrefs = []
for i in range(1,10):
    url = f"https://vnexpress.net/khoa-hoc-p{i}"
    urls.append(url)
for url in urls:
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    soups.append(soup) 
for soup in soups:
    for i in range(0,200):
        link = soup.find('a', {'data-medium':f"Item-{i}"})
        if link:
            href = link.get('href')
            hrefs.append({"Khoa học":href})

df = pd.DataFrame(hrefs)
df.to_csv(r'D:\Phenikaa\Python\Final OOP Project\OOP - Project\Import data into database\database.csv', index=False, encoding='utf-8-sig')
print("Data imported sucessfully")


   

