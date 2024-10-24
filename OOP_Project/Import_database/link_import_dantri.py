# dantri_scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL for HTTP requests
base_url = 'https://dantri.com.vn'
categories = {
    "kinh-doanh": "Kinh Doanh",
    "xa-hoi": "Xã Hội",
    "the-thao": "Thể Thao",
    "giai-tri": "Giải trí",
    "the-gioi": "Thế giới",
    "suc-khoe": "Sức Khoẻ"
}
hrefs = []

def get_articles_from_page(category, category_name, page, position):
    url = f'{base_url}/{category}/trang-{page}.htm'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all('article', {'data-content-piece': f'category-timeline_page_{page}-position_{position}'})

    for article in articles:
        link = article.find('a', href=True)['href']
        hrefs.append({"Category": category_name, "Link": base_url + link})

def scrape_articles():
    for category, category_name in categories.items():
        for position in range(14, 250):
            page = round(position/20 + 13/10)
            get_articles_from_page(category, category_name, page, position)

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(hrefs)

    # Save to CSV
    df.to_csv(r'D:\Phenikaa\Python\Final_OOP_Project\OOP_Project\database\dantri_database_link.csv', index=False, encoding='utf-8-sig')

    print("DanTri link imported successfully")

