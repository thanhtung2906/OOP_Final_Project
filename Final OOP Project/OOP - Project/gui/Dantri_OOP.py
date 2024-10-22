import tkinter as tk
from tkinter import scrolledtext, messagebox
import pandas as pd
import requests
from bs4 import BeautifulSoup

df1 = pd.read_csv(r'D:\Phenikaa\Python\Final OOP Project\OOP - Project\Import data into database\dantri_database_article.csv')
class GUI:
    def __init__(self, root):
        self.root = root
        self.filtered_df = df1
        self.total_pages = len(self.filtered_df)
        self.page = 0 

        self.root.title('Online Newspaper Reader')

        # Buttons for DanTri
        self.dantri_button = tk.Button(root, text='DanTri', command=self.load_dantri)
        self.dantri_button.grid(row=0, column=0, padx=10, pady=10)

        self.home_button = tk.Button(root, text='Home', command=self.clear_all_but_home)
        self.home_button.grid(row=0, column=1, padx=10, pady=10)

        self.text_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
        self.text_display.grid(row=2, column=0, columnspan=6, padx=10, pady=10)

        self.label_word_count = tk.Label(root, text="Word Count: 0")
        self.label_word_count.grid(row=6, column=0, padx=10, pady=10)

        self.label_page_count = tk.Label(root, text="Page 1/1")
        self.label_page_count.grid(row=6, column=1, padx=10, pady=10)

        self.search_bar = tk.Entry(root, width=50)
        self.search_bar.grid(row=7, column=0, padx=10, pady=10)

        self.search_button = tk.Button(root, text="Search", command=self.perform_search)
        self.search_button.grid(row=7, column=1, padx=10, pady=10)

        self.page_back_button = tk.Button(root, text="Back", command=self.page_backward)
        self.page_back_button.grid(row=5, column=0, padx=10, pady=10)

        self.page_forward_button = tk.Button(root, text="Forward", command=self.page_forward)
        self.page_forward_button.grid(row=5, column=1, padx=10, pady=10)
    def change_categories(self, category):
        self.filtered_df = df1[df1['Category'].isin([category])].reset_index(drop=True)
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
    def clear_all_but_home(self):
        for widget in self.root.winfo_children():
            if widget not in [self.dantri_button, self.home_button]:
                widget.grid_forget()

    def load_dantri(self):
        
        self.total_pages = len(self.filtered_df)
        self.page = 0
        self.load_article()

    def load_article(self):
        if 0 <= self.page < self.total_pages:
            article = self.filtered_df.iloc[self.page]
            article_text = f"Category: {article['Category']}\nLink: {article['Link']}"
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, article_text)
            self.label_page_count.config(text=f"Page {self.page + 1}/{self.total_pages}")
            word_count = len(article['Content'].split())
            self.label_word_count.config(text=f"Word Count: {word_count}")
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

    def perform_search(self):
        keyword = self.search_bar.get()
        if keyword:
            result = self.filtered_df[self.filtered_df['Content'].str.contains(keyword, case=False, na=False)]
            if not result.empty:
                self.filtered_df = result.reset_index(drop=True)
                self.total_pages = len(self.filtered_df)
                self.page = 0
                self.load_article()
            else:
                messagebox.showinfo("Info", f"No articles found containing the keyword '{keyword}'.")
        else:
            messagebox.showinfo("Info", "Please enter a keyword to search.")

root = tk.Tk()
app = GUI(root)
root.mainloop()
