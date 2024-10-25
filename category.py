import os
import csv
import requests
from bs4 import BeautifulSoup

if not os.path.exists('csv'):
    os.makedirs('csv')

url_home = 'http://books.toscrape.com/'
url_catalogue = 'http://books.toscrape.com/catalogue/'

def get_book(book_url):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    book_data = soup.select('td')

    # Vérification des éléments avant l'extraction
    try:
        upc = book_data[0].text if len(book_data) > 0 else "N/A"
        title = soup.h1.text if soup.h1 else "N/A"
        price_including_tax = book_data[3].text.replace('Â', '') if len(book_data) > 3 else "N/A"
        price_excluding_tax = book_data[2].text.replace('Â', '') if len(book_data) > 2 else "N/A"
        number_available = book_data[5].text if len(book_data) > 5 else "N/A"
        product_description = soup.select_one('#product_description ~ p').text if soup.select_one('#product_description ~ p') else "N/A"
        category = soup.select('ul.breadcrumb li a')[-1].text.strip() if soup.select('ul.breadcrumb li a') else "N/A"
        review_rating = soup.find('p', class_='star-rating')['class'][1] if soup.find('p', class_='star-rating') else "No rating"
        image_url = url_home + soup.select_one('.item.active img')['src'].replace('../', '') if soup.select_one('.item.active img') else "N/A"

        return {
            'product_page_url': book_url, 
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
    except Exception as e:
        print(f"Erreur lors de l'extraction des données pour le livre {book_url}: {e}")
        return None

def get_Books_from_category(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    all_books = []

    while True:
        books = soup.select('h3 > a')
        for book in books:
            book_url = url_catalogue + book['href'].replace('../../../', '')
            book_data = get_book(book_url)
            if book_data:  # Ajouter le livre seulement s'il a des données
                all_books.append(book_data)

        # Suivre le lien "Next" pour la page suivante
        next_button = soup.find('li', class_='next')
        if next_button:
            next_page_url = url_home + next_button.find('a')['href']
            response = requests.get(next_page_url)
            soup = BeautifulSoup(response.text, 'html.parser')
        else:
            break

    return all_books

def get_all_books_from_all_category():
    response = requests.get(url_home)
    soup = BeautifulSoup(response.content, 'html.parser')
    categories = soup.select('ul > li > ul > li > a')

    for category in categories:
        category_name = category.text.strip()
        category_url = url_home + category['href']

        # Assurer la création du dossier pour chaque catégorie
        category_dir = 'csv/category'
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
        category_filename = f'{category_dir}/{category_name}.csv'

        # Récupérer et enregistrer les données des livres dans la catégorie
        print(f"Téléchargement de la catégorie : {category_name}")
        all_books = get_Books_from_category(category_url)

        with open(category_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_books)

        print(f"{category_name} téléchargé avec succès")

# Lancer le processus
get_all_books_from_all_category()
print("Tous les livres ont été téléchargés avec succès !")