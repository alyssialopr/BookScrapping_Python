from bs4 import BeautifulSoup
import requests
import csv

#  Phase 1 : Extraction des données des pages produits : Princess Between Worlds (Wide-Awake Princess #5)

url = "https://books.toscrape.com/catalogue/princess-between-worlds-wide-awake-princess-5_919/index.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


# product page url
product_page_url = url
# print(product_page_url)

# universal product code (upc)
upc = soup.find('td').text
# print(upc)

# title
title = soup.h1.text
# print(title)

# price including tax
price_including_tax = soup.find_all('td')[3].text
# print(price_including_tax)

# price excluding tax
price_excluding_tax = soup.find_all('td')[2].text
# print(price_excluding_tax)

# number available
number_available = soup.find_all('td')[5].text
# print(number_available)

# product description
product_description = soup.find_all('p')[3].text
# print(product_description)

# category
category = soup.find_all('a')[3].text
# print(category)

# review rating
review_rating = soup.find('p', class_='star-rating')['class'][1]
# print(review_rating)

# image url
image_url = soup.find('img')['src']
# print(image_url)


with open('princess_between_worlds.csv', 'w', newline='', encoding='utf-8') as csvfile:
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