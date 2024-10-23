from bs4 import BeautifulSoup
import requests
import csv
import os

if not os.path.exists('csv'):
    os.makedirs('csv')

url = 'http://books.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

url_home = 'http://books.toscrape.com/catalogue/'

def get_book(soup, url):
    product_page_url = url
    response = requests.get(product_page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    book_data = soup.select('td')

    upc = book_data[0].text
    title = soup.h1.text
    price_including_tax = soup.find_all('td')[3].text.replace('Â', '')
    price_excluding_tax = soup.find_all('td')[2].text.replace('Â', '')
    number_available = soup.find_all('td')[5].text
    product_description = soup.find_all('p')[3].text
    category = soup.find_all('a')[3].text
    review_rating = soup.find_all("p", class_="star-rating")[0]['class'][1]
    image_url = url_home + soup.select("img")[0]["src"].replace('../../', '')

    return {
        'product_page_url': product_page_url, 
        'upc': upc, 
        'title': title, 
        'price_including_tax': price_including_tax, 
        'price_excluding_tax': price_excluding_tax, 
        'number_available': number_available, 
        'product_description': product_description, 
        'category': category,  
        'review_rating': review_rating,
        'image_url': image_url
    }

def get_Books_from_category(soup, url, category_number):
    url_category = url + soup.select('ul > li > a')[category_number]['href']
    response = requests.get(url_category)
    soup = BeautifulSoup(response.text, 'html.parser')

    all_books = []

    while True:
            
        books = soup.select('h3 > a')
        for book in books:
            book_url = url_home + book['href'].replace('../../../', '')
            book_data = get_book(soup, book_url)
            all_books.append(book_data)

        next = soup.find('li', class_='next')
        if next :
            next_page_url = next.find('a')['href']
            response = requests.get(url_category.replace('index.html', next_page_url))
            soup = BeautifulSoup(response.text, 'html.parser')

        else :
            break

    with open('csv/category.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for book in all_books:
            writer.writerow(book)

url = 'http://books.toscrape.com/'

get_Books_from_category(soup, url, 4)