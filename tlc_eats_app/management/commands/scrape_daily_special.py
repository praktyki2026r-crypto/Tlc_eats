from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from tlc_eats_app.models import Restaurant, DailySpecial
import time
import datetime

KEYWORDS = ['danie dnia', 'dzisiaj polecamy', 'dziś polecamy', 
            'specjalność dnia', 'today special', 'menu dnia']

class Command(BaseCommand):
    help = 'Scrape daily specials from restaurant Facebook pages'

    def handle(self, *args, **kwargs):
        restaurants = Restaurant.objects.filter(facebook_url__isnull=False).exclude(facebook_url='')
        
        if not restaurants:
            self.stdout.write(self.style.WARNING('Brak restauracji z podanym URL Facebook'))
            return

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')           # bez okna przeglądarki
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
        time.sleep(5)  # czekaj na załadowanie strony

        # zamknij popup z cookies jeśli się pojawi
        try:
            cookie_btn = driver.find_element(By.XPATH, '//button[contains(text(), "Zezwól")]')
            cookie_btn.click()
            time.sleep(2)
        except:
            pass

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        posts = soup.find_all('div', {'data-ad-comet-preview': 'message'})

        if not posts:
            # alternatywny selektor
            posts = soup.find_all('div', {'dir': 'auto'})

        today = datetime.date.today()

        for post in posts[:5]:  # sprawdź 5 najnowszych postów
            text = post.get_text().lower()
            for keyword in KEYWORDS:
                if keyword in text:
                    # sprawdź czy już mamy danie dnia na dziś
                    exists = DailySpecial.objects.filter(
                        restaurant=restaurant,
                        date=today
                    ).exists()

                    if not exists:
                        DailySpecial.objects.create(
                            restaurant=restaurant,
                            name='Danie dnia',
                            description=post.get_text()[:500],
                            source_url=restaurant.facebook_url
                        )
                        self.stdout.write(
                            self.style.SUCCESS(f'Zapisano danie dnia dla {restaurant.name}!')
                        )
                    return