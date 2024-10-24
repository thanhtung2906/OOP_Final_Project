import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import pandas as pd
import time


dantri = pd.read_csv(r"D:\Phenikaa\Python\Final_OOP_Project\OOP_Project\database\dantri_database_article.csv")
vnexpress = pd.read_csv(r"D:\Phenikaa\Python\Final_OOP_Project\OOP_Project\database\vnexpress_database_article.csv")


class GUI:
    def __init__(self,root):
        self.root = root
        self.news_source = pd.DataFrame()
        self.category_buttons = []
       
        self.page = 0 
        self.root.title('Online Newspaper Reader')
        #Vnexpress change categories button  
    def button_delete(self):
        self.text_display.clear()
    def button_load(self):
        # ScrolledText to display the article
        self.text_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
        self.text_display.grid(row=2, column=0, columnspan=6, padx=10, pady=10)
        # Buttons for categories
        self.category_buttons = []
        #Back and Foward button of VNexpress
        self.back_button = tk.Button(root,text="Back",command=self.page_backward)
        self.forward_button = tk.Button(root,text="Forward",command=self.page_forward)
        self.back_button.grid(row=5, column=0, padx=10, pady=10)
        self.forward_button.grid(row=5, column=1, padx=10, pady=10)

        self.label_word_count = tk.Label(root, text="Word Count: 0")
        self.label_word_count.grid(row=6, column=0, padx=10, pady=10)

        # Page Count Label
        self.label_vnexpress_page_count = tk.Label(root, text="Page 1/1")
        self.label_vnexpress_page_count.grid(row=6, column=1, padx=10, pady=10)


        self.search_bar = tk.Entry(root, width=50)
        self.search_bar.grid(row=7, column=0, padx=10, pady=10)

        self.search_button = tk.Button(root, text="Search", command=self.perform_search)
        self.search_button.grid(row=7, column=1, padx=10, pady=10)
    def clear_category_buttons(self):
        for btn in self.category_buttons:
            btn.grid_forget()
        self.category_buttons.clear()   
    def change_source(self,source):
        if source == "dantri":
            self.news_source = dantri 
        elif source == "vnexpress":
            self.news_source = vnexpress 
    def change_categories(self, category):
        self.filtered_df = self.news_source[self.news_source['Category'].isin([category])].reset_index(drop=True)
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
            self.description = self.filtered_df.loc[self.page,"Description"]
            self.author = self.filtered_df.loc[self.page, "Author"]
            self.content = self.filtered_df.loc[self.page, "Content"]
            self.title = self.filtered_df.loc[self.page, "Title"]
            self.display_article()  # Update the display
        else:
            messagebox.showwarning("Warning", "No more articles in this direction.")
    
    def display_article(self):
        self.button_load()
        self.text_display.delete(1.0, tk.END)
        if self.content:
            article_text = f"Author: {self.author}\nTitle: {self.title}\n\nDescription: {self.description}\n\n{self.content}"
            self.text_display.insert(tk.INSERT, article_text)
            word_count = self.word_count()
            self.label_word_count.config(text=f"Word Count: {word_count}")
            page_count = self.total_pages
            self.label_vnexpress_page_count.config(text=f"Page {self.page + 1}/{page_count}")
        else:
            self.text_display.insert(tk.INSERT, "No articles available.")
    
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
    def perform_search(self):
        keyword = self.search_bar.get()
        if keyword:
            self.keyword_searching(keyword)
        else:
            messagebox.showinfo("Info", "Please enter a keyword to search.")
            
    def keyword_searching(self, keyword: str):
        result = self.filtered_df[self.filtered_df['Content'].str.contains(keyword, case=False, na=False)]
        if not result.empty:
            self.filtered_df = result.reset_index(drop=True)
            self.total_pages = len(self.filtered_df)
            self.page = 0
            self.load_article()  # Display the first article in the search result
        else:
            messagebox.showinfo("Info", f"No articles found containing the keyword '{keyword}'.")

    def word_count(self):
        if isinstance(self.content, str):
            return len(self.content.split())
        return 0  


    def page_count(self):
        return len(self.filtered_df)
    
    
class Vnexpress(GUI):  
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        
        self.filtered_df = vnexpress
        self.vnexpress_button = tk.Button(root,text='Vnexpress',command=self.vnexpress)
        self.vnexpress_button.grid(row=0, column=1, padx=10, pady=10)
        self.page = 0
        self.total_pages = len(vnexpress)
        self.change_source("vnexpress")
    
    def vnexpress(self):
        self.clear_category_buttons()
        self.page_count()
        self.change_source("vnexpress")
        self.load_article()
        
        categories = [
            ("Thế giới", self.the_gioi),
            ("Kinh Doanh", self.kinh_doanh),
            ("Khoa Học", self.khoa_hoc),
            ("Giáo dục", self.giao_duc),
            ("Sức Khoẻ", self.suc_khoe),
            ("Thời sự", self.thoi_su)
        ]
        for idx, (name, cmd) in enumerate(categories):
            btn = tk.Button(self.root, text=name, command=cmd)
            btn.grid(row=1, column=idx, padx=10, pady=10)
            self.category_buttons.append(btn) 
    def the_gioi(self):
        self.change_categories("Thế giới")
        self.load_article()
    def kinh_doanh(self):
        self.change_categories("Kinh Doanh")
        self.load_article()
    def suc_khoe(self):
        self.change_categories("Sức khoẻ")
        self.load_article()
    def khoa_hoc(self):
        self.change_categories("Khoa Học")
        self.load_article()
    def giao_duc(self):
        self.change_categories("Giáo dục")
        self.load_article()
    def thoi_su(self):
        self.change_categories("Thời Sự")
        self.load_article()      
class DanTri(GUI):
    def __init__(self, root):
        
        self.category_buttons = []
        self.root = root
        self.filtered_df = dantri
        
        
        self.dantri_button = tk.Button(root,text='Dantri',command=self.dantri)
        self.dantri_button.grid(row=0, column=2, padx=10, pady=10)
        self.page = 0
        self.change_source("dantri")
        self.total_pages = len(dantri)
    def dantri(self):
        self.clear_category_buttons()
        self.page_count()
        self.change_source("dantri")
        self.load_article()
        categories = [
            ("Thế giới", self.the_gioi),
            ("Kinh Doanh", self.kinh_doanh),
            ("Xã Hội", self.xa_hoi),
            ("Thể Thao", self.the_thao),
            ("Giải Trí", self.giai_tri),
            ("Sức Khoẻ", self.suc_khoe)
        ]

        for idx, (name, cmd) in enumerate(categories):
            btn = tk.Button(self.root, text=name, command=cmd)
            btn.grid(row=1, column=idx, padx=10, pady=10)
            self.category_buttons.append(btn)
    def the_gioi(self):
        self.change_categories("Thế giới")
        self.load_article()
    def kinh_doanh(self):
        self.change_categories("Kinh Doanh")
        self.load_article()
    def suc_khoe(self):
        self.change_categories("Sức khoẻ")
        self.load_article()
    def giai_tri(self):
        self.change_categories("Giải trí")
        self.load_article()
    def the_thao(self):
        self.change_categories("Thể Thao")
        self.load_article()
    def xa_hoi(self):
        self.change_categories("Xã Hội")
        self.load_article()

root = tk.Tk()
app = GUI(root)   
vnexpress_app = Vnexpress(root)
dantri_app = DanTri(root)
root.mainloop() 



       