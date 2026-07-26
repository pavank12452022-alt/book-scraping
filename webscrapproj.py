from bs4 import BeautifulSoup
import csv
import requests
# def func(page_num):
#    url="https://books.toscrape.com/catalogue/category/books/mystery_3/page-{}.html".format(page_num)
#    r=requests.get(url)
#    soup=BeautifulSoup(r.text,'lxml')
#    books= soup.find_all('article',class_='product_pod')
#    with open(f'data/booksproj.csv', 'w', newline='', encoding='utf-8') as f:
#        csv_writer=csv.writer(f, delimiter=',')
#        csv_writer.writerow(['Title','Rating','Price'])
#        for book in books:
#              title=book.h3.a['title']
#              rating=book.find('p',class_='star-rating')['class'][1]#here ratings are stored in the class attribute of the p tag with class 'star-rating'. so we can get the rating by getting the second class of the p tag.
#              #space in class attribute is used to separate multiple classes. so we can get the rating
#              price=book.find('p',class_='price_color').text
             

#              csv_writer.writerow([title,rating,price])
#    data_list=[]
#    with open (f'data/booksproj.csv','r',encoding='utf-8') as f:
#        csv_reader=csv.reader(f)
       
#        next(csv_reader)#skip the header row
#        for row in csv_reader:
#           data_list.append({'title':row[0],'rating':row[1],'price':row[2]})      
#    return data_list
     
   
      

#       data_list.append({'title':title,'rating':rating,'price':price})
#    return data_list
def scrape_page(page_num):
   data_list=[]
   url = f"https://books.toscrape.com/catalogue/category/books/mystery_3/page-{page_num}.html"
   r=requests.get(url)
   sou=BeautifulSoup(r.text,'lxml')
   books= sou.find_all('article',class_='product_pod')
   for book in books:
             title=book.h3.a['title']
             rating=book.find('p',class_='star-rating')['class'][1]#here ratings are stored in the class attribute of the p tag with class 'star-rating'. so we can get the rating by getting the second class of the p tag.
             #space in class attribute is used to separate multiple classes. so we can get the rating
             price=book.find('p',class_='price_color').text
             data_list.append({'title':title,'rating':rating,'price':price})
   return data_list
def scrape_all_pages():
   data_list=[]
   for page_num in range(1, 51):
      data_list.extend(scrape_page(page_num))
   return data_list
def csv_load(data_list):
    with open(f'booksproj.csv', 'w', newline='', encoding='utf-8') as f:
        csv_writer=csv.writer(f, delimiter=',')
        csv_writer.writerow(['Title','Rating','Price'])
        for book in data_list:
            csv_writer.writerow([book['title']+'\t',book['rating']+'\t',book['price']])
def csv_read():
    data_list=[]
    with open (f'booksproj.csv','r',encoding='utf-8') as f:
        csv_reader=csv.reader(f)
        next(csv_reader)#skip the header row
        for row in csv_reader:
           data_list.append({'title':row[0],'rating':row[1],'price':row[2]})      
    return data_list
def filter_rating(data_list):
   mapping={'One':1,'Two':2,'Three':3,'Four':4,'Five':5,'1':1,'2':2,'3':3,'4':4,'5':5}
   stars = input("Enter rating: ")
   if stars in mapping:
      stars = mapping[stars]
   for book in data_list:
      if mapping.get(book['rating']) == stars:
            print(f"Title: {book['title']}, Price: {book['price']}, Rating: {book['rating']}")

def price_range(data_list):
   min_price=float(input("Enter the minimum price: "))
   max_price=float(input("Enter the maximum price: "))
   for book in data_list:
      price = float(book['price'].replace('£', '').replace('Â', '').strip())#here we are removing the currency symbol and any whitespace from the price string and converting it to a float for comparison.
      if min_price <= price <= max_price:
         print(f"Title: {book['title']}, Price: {book['price']}, Rating: {book['rating']}") 

def book_search(data_list):
   search=input("Enter the title of the book you want to search: ")
   for book in data_list:
      if search.lower() in book['title'].lower():
         print(f"Title: {book['title']}, Price: {book['price']}, Rating: {book['rating']}")

# if __name__=="__main__":
#     data_list=func()
#     while True:
#         print("1. Filter by rating")
#         print("2. Filter by price range")
#         print("3. Search by title")
#         print("4. Exit")
#         try:
#             choice = int(input("Enter your choice: "))
#         except ValueError:
#              print("Enter a valid number")
#              continue
#         if choice == 1:
#             filter_rating(data_list)
#         elif choice == 2:
#             price_range(data_list)
#         elif choice == 3:
#             book_search(data_list)
#         elif choice == 4:
#             break
#         else:
#             print("Invalid choice")
import os

if __name__ == "__main__":
    if not os.path.exists('booksproj.csv'):
        data_list = scrape_all_pages()
        csv_load(data_list)
    else:
        data_list = csv_read()

    while True:
        print("1. Filter by rating")
        print("2. Filter by price range")
        print("3. Search by title")
        print("4. Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Enter a valid number")
            continue

        if choice == 1:
            filter_rating(data_list)
        elif choice == 2:
            price_range(data_list)
        elif choice == 3:
            book_search(data_list)
        elif choice == 4:
            break
        else:
            print("Invalid choice")