from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem, OptionGroup, Option
import pdfplumber
import re
import ssl
import urllib.request
import os
import tempfile

PDF_URL = 'https://delpiero.gorlice.pl/wp-content/uploads/2026/02/menu-delpiero-2026-bez-grubych.pdf'

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
    'FAST-FOOD': 'Fast Food',
    'NAPOJE GORĄCE': 'Napoje gorące',
    'NAPOJE': 'Napoje',
    
}

SKIP_CATEGORIES = [
    'PIWO', 'WINO', 'DRINKI BEZALKOHOLOWE', 'DRINKI', 'ALKOHOLE', 'PIWO I WINO'
]

IGNORE_PATTERNS = [
    r'^menu$',
    r'^pizza$',
    r'^włoska$',
    r'^polska$',
    r'^piwo i wino$',
    r'^drinki bezalkoholowe$',
    r'^drinki$',
    r'^porcja .+$',
    r'^przy zwiększonym',
    r'^zamówienia przyjmujemy',
    r'^o chęci dzielenia',
    r'^restauracja włoska',
    r'^czyli kulinarne',
    r'^pizza pół na pół',
    r'^23cm\s+30cm\s+40cm',
    r'^0,25l\s+0,5l',
    r'^40ml\s+0,5l',
    r'^0,3l\s+0,5l',
    r'^napoje gorące—*$',
    r'^fast-food—*$',
    r'^napoje gorące wloska$'
]

class Command(BaseCommand):
    help = 'Scrape menu Del Piero z PDF'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='Del Piero')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono Del Piero w bazie!'))
            return

        # usuń stare dane
        Category.objects.filter(restaurant=restaurant).delete()
        self.stdout.write('Usunięto stare dane.')

        self.stdout.write('Pobieram PDF...')
        tmp_path = os.path.join(tempfile.gettempdir(), 'del_piero_menu.pdf')
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
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
        skip_mode = False
        pizza_mode = False

        all_lines = []
        with pdfplumber.open(pdf_path) as pdf:
            self.stdout.write(f'Liczba stron: {len(pdf.pages)}')
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    lines = text.split('\n') 

                    # strona 7 to fast-food nie ma nagłówka, dodajemy ręcznie
                    if page_num == 7:
                        lines = ['FAST-FOOD'] + lines
                    # strona 8 to kawy nie ma nagłówka, dodajemy ręcznie
                    if page_num == 8:
                        lines = ['NAPOJE GORĄCE'] + lines
                    # strona 9 to napoje zimne
                    if page_num == 9:
                        lines = ['NAPOJE'] + lines
                    for line in lines:
                        line = line.strip()
                        if line:
                            all_lines.append(line)

        i = 0
        while i < len(all_lines):
            line = all_lines[i]
            line_upper = line.upper().strip()

            if any(line_upper == skip or line_upper.startswith(skip) for skip in SKIP_CATEGORIES):
                skip_mode = True
                current_category = None
                pizza_mode = False
                i += 1
                continue

            # stopki stron które wyglądają jak kategorie ale nimi nie są
            # stopki stron – tylko te które NIE są kategoriami w CATEGORIES
            FOOTER_STOPWORDS = ['PIZZA', 'WŁOSKA', 'POLSKA', 'PIWO I WINO']
            if any(line_upper == fw for fw in FOOTER_STOPWORDS):
                i += 1
                continue

            matched = self._match_category(line_upper)
            if matched:
                skip_mode = False
                pizza_mode = matched == 'CIENKIE CIASTO'
                if not (current_category and current_category.name == CATEGORIES[matched]):
                    current_category, _ = Category.objects.get_or_create(
                        name=CATEGORIES[matched],
                        restaurant=restaurant
                    )
                    self.stdout.write(f'\n[Kategoria] {CATEGORIES[matched]}')
                i += 1
                continue

            if skip_mode or current_category is None:
                i += 1
                continue

            if self._should_ignore(line):
                i += 1
                continue

            if pizza_mode:
                skip = self._parse_pizza(all_lines, i, restaurant, current_category)
                if skip:
                    i += skip
                    continue

            skip = self._parse_item(all_lines, i, restaurant, current_category)
            if skip:
                i += skip
                continue

            i += 1

    def _match_category(self, line_upper):
        for key in CATEGORIES:
            if line_upper == key:
                return key
            # obsługuje "CIENKIE CIASTO 23cm 30cm 40cm"
            if line_upper.startswith(key):
                return key
        return None

    def _should_ignore(self, line):
        line_lower = line.lower().strip()
        for pattern in IGNORE_PATTERNS:
            if re.match(pattern, line_lower):
                return True
        if re.match(r'^[\d\s,\.lcm/]+$', line_lower):
            return True
        return False

    def _get_ingredients(self, lines, i):
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            next_upper = next_line.upper()
            is_price_line = bool(re.match(r'^[\d\s,\.]+$', next_line))
            is_category = bool(self._match_category(next_upper))
            is_ignored = self._should_ignore(next_line)
            is_skip = any(next_upper.startswith(s) for s in SKIP_CATEGORIES)
            has_price = bool(re.match(r'^.+?\s+\d{1,3}\s*$', next_line))
            has_3prices = bool(re.match(r'^.+?\s+\d{2}\s+\d{2}\s+\d{2,3}\s*$', next_line))

            if not any([is_price_line, is_category, is_ignored, is_skip, has_price, has_3prices]):
                return next_line, 2
        return '', 1

    def _parse_pizza(self, lines, i, restaurant, category):
        line = lines[i]
        line_clean = re.sub(r'[^\w\s\-/]', '', line).strip()

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

        # jedna cena
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
        line_clean = re.sub(r'[^\w\s\-/,]', '', line).strip()

        # 2 ceny
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
            menu_item=item, name='Rozmiar', type='single', required=True
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
            menu_item=item, name='Rozmiar', type='single', required=True
        )
        Option.objects.create(group=group, name='Mały', extra_price=0)
        Option.objects.create(group=group, name='Duży', extra_price=p2 - p1)
        self.stdout.write(self.style.SUCCESS(f'  Dodano: {name} — {p1}/{p2} zł'))