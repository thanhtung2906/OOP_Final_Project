from bs4 import BeautifulSoup
import requests
import pandas as pd

hrefs = []
categories = {"kinh-doanh": "Kinh Doanh", "khoa-hoc": "Khoa Học","suc-khoe":"Sức khoẻ","giao-duc":"Giáo dục","the-gioi":"Thế giới","thoi-su":"Thời Sự"}
def scrape_articles():
    for category, category_name in categories.items():
        for i in range(1, 10): 
            url = f"https://vnexpress.net/{category}-p{i}"
            data = requests.get(url)
            soup = BeautifulSoup(data.text, 'html.parser')
            for z in range(0, 200):
                link = soup.find('a', {'data-medium':f"Item-{z}"})
                if link:
                    href = link.get('href')
                    hrefs.append({"Category": category_name, "Link": href})
    df = pd.DataFrame(hrefs)
    df.to_csv(r'D:\Phenikaa\Python\Final_OOP_Project\OOP_Project\database\vnexpress_database_link.csv', index=False, encoding='utf-8-sig')

    print("Vnexpress link imported successfully")
