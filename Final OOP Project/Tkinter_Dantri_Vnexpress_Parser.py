import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
class news_dantri:
    #Định nghĩa object news (ở đây là trang báo vnexpress) thuộc tính là url của trang báo
    def __init__(self,url,position):
        self.url = url
        self.position = position
        self.link = None 
        self.article_link = None
    
    def get_link(self): #Hàm get link để lấy link của một bài báo trong object
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        article = soup.find('article',{'data-content-piece': str('category-timeline_page_1-position_' + str(self.position))})
        if article:
            a_tags = article.find_all('a')
            for a in a_tags:
                self.link = a.get('href')# href là link của bài báo trong trang vnexpress
        self.dantri_article_link = ("https://dantri.com.vn"+str(self.link))
class article:
    def __init__(self,dantri_article_link,title,description,content_text):
        self.dantri_article_link = dantri_article_link
        self.title = title
        self.description = description
        self.content_text  = content_text

class article_dantri(article):
    def get_title(self):
        news_request = requests.get(self.dantri_article_link)
        soup =  BeautifulSoup(news_request.text,'html.parser')
        title = soup.find_all('h1',class_='title-page detail')
        self.title = [tag.get_text(strip=True) for tag in title]
    def get_description(self):
        news_request = requests.get(self.dantri_article_link)
        soup =  BeautifulSoup(news_request.text,'html.parser')
        description = soup.find_all('h2',class_='singular-sapo')
        self.description = [tag.get_text(strip=True) for tag in description]
    def get_content(self):
        news_request = requests.get(self.dantri_article_link)
        soup =  BeautifulSoup(news_request.text,'html.parser')
        content = soup.find_all('p')
        self.content = [tag.get_text(strip=True) for tag in content]
    def get_author(self):
        news_request = requests.get(self.dantri_article_link)
        soup =  BeautifulSoup(news_request.text,'html.parser')
        author = soup.find('div',class_="author-wrap")
        self.author = author.find('b')
    def get_all_information(self):
        self.get_content()
        self.get_title()
        self.get_description()
        self.get_author()

    def print_out(self):
        print(f"Title: {', '.join(self.title)}")
        print(f"Description: {', '.join(self.description)}")
        print("Content:")
        for paragraph in self.content:
            print(paragraph) 
        print(self.author.text)   
class news_vnexpress:
    #Định nghĩa object news (ở đây là trang báo vnexpress) thuộc tính là url của trang báo
    def __init__(self,url,offset):
        self.url = url
        self.offset = offset
        self.link = None 
    
    def get_link(self): #Hàm get link để lấy link của một bài báo trong object
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        article = soup.find('article',{'data-offset': int(self.offset)})
        if article:
            a_tags = article.find_all('a')
            for a in a_tags:
                self.link = a.get('href')# href là link của bài báo trong trang vnexpresszz
class article_vnexpress(article):
    def get_title(self):
        news_request = requests.get(self.link)
        soup =  BeautifulSoup(news_request.text,'html.parser')
        title = soup.find_all('h1',class_='title-detail')
        self.title = [tag.get_text(strip=True) for tag in title]
    def get_description(self):
        news_request = requests.get(self.link)
        soup =  BeautifulSoup(news_request.text,'html.parser')
        description = soup.find_all('p',class_='description')
        self.description = [tag.get_text(strip=True) for tag in description]
    def get_content(self):
        news_request = requests.get(self.link)
        soup =  BeautifulSoup(news_request.text,'html.parser')
        content = soup.find_all('p',class_='Normal')
        self.content = [tag.get_text(strip=True) for tag in content]
    def get_author(self):
        news_request = requests.get(self.link)
        soup =  BeautifulSoup(news_request.text,'html.parser')
        self.author = soup.find('p', class_="Normal",style="text-align:right;")

    def get_all_information(self):
        self.get_content()
        self.get_title()
        self.get_description()
        self.get_author()
    def print_out(self):
        print(f"Title: {', '.join(self.title)}")
        print(f"Description: {', '.join(self.description)}")
        print("Content:")
        for paragraph in self.content:
            print(paragraph)     
        print(self.author.text)   
