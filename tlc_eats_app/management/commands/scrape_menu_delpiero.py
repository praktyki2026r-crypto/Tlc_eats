from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem, OptionGroup, Option
import pdfplumber
import re
import urllib.request
import os
import tempfile

PDF_URL = 'https://delpiero.gorlice.pl/wp-content/uploads/2026/02/menu-delpiero-2026-bez-grubych.pdf'

# Tylko te kategorie nas interesują
CATEGORIES = {
    'CIENKIE CIASTO': 'Pizza',
    'MAKARONY': 'Makarony',
    'PANOZZO': 'Panozzo',
    'PRZYSTAWKI': 'Przystawki',
    'ZUPY': 'Zupy',
    'DANIA GŁÓWNE': 'Dania główne',
    'SAŁATKI': 'Sałatki',
    'NA SŁODKO': 'Na słodko',
    'DODATKI': 'Dodatki',
    'NAPOJE GORĄCE': 'Napoje gorące',
    'NAPOJE': 'Napoje',
}

# Te kategorie pomijamy w całości
SKIP_CATEGORIES = [
    'PIWO', 'WINO', 'DRINKI', 'DRINKI BEZALKOHOLOWE', 'ALKOHOLE'
]

IGNORE_LINES = [
    'menu', 'pizza', 'włoska', 'polska', 'fast-food', 'napoje gorące',
    'napoje', 'piwo i wino', 'drinki bezalkoholowe', 'drinki', 'porcja',
    'przy zwiększonym', 'zamówienia przyjmujemy', 'o chęci dzielenia',
    'restauracja włoska', 'czyli kulinarne', 'pizza pół na pół',
]

