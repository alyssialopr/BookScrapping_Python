from bs4 import BeautifulSoup
import requests
import csv


url = 'http://books.toscrape.com/'
def get_book(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    book = soup.select('article > div > a')[2]['href']
    print(url + book)

    product_page_url = url + book
    book_url = requests.get(product_page_url)
    soup = BeautifulSoup(book_url.text, 'html.parser')
    upc = soup.find('td').text
    title = soup.h1.text
    price_including_tax = soup.find_all('td')[3].text
    price_excluding_tax = soup.find_all('td')[2].text
    number_available = soup.find_all('td')[5].text
    product_description = soup.find_all('p')[3].text
    category = soup.find_all('a')[3].text
    review_rating = soup.find('p', class_='star-rating')['class'][1]
    image_url = soup.find('img')['src']

    with open('csv/princess_between_worlds.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({
            'product_page_url': product_page_url, 
            'upc': upc, 'title':title, 
            'price_including_tax':price_including_tax , 
            'price_excluding_tax' : price_excluding_tax, 
            'number_available' : number_available , 
            'product_description' : product_description, 
            'category': category ,  
            'review_rating' : review_rating ,
            'image_url' : image_url})

get_book(url)

# def get_books_from_category():
#     category_url = url + soup.select('ul > li > a')[3]['href']

#     for i in range(len())


# get_books_from_category()