from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from tlc_eats_app.models import Restaurant, Category, MenuItem, OptionGroup, Option
import time
import re

class Command(BaseCommand):
    help = 'Scrape menu Dark Pub'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='Dark Pub')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono Dark Pub w bazie!'))
            return

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        pages = [
            ('Restauracja', 'https://darkpub.pl/menu-restauracji/'),
            ('Pizza', 'https://darkpub.pl/pizza/'),
            ('Napoje', 'https://darkpub.pl/napoje-i-alkohole/', True),
        ]

        for page in pages:
            category_name = page[0]
            url = page[1]
            stop = page[2] if len(page) > 2 else False

            self.stdout.write(f'Scrapuję: {category_name} — {url}')
            driver.get(url)
            time.sleep(4)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            self._parse_menu(soup, restaurant, category_name, stop)

        driver.quit()
        self.stdout.write(self.style.SUCCESS('Gotowe!'))

    def _parse_menu(self, soup, restaurant, category_name, stop_at_kompozycje=False):
        category, _ = Category.objects.get_or_create(
            name=category_name,
            restaurant=restaurant
        )

        if stop_at_kompozycje:
            kompozycje = soup.find('h3', string=lambda t: t and 'Kompozycje' in t)
            if kompozycje:
                for sibling in kompozycje.find_all_next():
                    sibling.decompose()

        items = soup.find_all('li', class_='elementor-price-list-item')

        for item in items:
            name_tag = item.find('span', class_='elementor-price-list-title')
            price_tags = item.find_all('span', class_='elementor-price-list-price')
            desc_tag = item.find('p', class_='elementor-price-list-description')

            if not name_tag or not price_tags:
                continue

            name = name_tag.get_text(strip=True)
            ingredients = desc_tag.get_text(strip=True) if desc_tag else ''

            if MenuItem.objects.filter(name=name, restaurant=restaurant).exists():
                self.stdout.write(f'  Już istnieje: {name}')
                continue

            prices_data = []
            for pt in price_tags:
                text = pt.get_text(strip=True)
                capacity_match = re.search(r'(\d+[.,]?\d*\s*[lL])', text)
                price_match = re.search(r'(\d+[.,]\d+)\s*zł', text)
                if price_match:
                    prices_data.append({
                        'capacity': capacity_match.group(1) if capacity_match else None,
                        'price': float(price_match.group(1).replace(',', '.'))
                    })

            if not prices_data:
                continue

            base_price = prices_data[0]['price']

            menu_item = MenuItem.objects.create(
                restaurant=restaurant,
                category=category,
                name=name,
                price=base_price,
                ingredients=ingredients
            )

            if len(prices_data) > 1:
                group = OptionGroup.objects.create(
                    menu_item=menu_item,
                    name='Rozmiar',
                    type='single',
                    required=True
                )
                for i, pd in enumerate(prices_data):
                    Option.objects.create(
                        group=group,
                        name=pd['capacity'] or f'Rozmiar {i+1}',
                        extra_price=pd['price'] - base_price,
                        capacity=pd['capacity']
                    )

            self.stdout.write(self.style.SUCCESS(f'  Dodano: {name} — {base_price} zł'))