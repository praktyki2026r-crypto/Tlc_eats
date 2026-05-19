from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from tlc_eats_app.models import Restaurant, DailySpecial, Category, MenuItem, OptionGroup, Option
import time
import datetime
import re

KEYWORDS = ['danie dnia', 'dzisiaj polecamy', 'dziś polecamy',
            'specjalność dnia', 'today special', 'menu dnia',
            'lunch dnia', 'zestaw 1', 'poniedziałek', 'wtorek',
            'środa', 'czwartek', 'piątek', 'sobota', 'niedziela']

class Command(BaseCommand):
    help = 'Scrape daily specials from restaurant Facebook pages'

    def handle(self, *args, **kwargs):
        restaurants = Restaurant.objects.filter(
            name__in=['New York']
        )
        if not restaurants:
            self.stdout.write(self.style.WARNING('Brak restauracji'))
            return

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--lang=pl')

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        for restaurant in restaurants:
            self.stdout.write(f'Scrapuję: {restaurant.name} — {restaurant.facebook_url}')
            try:
                self._scrape_restaurant(driver, restaurant)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Błąd dla {restaurant.name}: {e}'))

        driver.quit()
        self.stdout.write(self.style.SUCCESS('Gotowe!'))

    def _scrape_restaurant(self, driver, restaurant):
        driver.get(restaurant.facebook_url)
        time.sleep(5)

        try:
            cookie_btn = driver.find_element(By.XPATH, '//button[contains(text(), "Zezwól")]')
            cookie_btn.click()
            time.sleep(2)
        except:
            pass

        try:
            time.sleep(3)
            see_more_buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
            for btn in see_more_buttons:
                if 'więcej' in btn.text.lower() or 'see more' in btn.text.lower():
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(2)
        except:
            pass

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        posts = soup.find_all('div', {'data-ad-comet-preview': 'message'})
        if not posts:
            posts = soup.find_all('div', {'dir': 'auto'})

        today = datetime.date.today()

        for post in posts[:5]:
            text = post.get_text()
            text_lower = text.lower()
            for keyword in KEYWORDS:
                if keyword in text_lower:
                    DailySpecial.objects.filter(restaurant=restaurant, date=today).delete()
                    DailySpecial.objects.create(
                        restaurant=restaurant,
                        name='Danie dnia',
                        description=text[:500],
                        source_url=restaurant.facebook_url
                    )
                    self._parse_and_save(text, restaurant)
                    self.stdout.write(self.style.SUCCESS(f'Zapisano danie dnia dla {restaurant.name}!'))
                    return

    def _parse_and_save(self, text, restaurant):
        category, _ = Category.objects.get_or_create(
            restaurant=restaurant,
            name='Danie dnia'
        )
        # usuń stare itemy i ich opcje
        old_items = MenuItem.objects.filter(restaurant=restaurant, category=category)
        for item in old_items:
            OptionGroup.objects.filter(menu_item=item).delete()
        old_items.delete()

        # wyciągnij cenę zestawu (z zupą)
        price_zestaw = 0.0
        m = re.search(r'ZESTAW\s*\(zupa.*?\)\s*(\d+)\s*zł', text, re.IGNORECASE)
        if m:
            price_zestaw = float(m.group(1))

        # wyciągnij cenę dania (bez zupy)
        price_danie = 0.0
        m = re.search(r'DANIE DNIA.*?(\d+)\s*zł', text, re.IGNORECASE)
        if m:
            price_danie = float(m.group(1))

        # wyciągnij wszystkie zestawy
        zestawy = re.findall(r'Zestaw\s*\d+\s*:(.*?)(?=Zestaw\s*\d+\s*:|DANIE DNIA|$)', text, re.IGNORECASE)

        for skladniki in zestawy:
            skladniki = skladniki.strip()
            if not skladniki:
                continue
            parts = [p.strip() for p in skladniki.split('+')]
            # pomijamy zupę (pierwsza część)
            danie_parts = parts[1:] if len(parts) > 1 else parts
            name = ' + '.join(danie_parts)[:200]

            item = MenuItem.objects.create(
                restaurant=restaurant,
                category=category,
                name=name,
                price=price_danie,  # cena bazowa = bez zupy
                ingredients=skladniki,
                is_available=True,
            )

            # OptionGroup — wybór zupy
            group = OptionGroup.objects.create(
                menu_item=item,
                name='Zestaw',
                type='single',
                required=True,
            )

            Option.objects.create(
                group=group,
                name='Bez zupy',
                extra_price=0,
            )
            Option.objects.create(
                group=group,
                name='Z zupą',
                extra_price=round(price_zestaw - price_danie, 2),
            )

            self.stdout.write(f'  Dodano: {name} — {price_danie} zł / {price_zestaw} zł z zupą')