class Command(BaseCommand):
    help = 'Scrape menu Del Piero z PDF'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='Del Piero')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono Del Piero w bazie!'))
            return

        self.stdout.write('Pobieram PDF...')
        tmp_path = os.path.join(tempfile.gettempdir(), 'del_piero_menu.pdf')
        try:
            # pomijamy weryfikację SSL (certyfikat strony jest nieprawidłowy)
            import ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            import urllib.request
            opener = urllib.request.build_opener(
                urllib.request.HTTPSHandler(context=ctx)
            )
            with opener.open(PDF_URL) as response:
                with open(tmp_path, 'wb') as f:
                    f.write(response.read())

            self.stdout.write('PDF pobrany, przetwarzam...')
            self._parse_pdf(tmp_path, restaurant)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        self.stdout.write(self.style.SUCCESS('Gotowe!'))

    def _parse_pdf(self, pdf_path, restaurant):
        current_category = None
        skip_mode = False       # True gdy jesteśmy w kategorii alkoholowej
        pizza_mode = False      # True gdy przetwarzamy pizzę (3 rozmiary)

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue

                lines = [l.strip() for l in text.split('\n') if l.strip()]

                i = 0
                while i < len(lines):
                    line = lines[i]
                    line_upper = line.upper()

                    # sprawdź czy to nagłówek kategorii do pominięcia
                    if any(skip in line_upper for skip in SKIP_CATEGORIES):
                        skip_mode = True
                        current_category = None
                        pizza_mode = False
                        i += 1
                        continue

                    # sprawdź czy to nagłówek kategorii którą chcemy
                    matched = self._match_category(line_upper)
                    if matched:
                        skip_mode = False
                        pizza_mode = matched == 'CIENKIE CIASTO'
                        current_category, _ = Category.objects.get_or_create(
                            name=CATEGORIES[matched],
                            restaurant=restaurant
                        )
                        self.stdout.write(f'\n[Kategoria] {CATEGORIES[matched]}')
                        i += 1
                        continue

                    # jesteśmy w kategorii alkoholowej – pomijamy
                    if skip_mode:
                        i += 1
                        continue

                    # brak aktywnej kategorii
                    if current_category is None:
                        i += 1
                        continue

                    # pomiń linie nagłówkowe i stopki
                    if self._should_ignore(line):
                        i += 1
                        continue

                    # pomiń nagłówek rozmiarów pizzy
                    if re.match(r'^23cm\s+30cm\s+40cm', line):
                        i += 1
                        continue

                    # PIZZA – 3 rozmiary
                    if pizza_mode:
                        skip = self._parse_pizza(lines, i, restaurant, current_category)
                        if skip:
                            i += skip
                            continue

                    # ZWYKŁE DANIE – 1 lub 2 ceny
                    skip = self._parse_item(lines, i, restaurant, current_category)
                    if skip:
                        i += skip
                        continue

                    i += 1

    def _match_category(self, line_upper):
        for key in CATEGORIES:
            if key in line_upper:
                return key
        return None

    def _should_ignore(self, line):
        line_lower = line.lower().strip()
        for ig in IGNORE_LINES:
            if ig in line_lower:
                return True
        if re.match(r'^[\d\s,\.lcm/]+$', line_lower):
            return True
        return False

    def _get_ingredients(self, lines, i):
        """Pobiera składniki z następnej linii jeśli nie jest ceną/nagłówkiem."""
        if i + 1 < len(lines):
            next_line = lines[i + 1]
            if (not re.match(r'^[\d\s]+$', next_line)
                    and not self._match_category(next_line.upper())
                    and not self._should_ignore(next_line)
                    and not any(s in next_line.upper() for s in SKIP_CATEGORIES)):
                return next_line, 2
        return '', 1

    def _parse_pizza(self, lines, i, restaurant, category):
        line = lines[i]
        # usuń emoji
        line_clean = re.sub(r'[^\w\s\-]', '', line).strip()

        # "Nazwa  23  32  47"
        match3 = re.match(r'^(.+?)\s+(\d{2})\s+(\d{2})\s+(\d{2,3})\s*$', line_clean)
        if match3:
            name = match3.group(1).strip()
            p23 = float(match3.group(2))
            p30 = float(match3.group(3))
            p40 = float(match3.group(4))
            ingredients, skip = self._get_ingredients(lines, i)
            self._save_pizza(name, ingredients, p23, p30, p40, restaurant, category)
            return skip

        # pizze z jedną ceną (Szkolna 40cm=47, Familijna 50cm=61, Zawał=35, Calzone=36)
        match1 = re.match(r'^(.+?)\s+(\d{2,3})\s*$', line_clean)
        if match1:
            name = match1.group(1).strip()
            price = float(match1.group(2))
            ingredients, skip = self._get_ingredients(lines, i)
            self._save_item(name, ingredients, price, restaurant, category)
            return skip

        return None

    def _parse_item(self, lines, i, restaurant, category):
        line = lines[i]
        line_clean = re.sub(r'[^\w\s\-]', '', line).strip()

        # 2 ceny (np. napoje 0,25l i 0,5l)
        match2 = re.match(r'^(.+?)\s+(\d+)\s+(\d+)\s*$', line_clean)
        if match2:
            name = match2.group(1).strip()
            p1 = float(match2.group(2))
            p2 = float(match2.group(3))
            ingredients, skip = self._get_ingredients(lines, i)
            self._save_item_two_prices(name, ingredients, p1, p2, restaurant, category)
            return skip

        # 1 cena
        match1 = re.match(r'^(.+?)\s+(\d+)\s*$', line_clean)
        if match1:
            name = match1.group(1).strip()
            price = float(match1.group(2))
            ingredients, skip = self._get_ingredients(lines, i)
            self._save_item(name, ingredients, price, restaurant, category)
            return skip

        return None

    def _save_pizza(self, name, ingredients, p23, p30, p40, restaurant, category):
        if MenuItem.objects.filter(name=name, restaurant=restaurant).exists():
            self.stdout.write(f'  Już istnieje: {name}')
            return

        item = MenuItem.objects.create(
            restaurant=restaurant,
            category=category,
            name=name,
            price=p23,
            ingredients=ingredients,
        )
        group = OptionGroup.objects.create(
            menu_item=item,
            name='Rozmiar',
            type='single',
            required=True,
        )
        Option.objects.create(group=group, name='23cm', extra_price=0)
        Option.objects.create(group=group, name='30cm', extra_price=p30 - p23)
        Option.objects.create(group=group, name='40cm', extra_price=p40 - p23)
        self.stdout.write(self.style.SUCCESS(f'  Dodano: {name} — {p23}/{p30}/{p40} zł'))

    def _save_item(self, name, ingredients, price, restaurant, category):
        if MenuItem.objects.filter(name=name, restaurant=restaurant).exists():
            self.stdout.write(f'  Już istnieje: {name}')
            return
        MenuItem.objects.create(
            restaurant=restaurant,
            category=category,
            name=name,
            price=price,
            ingredients=ingredients,
        )
        self.stdout.write(self.style.SUCCESS(f'  Dodano: {name} — {price} zł'))

    def _save_item_two_prices(self, name, ingredients, p1, p2, restaurant, category):
        if MenuItem.objects.filter(name=name, restaurant=restaurant).exists():
            self.stdout.write(f'  Już istnieje: {name}')
            return
        item = MenuItem.objects.create(
            restaurant=restaurant,
            category=category,
            name=name,
            price=p1,
            ingredients=ingredients,
        )
        group = OptionGroup.objects.create(
            menu_item=item,
            name='Rozmiar',
            type='single',
            required=True,
        )
        Option.objects.create(group=group, name='Mały', extra_price=0)
        Option.objects.create(group=group, name='Duży', extra_price=p2 - p1)
        self.stdout.write(self.style.SUCCESS(f'  Dodano: {name} — {p1}/{p2} zł'))