from bs4 import BeautifulSoup
import requests
import csv
import os

if not os.path.exists('book_img'):
    os.makedirs('book_img')

# Phase 1 :  Récuperer les données d'un livre
if not os.path.exists('csv'):
    os.makedirs('csv')


url = 'http://books.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

base_url = 'http://books.toscrape.com/' 

url_home = 'http://books.toscrape.com/catalogue/'

def get_book(soup, url):
    product_page_url = url
    response = requests.get(product_page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    book_data = soup.select('td')

    upc = book_data[0].text
    title = soup.h1.text
    price_including_tax = soup.find_all('td')[3].text.replace('Â', '')
    price_excluding_tax = soup.find_all('td')[2].text.replace('Â', '')
    number_available = soup.find_all('td')[5].text
    product_description = soup.find_all('p')[3].text
    category = soup.find_all('a')[3].text
    review_rating = soup.find_all("p", class_="star-rating")[0]['class'][1]
    image_url = base_url + soup.select("img")[0]["src"].replace('../../', '')
    # print(image_url)

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

# get_book(soup, url)

# Phase 2 : Récuperer les données de tout les livres d'une catégorie

def download_images(X, filename):
    # books_img_urls = [url + img["src"].replace('../../', '') for img in soup.select("img")]
    # print(books_img_urls)
    # for img_url in books_img_urls:
    #     response = requests.get(img_url)
        # filename = 'book_img/' + img_url.split('/')[-1]

    try:
        response = requests.get(str(X))
        soup_image = BeautifulSoup(response.content, 'html.parser')
        # print(soup_image)
        print(response)
        print('book_img/' + filename)
        print(X)
        with open('book_img/' + filename + '.jpg', 'wb') as file:
            file.write(response.content)
        print('Image downloaded')
    except:
        print('Error')

def get_Books_from_category(soup, url, category_number):
    url_category = url + soup.select('ul > li > a')[category_number]['href']
    response = requests.get(url_category)
    soup = BeautifulSoup(response.content, 'html.parser')

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
            soup = BeautifulSoup(response.content, 'html.parser')

        else :
            break

    with open('csv/category.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for book in all_books:
            writer.writerow(book)
            download_images(book['image_url'], book['title'])


url = 'http://books.toscrape.com/'

get_Books_from_category(soup, url, 4)


# Phase 3 : Récupérer les images de chaque livres de la même catégorie et les télécharger dans un dossier

# books_img_urls = [url + img["src"].replace('../../', '') for img in soup.select("img")]
# print(books_img_urls)

# for book_img_url in books_img_urls:
#     response = requests.get(book_img_url)
#     # filename = 'book_img/' + book_img_url.split('/')[-1]
#     # filename = 'book_img/' + book_title 
#     # download_images(book_img_url, filename)
