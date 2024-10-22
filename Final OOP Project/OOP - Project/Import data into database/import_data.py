import requests
from bs4 import BeautifulSoup
import pandas as pd

class news_vnexpress:
    # Định nghĩa object news (ở đây là trang báo vnexpress) thuộc tính là url của trang báo
    def __init__(self, url, item):
        self.url = url
        self.item = item
        self.link = None 
    
    def get_link(self): # Hàm get link để lấy link của một bài báo trong object
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        article = soup.find('article', {'data-medium': f"Item {self.item}" })
        if article:
            a_tags = article.find_all('a')
            for a in a_tags:
                self.link = a.get('href') # href là link của bài báo trong trang vnexpress

class article_vnexpress:
    # article là bài báo được lấy từ trang vnexpress
    def __init__(self, link, title=None, description=None, content_text=None, author=None):
        self.link = link
        self.title = title
        self.description = description
        self.content_text = content_text
        self.author = author
    
    def get_title(self):
        news_request = requests.get(self.link)
        soup = BeautifulSoup(news_request.text, 'html.parser')
        title = soup.find_all('h1', class_='title-detail')
        self.title = [tag.get_text(strip=True) for tag in title]
    
    def get_description(self):
        news_request = requests.get(self.link)
        soup = BeautifulSoup(news_request.text, 'html.parser')
        description = soup.find_all('p', class_='description')
        self.description = [tag.get_text(strip=True) for tag in description]
    
    def get_content(self):
        news_request = requests.get(self.link)
        soup = BeautifulSoup(news_request.text, 'html.parser')
        content = soup.find_all('p', class_='Normal')
        self.content_text = [tag.get_text(strip=True) for tag in content]
    
    def get_author(self):
        news_request = requests.get(self.link)
        soup = BeautifulSoup(news_request.text, 'html.parser')
        author = soup.find('p', align='right', class_='Normal')
        self.author = author.get_text(strip=True) if author else "Unknown"
    
    def get_all_information(self):
        self.get_content()
        self.get_title()
        self.get_description()
        self.get_author()
    
    def print_out(self):
        print(f"Title: {', '.join(self.title)}")
        print(f"Description: {', '.join(self.description)}")
        print("Content:")
        for paragraph in self.content_text:
            print(paragraph)
        print(f"Author: {self.author}")
        print(self.link)

# Danh sách chứa các bài báo
articles = []

for i in range(5, 100):
    vnexpress = news_vnexpress("https://vnexpress.net/khoa-hoc", i)
    vnexpress.get_link()
    
    # Kiểm tra nếu có link thì mới tiếp tục
    if vnexpress.link:
        vnexpress_article = article_vnexpress(vnexpress.link)
        vnexpress_article.get_all_information()
        
        # Thêm thông tin bài báo vào danh sách articles
        articles.append({
            'Title': ', '.join(vnexpress_article.title),
            'Description': ', '.join(vnexpress_article.description),
            'Content': ' '.join(vnexpress_article.content_text),
            'Author': vnexpress_article.author,
            'Link': vnexpress_article.link
        })
    else:
        print(f"No article found at offset {i}")

# Chuyển dữ liệu vào DataFrame của pandas và lưu vào file CSV
df = pd.DataFrame(articles)
df.to_csv(r'D:\Phenikaa\Python\Final OOP Project\OOP - Project\Import data into database\database.csv', index=False, encoding='utf-8-sig')

print("Dữ liệu đã được lưu vào file CSV")
