from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from tlc_eats_app.models import Restaurant, Category, MenuItem
import time

class Command(BaseCommand):
    help = 'Scrape menu Bar Wojtek'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='Bar Wojtek')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono Bar Wojtek w bazie!'))
            return

        Category.objects.filter(restaurant=restaurant).delete()
        self.stdout.write('Usunięto stare dane.')

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        url = 'https://barwojtekgorlice.pl/section:menu/polecane'
        self.stdout.write(f'Pobieram: {url}')
        driver.get(url)
        time.sleep(5)

        # przewiń stronę żeby załadować wszystkie dania
        last_height = driver.execute_script('return document.body.scrollHeight')
        while True:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(2)
            new_height = driver.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                break
            last_height = new_height

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        self._parse_menu(soup, restaurant)
        self.stdout.write(self.style.SUCCESS('Gotowe!'))

    def _parse_menu(self, soup, restaurant):
        current_category = None

        # znajdź wszystkie kategorie i dania
        for tag in soup.find_all(['div']):
            # kategoria
            if 'categoryName' in ' '.join(tag.get('class', [])):
                cat_name = tag.get_text(strip=True)
                if cat_name:
                    current_category, _ = Category.objects.get_or_create(
                        name=cat_name,
                        restaurant=restaurant
                    )
                    self.stdout.write(f'\n[Kategoria] {cat_name}')
                continue

            # danie
            if 'menu-item-title' in ' '.join(tag.get('class', [])) and current_category:
                name = tag.get_text(strip=True)
                if not name:
                    continue

                # cena — szukaj w następnym rodzeństwie
                price = 0
                price_tag = tag.find_next('div', attrs={'data-price': True})
                if price_tag:
                    try:
                        price = float(price_tag.get('data-price'))
                    except ValueError:
                        pass

                # składniki
                ingredients = ''
                desc_tag = tag.find_next('pre')
                if desc_tag:
                    ingredients = desc_tag.get_text(strip=True)

                if MenuItem.objects.filter(name=name, restaurant=restaurant).exists():
                    self.stdout.write(f'  Już istnieje: {name}')
                    continue

                MenuItem.objects.create(
                    restaurant=restaurant,
                    category=current_category,
                    name=name,
                    price=price,
                    ingredients=ingredients,
                )

                self.stdout.write(self.style.SUCCESS(f'  Dodano: {name} — {price} zł'))
                