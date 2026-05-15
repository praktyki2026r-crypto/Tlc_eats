from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from tlc_eats_app.models import Restaurant, Category, MenuItem, OptionGroup, Option
import urllib.request
import ssl

PAGES = [
    'https://www.rafaello.gorlice.pl/',
    'https://www.rafaello.gorlice.pl/cienkie_ciasto.php',
    'https://www.rafaello.gorlice.pl/dodatki.php',
]

SIZE_NAMES = ['Mała', 'Średnia', 'Duża', 'Bardzo duża']

class Command(BaseCommand):
    help = 'Scrape menu Rafaello'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='Rafaello')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono Rafaello w bazie!'))
            return

        Category.objects.filter(restaurant=restaurant).delete()
        self.stdout.write('Usunięto stare dane.')

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        for url in PAGES:
            self.stdout.write(f'\nPobieram: {url}')
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
            try:
                with opener.open(req) as response:
                    html = response.read().decode('utf-8')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Błąd: {e}'))
                continue

            soup = BeautifulSoup(html, 'html.parser')
            self._parse_menu(soup, restaurant)

        self.stdout.write(self.style.SUCCESS('\nGotowe!'))

    def _parse_menu(self, soup, restaurant):
        current_category = None
        seen_in_this_page = set()  # ← śledź dania na tej stronie

        for tag in soup.find_all(['span', 'tr']):
            if tag.name == 'span' and tag.get('class') == ['header']:
                cat_name = tag.get_text(strip=True).rstrip(':')
                current_category, _ = Category.objects.get_or_create(
                    name=cat_name,
                    restaurant=restaurant
                )
                self.stdout.write(f'\n[Kategoria] {cat_name}')
                seen_in_this_page = set()  # reset przy nowej kategorii
                continue

            if tag.name == 'tr' and current_category:
                name_tag = tag.find('strong')
                if not name_tag:
                    continue

                name = name_tag.get_text(strip=True)
                if not name:
                    continue

                # pomiń duplikaty na tej samej stronie
                if name in seen_in_this_page:
                    continue
                seen_in_this_page.add(name)

                # składniki
                ingredients = ''
                for content in name_tag.next_siblings:
                    text = str(content).strip()
                    if text and not text.startswith('<'):
                        ingredients = text.strip()
                        break

                # ceny
                price_cells = tag.find_all('td', class_='ceny')
                prices = []
                for cell in price_cells:
                    text = cell.get_text(strip=True).replace(',', '.')
                    try:
                        prices.append(float(text))
                    except ValueError:
                        continue

                if not prices:
                    continue

                if MenuItem.objects.filter(name=name, restaurant=restaurant).exists():
                    self.stdout.write(f'  Już istnieje: {name}')
                    continue

                base_price = prices[0]
                menu_item = MenuItem.objects.create(
                    restaurant=restaurant,
                    category=current_category,
                    name=name,
                    price=base_price,
                    ingredients=ingredients,
                )

                if len(prices) > 1:
                    group = OptionGroup.objects.create(
                        menu_item=menu_item,
                        name='Rozmiar',
                        type='single',
                        required=True,
                    )
                    for i, price in enumerate(prices):
                        size_name = SIZE_NAMES[i] if i < len(SIZE_NAMES) else f'Rozmiar {i+1}'
                        Option.objects.create(
                            group=group,
                            name=size_name,
                            extra_price=price - base_price,
                        )

                if len(prices) > 1:
                    sizes_str = ' / '.join(
                        f'{SIZE_NAMES[i] if i < len(SIZE_NAMES) else i+1}: {p} zł'
                        for i, p in enumerate(prices)
                    )
                else:
                    sizes_str = f'{prices[0]} zł'

                self.stdout.write(self.style.SUCCESS(f'  Dodano: {name} — {sizes_str}'))