class News_GUI:
    def __init__(self,root):
        self.root = root
        self.link_of_vnexpress_type = 'https://vnexpress.net/the-gioi'
        self.link_of_dantri_type = "https://dantri.com.vn/the-gioi.htm"
        self.offset = 5
        self.position = 5
        self.root.title = ('Online Newspaper Reader')
        #Button to change website to Dantri
        self.dantri_button = tk.Button(root,text='Dân trí',command=self.change_to_dantri)
        self.dantri_button.grid(row=0, column=0, padx=10, pady=10)
        #Button to change website to Vnexpress
        self.vnexpress_button = tk.Button(root,text='Vnexpress',command=self.change_to_vnexpress)
        self.vnexpress_button.grid(row=0, column=1, padx=10, pady=10)
        #Dan tri change categories button 
        self.dantri_button_thegioi = tk.Button(root, text="Thế giới", command=self.dantri_type_thegioi)
        self.dantri_button_kinhdoanh = tk.Button(root, text="Kinh Doanh", command=self.dantri_type_kinhdoanh)
        self.dantri_button_xahoi = tk.Button(root, text="Xã hội", command=self.dantri_type_xahoi)
        self.dantri_button_giaitri = tk.Button(root, text="Giải trí", command=self.dantri_type_giaitri)
        self.dantri_button_thethao = tk.Button(root, text="Thể Thao", command=self.dantri_type_thethao)
        self.dantri_button_suckhoe = tk.Button(root, text="Sức khoẻ", command=self.dantri_type_suckhoe)

        #Vnexpress change categories button
        self.vnexpress_button_thegioi = tk.Button(root, text="Thế giới", command=self.vnexpress_type_thegioi)
        self.vnexpress_button_kinhdoanh = tk.Button(root, text="Kinh Doanh", command=self.vnexpress_type_kinhdoanh)
        self.nexpress_button_khoahoc = tk.Button(root, text="Khoa Học", command=self.vnexpress_type_khoahoc)
        self.nexpress_button_giaitri = tk.Button(root, text="Giải trí", command=self.vnexpress_type_giaitri)
        self.nexpress_button_thethao = tk.Button(root, text="Thể Thao", command=self.vnexpress_type_thethao)
        self.nexpress_button_thoisu = tk.Button(root, text="Thời sự", command=self.vnexpress_type_thoisu)

        # ScrolledText to display the article
        self.text_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
        self.text_display.grid(row=2, column=0, columnspan=6, padx=10, pady=10)
        # Buttons for categories
        self.category_buttons = []
        #Back and Foward button of VNexpress
        self.vnexpress_back_button = tk.Button(root,text="Back",command=self.vnexpress_back)
        self.vnexpress_forward_button = tk.Button(root,text="Forward",command=self.vnexpress_forward)
        
        #Back and Foward button of Dantri
        self.dantri_back_button = tk.Button(root,text="Back",command=self.dantri_back)
        self.dantri_forward_button = tk.Button(root,text="Forward",command=self.dantri_forward)
        #Word count label
        self.label_word_count = tk.Label(root,text = self.word_count)
        #Page counter
        self.label_vnexpress_page_count = tk.Label(root,text= self.vnexpress_max_page)
        
        
    def change_to_dantri(self):
        self.clear_category_buttons()
        self.dantri_navigation()
        categories = [
            ("Thế giới", self.dantri_type_thegioi),
            ("Kinh Doanh", self.dantri_type_kinhdoanh),
            ("Xã hội", self.dantri_type_xahoi),
            ("Giải trí", self.dantri_type_giaitri),
            ("Thể Thao", self.dantri_type_thethao),
            ("Sức khoẻ", self.dantri_type_suckhoe)
        ]

        for idx, (name, cmd) in enumerate(categories):
            btn = tk.Button(self.root, text=name, command=cmd)
            btn.grid(row=1, column=idx, padx=10, pady=10)
            self.category_buttons.append(btn)
    def clear_category_buttons(self):
        for btn in self.category_buttons:
            btn.grid_forget()
        self.category_buttons.clear()
    
    
    def change_to_vnexpress(self):
        self.clear_category_buttons()
        self.vnexpress_navigation()
        categories = [
            ("Thế giới", self.vnexpress_type_thegioi),
            ("Kinh Doanh", self.vnexpress_type_kinhdoanh),
            ("Khoa Học", self.vnexpress_type_khoahoc),
            ("Giải trí", self.vnexpress_type_giaitri),
            ("Thể Thao", self.vnexpress_type_thethao),
            ("Thời sự", self.vnexpress_type_thoisu)
        ]

        for idx, (name, cmd) in enumerate(categories):
            btn = tk.Button(self.root, text=name, command=cmd)
            btn.grid(row=1, column=idx, padx=10, pady=10)
            self.category_buttons.append(btn)

    def dantri_type_thegioi(self):
        self.link_of_dantri_type = 'https://dantri.com.vn/the-gioi.htm'
        self.dantri_article_parse()

    def dantri_type_kinhdoanh(self):
        self.link_of_dantri_type = 'https://dantri.com.vn/kinh-doanh.htm'
        self.dantri_article_parse()

    def dantri_type_xahoi(self):
        self.link_of_dantri_type = 'https://dantri.com.vn/xa-hoi.htm'
        self.dantri_article_parse()

    def dantri_type_giaitri(self):
        self.link_of_dantri_type = 'https://dantri.com.vn/giai_tri.htm'
        self.dantri_article_parse()

    def dantri_type_thethao(self):
        self.link_of_dantri_type = 'https://dantri.com.vn/the-thao.htm'
        self.dantri_article_parse()

    def dantri_type_suckhoe(self):
        self.link_of_dantri_type = 'https://dantri.com.vn/suc-khoe.htm'
        self.dantri_article_parse()

    def vnexpress_type_thegioi(self):
        self.link_of_vnexpress_type = 'https://vnexpress.net/the-gioi'
        
        self.vnexpress_article_parse()

    def vnexpress_type_kinhdoanh(self):
        self.link_of_vnexpress_type= 'https://vnexpress.net/kinh-doanh'
        
        self.vnexpress_article_parse()
    def vnexpress_type_khoahoc(self):
        self.link_of_vnexpress_type = 'https://vnexpress.net/khoa-hoc'
        
        self.vnexpress_article_parse()
    
    def vnexpress_type_giaitri(self):
        self.link_of_vnexpress_type = 'https://vnexpress.net/giai-tri'
        
        self.vnexpress_article_parse()
    
    def vnexpress_type_thethao(self):
        self.link_of_vnexpress_type = 'https://vnexpress.net/the-thao'
        
        self.vnexpress_article_parse()
    def vnexpress_type_thoisu(self):
        self.link_of_vnexpress_type = 'https://vnexpress.net/thoi-su'
        
        self.vnexpress_article_parse()
    def vnexpress_article_parse(self):
        vnexpress_categories = news_vnexpress(self.link_of_vnexpress_type,self.offset)
        vnexpress_categories.get_link()
        self.vnexpress_article = article_vnexpress(vnexpress_categories.link,[],[],[],[])
        self.vnexpress_article.get_all_information()
        self.display_vnexpress_article()
    def dantri_article_parse(self):
        dantri_categories  = news_dantri(self.link_of_dantri_type,self.position)
        dantri_categories.get_link()
        self.dantri_article = article_dantri(dantri_categories.dantri_article_link,[],[],[])     
        self.dantri_article.get_all_information()
        self.display_dantri_article()

    def display_vnexpress_article(self):
        self.text_display.delete(1.0, tk.END)
        if self.vnexpress_article:
            article = self.vnexpress_article
            self.content = f"Author: {str(article.author.text)}\n"
            self.content += f"Title: {', '.join(article.title)}\n\n"
            self.content += f"Description: {', '.join(article.description)}\n\n"
            self.content += "\n".join(article.content)
            self.text_display.insert(tk.INSERT, self.content)
            word_count = self.word_count()
            self.label_word_count.config(text=f"Word Count: {word_count}")
            page_count = self.vnexpress_max_page()
            self.label_vnexpress_page_count.config(text=f"Page {self.offset}/{page_count}")
        else:
            self.text_display.insert(tk.INSERT, "No articles available.")
    def display_dantri_article(self):
        self.text_display.delete(1.0, tk.END)
        if self.dantri_article:
            article = self.dantri_article
            self.content = f"Author: {str(article.author.text)}\n"
            self.content += f"Title: {', '.join(article.title)}\n\n"
            self.content += f"Description: {', '.join(article.description)}\n\n"
            self.content += "\n".join(article.content)
            
            self.text_display.insert(tk.INSERT, self.content)
            word_count = self.word_count()
            self.label_word_count.config(text=f"Word Count: {word_count}")
            

        else:
            self.text_display.insert(tk.INSERT, "No articles available.")
    def vnexpress_back(self):
        if self.offset > 1:
            self.offset -= 1
            vnexpress_categories = news_vnexpress(self.link_of_vnexpress_type, self.offset)
            vnexpress_categories.get_link()
            self.vnexpress_article = article_vnexpress(vnexpress_categories.link,[],[],[],[])
            self.vnexpress_article.get_all_information()
            self.display_vnexpress_article()
        else:
            messagebox.showinfo("Info", "Already at the first article")
    def vnexpress_forward(self):
        self.offset += 1
        vnexpress_categories = news_vnexpress(self.link_of_vnexpress_type, self.offset)
        vnexpress_categories.get_link()
        self.vnexpress_article = article_vnexpress(vnexpress_categories.link,[],[],[],[])
        self.vnexpress_article.get_all_information()
        self.display_vnexpress_article()
    def dantri_back(self):
        if self.position > 1:
            self.position -= 1
            dantri_categories  = news_dantri(self.link_of_dantri_type,self.position)
            dantri_categories .get_link()
            self.dantri_article = article_dantri(dantri_categories .dantri_article_link,[],[],[])     
            self.dantri_article.get_all_information()
            self.display_dantri_article()
        else:
            messagebox.showinfo("Info", "Already at the first article")
    def dantri_forward(self):
        self.position += 1
        dantri_categories  = news_dantri(self.link_of_dantri_type,self.position)
        dantri_categories .get_link()
        self.dantri_article = article_dantri(dantri_categories .dantri_article_link,[],[],[])     
        self.dantri_article.get_all_information()
        self.display_dantri_article()

    def dantri_navigation(self):
        self.vnexpress_back_button.grid_forget()
        self.vnexpress_forward_button.grid_forget()
        self.dantri_back_button.grid(row=5, column=0, padx=10, pady=10)
        self.dantri_forward_button.grid(row=5, column=1, padx=10, pady=10)

    def vnexpress_navigation(self):
        self.dantri_back_button.grid_forget()
        self.dantri_forward_button.grid_forget()
        self.vnexpress_back_button.grid(row=5, column=0, padx=10, pady=10)
        self.vnexpress_forward_button.grid(row=5, column=1, padx=10, pady=10)
    def word_count(self):
        self.label_word_count.grid(row=5, column=2, padx=10, pady=10)
        self.words = self.content.lower().split(" ")  # Split the content into words based on whitespace
        return len(self.words)
    def vnexpress_max_page(self):
        self.label_vnexpress_page_count.grid(row=6,column=2,padx=10,pady=10)
        response = requests.get(self.link_of_vnexpress_type)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article', attrs={'data-offset': True})
        for article in articles:
            max_offset = article.get('data-offset')
        return max_offset
    def dantri_max_page(self):
        response = requests.get(self.link_of_vnexpress_type)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article', attrs={'data-offset': True})
        for article in articles:
            max_offset = article.get('data-offset')
        return max_offset
      


root = tk.Tk()
app = News_GUI(root)
root.mainloop()    