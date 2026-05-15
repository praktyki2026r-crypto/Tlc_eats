from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from tlc_eats_app.models import Restaurant, Category, MenuItem, OptionGroup, Option
import urllib.request
import ssl
import re
import time

BASE_URL = 'https://gorlice.klitkauwitka.pl'

CATEGORIES = {
    '2016': 'Pizza',
    '2017': 'Zapiekanki',
    '2018': 'Sałatki',
    '2019': 'Sosy do pizzy',
    '2020': 'Napoje butelkowe',
    '2027': 'Śniadania',
    '2028': 'Frytki',
    '2030': 'Napoje gorące',
    '2033': 'Mrożone napoje',
    '2108': 'Pizza firmowa',
}

class Command(BaseCommand):
    help = 'Scrape menu Klitka u Witka'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='Klitka u Witka')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono Klitka u Witka w bazie!'))
            return

        Category.objects.filter(restaurant=restaurant).delete()
        self.stdout.write('Usunięto stare dane.')

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        for cat_id, cat_name in CATEGORIES.items():
            self.stdout.write(f'\n[Kategoria] {cat_name}')
            category, _ = Category.objects.get_or_create(
                name=cat_name,
                restaurant=restaurant
            )
            page = 1
            while True:
                url = f'{BASE_URL}/food/category/{cat_id}/page-{page}'
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    opener = urllib.request.build_opener(
                        urllib.request.HTTPSHandler(context=ctx)
                    )
                    with opener.open(req) as response:
                        html = response.read().decode('utf-8')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  Błąd pobierania: {e}'))
                    break

                soup = BeautifulSoup(html, 'html.parser')
                items = soup.find_all('div', class_='card-product')
                if not items:
                    items = soup.find_all('div', class_='product-item')
                if not items:
                    break

                for item in items:
                    self._parse_item(item, restaurant, category)

                next_page = soup.find('a', string=str(page + 1))
                if not next_page:
                    break
                page += 1
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('\nGotowe!'))

    def _parse_item(self, item, restaurant, category):
        name_tag = item.find('h3') or item.find('h4') or item.find(class_='product-name')
        if not name_tag:
            return
        name = name_tag.get_text(strip=True)

        item_text = item.get_text(separator='|', strip=True)
        parts = [p.strip() for p in item_text.split('|')]

        # składniki — element po "Skomponuj danie" lub "ulubionych"
        ingredients = ''
        for idx, part in enumerate(parts):
            if 'Skomponuj' in part or 'ulubionych' in part:
                if idx + 1 < len(parts):
                    candidate = parts[idx + 1]
                    if not re.search(r'\d+[.,]\d+\s*zł', candidate) and 'Dodaj' not in candidate:
                        ingredients = candidate
                break

        prices = []
        size_names = []

        i = 0
        while i < len(parts):
            part = parts[i]
            size_match = re.match(r'^(\d+\s*cm|DUŻA|MAŁA|ŚREDNIA|Mała|Duża|Średnia)', part, re.IGNORECASE)
            if size_match and i + 1 < len(parts):
                size_name = size_match.group(1).strip()
                next_part = parts[i + 1]
                if 'opakowanie' in next_part.lower():
                    i += 2
                    continue
                price_match = re.search(r'(\d+[.,]\d+)\s*zł', next_part)
                if price_match:
                    price = float(price_match.group(1).replace(',', '.'))
                    size_names.append(size_name)
                    prices.append(price)
                    i += 2
                    continue
            i += 1

        # sortuj po cenie rosnąco
        if prices and size_names:
            combined = sorted(zip(prices, size_names))
            prices = [p for p, _ in combined]
            size_names = [s for _, s in combined]

        # fallback — pojedyncza cena
        if not prices:
            single = re.search(r'(\d+[.,]\d+)\s*zł', item_text)
            if single:
                prices = [float(single.group(1).replace(',', '.'))]

        if not prices:
            return

        if MenuItem.objects.filter(name=name, restaurant=restaurant).exists():
            self.stdout.write(f'  Już istnieje: {name}')
            return

        base_price = prices[0]
        menu_item = MenuItem.objects.create(
            restaurant=restaurant,
            category=category,
            name=name,
            price=base_price,
            ingredients=ingredients,
        )

        if len(prices) > 1 and size_names:
            group = OptionGroup.objects.create(
                menu_item=menu_item,
                name='Rozmiar',
                type='single',
                required=True,
            )
            for size, price in zip(size_names, prices):
                Option.objects.create(
                    group=group,
                    name=size,
                    extra_price=price - base_price,
                    capacity=size,
                )

        sizes_str = ' / '.join(f'{s}: {p} zł' for s, p in zip(size_names, prices)) if size_names else f'{base_price} zł'
        self.stdout.write(self.style.SUCCESS(f'  Dodano: {name} — {sizes_str}'))