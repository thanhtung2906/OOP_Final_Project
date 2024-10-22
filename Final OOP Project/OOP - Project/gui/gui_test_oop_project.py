import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import pandas as pd
import time


df = pd.read_csv(r"D:\Phenikaa\Python\Final OOP Project\OOP - Project\Import data into database\database_article.csv")
df1 = pd.read_csv(r'D:\Phenikaa\Python\Final OOP Project\OOP - Project\Import data into database\dantri_database_article.csv')
class GUI:
    def __init__(self,root):
        self.root = root
        self.filtered_df = df
        self.total_pages = len(self.filtered_df)
        self.page = 0 
   
        self.root.title('Online Newspaper Reader')

        #Button to change website to Vnexpress
        self.vnexpress_button = tk.Button(root,text='Vnexpress',command=self.vnexpress)
        self.vnexpress_button.grid(row=0, column=1, padx=10, pady=10)
        self.persistent_buttons = [self.vnexpress_button]

        self.home = tk.Button(root,text='Home',command=self.clear_all_but_vnexpress)
        self.home.grid(row=0, column=2, padx=10, pady=10)
    

        #Vnexpress change categories button
        self.vnexpress_button_thegioi = tk.Button(root, text="Thế giới", command=self.the_gioi)
        self.vnexpress_button_kinhdoanh = tk.Button(root, text="Kinh Doanh", command=self.kinh_doanh)
        self.vnexpress_button_khoahoc = tk.Button(root, text="Khoa Học", command=self.khoa_hoc)
        self.vnexpress_button_giaitri = tk.Button(root, text="Giáo Dục", command=self.giao_duc)
        self.vnexpress_button_suckhoe = tk.Button(root, text="Sức Khoẻ", command=self.suc_khoe)
        self.vnexpress_button_thethao = tk.Button(root, text="Thời Sự", command=self.thoi_su)

        
    def clear_all_but_vnexpress(self):
        for widget in self.root.winfo_children():
            if widget not in self.persistent_buttons:
                widget.grid_forget()  # Hoặc dùng widget.destroy() để xóa hoàn toàn
    def button_delete(self):
        self.text_display.clear()
    def button_load(self):
        # ScrolledText to display the article
        self.text_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
        self.text_display.grid(row=2, column=0, columnspan=6, padx=10, pady=10)
        # Buttons for categories
        self.category_buttons = []
        #Back and Foward button of VNexpress
        self.vnexpress_back_button = tk.Button(root,text="Back",command=self.page_backward)
        self.vnexpress_forward_button = tk.Button(root,text="Forward",command=self.page_forward)
        self.vnexpress_back_button.grid(row=5, column=0, padx=10, pady=10)
        self.vnexpress_forward_button.grid(row=5, column=1, padx=10, pady=10)

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
    def vnexpress(self):
        self.filtered_df = df
        self.load_article()
        self.clear_category_buttons()
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
        self.home.grid(row=0, column=2, padx=10, pady=10)
    
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
            self.display_vnexpress_article()  # Update the display
        else:
            messagebox.showwarning("Warning", "No more articles in this direction.")
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
    def display_vnexpress_article(self):
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
    def keyword_searching(self,keyword:str):
        result = self.filtered_df[self.filtered_df['Content'].str.contains(keyword, case=False, na=False)]
        if not result.empty:
            print(result)
        else:
            print("NOT FOUND")



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
        return len(self.content.split()) 

    def page_count(self):
        return len(self.filtered_df)
    
    
            
    
      


root = tk.Tk()
app = GUI(root)
root.mainloop()    



       