from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from tlc_eats_app.models import Restaurant, Category, MenuItem, OptionGroup, Option
import time

class Command(BaseCommand):
    help = 'Scrape menu Kebab u Pajdy'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='Kebab u Pajdy')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono Kebab u Pajdy w bazie!'))
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

        url = 'https://www.upajdygorlice.pl/restauracja/kebab-u-pajdy-gorlice'
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
       
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # ← dodaj te 3 linie tutaj
        with open('kebabupajdy_debug.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        self.stdout.write('Zapisano HTML do kebabupajdy_debug.html')
        
        

        driver.quit()

        self._parse_menu(soup, restaurant)
        self.stdout.write(self.style.SUCCESS('Gotowe!'))

    def _parse_menu(self, soup, restaurant):
        current_category = None

        for tag in soup.find_all(['span', 'h4']):
            # kategoria
            if tag.name == 'span' and 'm-list__title-text' in tag.get('class', []):
                cat_name = tag.get_text(strip=True)
                if cat_name:
                    current_category, _ = Category.objects.get_or_create(
                        name=cat_name,
                        restaurant=restaurant
                    )
                    self.stdout.write(f'\n[Kategoria] {cat_name}')
                continue

            # danie
            if tag.name == 'h4' and 'restaurant-menu__dish-name' in tag.get('class', []) and current_category:
                name = tag.get_text(strip=True)
                if not name:
                    continue

                # cena
                price = 0
                price_tag = tag.find_next('span', string=lambda t: t and 'zł' in t)
                if price_tag:
                    price_text = price_tag.get_text(strip=True).replace('\xa0', '').replace('zł', '').replace(',', '.').strip()
                    try:
                        price = float(price_text)
                    except ValueError:
                        pass

                if MenuItem.objects.filter(name=name, restaurant=restaurant).exists():
                    self.stdout.write(f'  Już istnieje: {name}')
                    continue

                menu_item = MenuItem.objects.create(
                    restaurant=restaurant,
                    category=current_category,
                    name=name,
                    price=price,
                )

                # opcje — mięso, sos, dodatki
                for section in tag.find_all_next('h3', class_='h4'):
                    next_dish = section.find_previous('h4', class_='restaurant-menu__dish-name')
                    if next_dish != tag:
                        break

                    group_name = section.get_text(strip=True).rstrip(':')
                    choices = section.find_all_next('span', class_='u-text-break')
                    if not choices:
                        continue

                    group = OptionGroup.objects.create(
                        menu_item=menu_item,
                        name=group_name,
                        type='single',
                        required=False,
                    )
                    for choice in choices:
                        option_name = choice.get_text(strip=True)
                        if option_name:
                            Option.objects.create(
                                group=group,
                                name=option_name,
                                extra_price=0,
                            )

                self.stdout.write(self.style.SUCCESS(f'  Dodano: {name} — {price} zł'))