import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import pandas as pd

df = pd.read_csv(r"D:\Phenikaa\Python\Final OOP Project\OOP - Project\Import data into database\database_article.csv")

class Article:
    def __init__(self, author, title, description, content):
        self.author = author 
        self.title = title 
        self.description = description
        self.content = content
    def read_page(self,page):
        self.page = page 
        self.load_article()
        self.display_article()
    def display_article(self):
        print("Title:", self.title)
        print("Author:", self.author)
        print("Description:", self.description)
        print("Content:", self.content)
        print(f"Page:{self.page}/{len(self.filtered_df)}")

class Vnexpress_article(Article):
    def __init__(self, author, title, description, content, initial_category="Khoa Học"):
        super().__init__(author, title, description, content)
        self.page = 0
        self.change_categories(initial_category)
    
    def change_categories(self, category):
        self.filtered_df = df[df['Category'].isin([category])].reset_index(drop=True)
        self.total_pages = len(self.filtered_df)
        self.page = 0 
        if self.total_pages > 0:
            self.load_article()
        else:
            
            self.description = ""
            self.author = ""
            self.content = ""
            self.title = ""
            messagebox.showinfo("Info", f"No articles found in category '{category}'.")
    
    def load_article(self):
        if 0 <= self.page < self.total_pages:
            self.description = self.filtered_df.loc[self.page, "Description"]
            self.author = self.filtered_df.loc[self.page, "Author"]
            self.content = self.filtered_df.loc[self.page, "Content"]
            self.title = self.filtered_df.loc[self.page, "Title"]
        else:
            messagebox.showwarning("Warning", "No more articles in this direction.")
    
    def page_forward(self):
        if self.page < self.total_pages - 1:
            self.page += 1
            self.load_article()
        else:
            messagebox.showinfo("Info", "You are on the last article.")
    
    def page_backward(self):
        if self.page > 0:
            self.page -= 1
            self.load_article()
        else:
            messagebox.showinfo("Info", "You are on the first article.")
    def keyword_searching(self,keyword:str):
        result = self.filtered_df[self.filtered_df['Content'].str.contains(keyword, case=False, na=False)]

        # Nếu có bài báo chứa keyword, in ra
        if not result.empty:
            print(result)
        else:
            print("NOT FOUND")

    
if __name__ == "__main__":

    tung = Vnexpress_article(author="", title="", description="", content="", initial_category="Khoa Học")
    '''
    tung.change_categories("Giáo dục")
    tung.display_article()
    
    # Navigate forward
    tung.page_forward()
    tung.display_article()
 
    
    # Navigate backward
    tung.page_backward()
    tung.display_article()'''

    tung.keyword_searching("Trí tuệ nhân tạo")
    tung.read_page(149)
 
  
