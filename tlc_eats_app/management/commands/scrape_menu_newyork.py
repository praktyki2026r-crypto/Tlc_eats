from django.core.management.base import BaseCommand
import pytesseract
from PIL import Image
import os
import re
from tlc_eats_app.models import Restaurant, Category, MenuItem

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class Command(BaseCommand):
    help = 'Scrape menu New York z lokalnych zdjęć'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='New York')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono New York w bazie!'))
            return

        Category.objects.filter(restaurant=restaurant).delete()
        self.stdout.write('Usunięto stare dane.')

        folder = r'C:\Users\DS8JS73\Aplikacja_Tlc_Eats\tlc_eats\menu_restauracji_zdj\new_york_bar'

        text = ''
        for filename in sorted(os.listdir(folder)):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                path = os.path.join(folder, filename)
                self.stdout.write(f'Przetwarzam: {filename}')
                image = Image.open(path)
                text += pytesseract.image_to_string(image, lang='pol') + '\n'

        self._parse_menu(text, restaurant)
        self.stdout.write(self.style.SUCCESS('Gotowe!'))

    def _parse_menu(self, text, restaurant):
        current_category = None
        excluded_categories = [
            'piwo', 'alkohol', 'trunki', 'wino', 'napoje alkoholowe'
        ]
        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # kategoria — linia z samymi wielkimi literami bez ceny
            if line.isupper() and not re.search(r'\d+[.,]\d+', line) and len(line) > 3:
                if any(excl in line.lower() for excl in excluded_categories):
                    current_category = None  # pomiń kategorię i jej pozycje
                    continue
                current_category, _ = Category.objects.get_or_create(
                    name=line.title(),
                    restaurant=restaurant
                )
                self.stdout.write(f'\n[Kategoria] {line.title()}')
                continue

            if not current_category:
                continue

            # danie — linia z ceną np "Zestaw 12,00 zł" lub "I ZESTAW 12.00zł"
            price_match = re.search(r'(\d+[.,]\d+)\s*z[łl]?', line)
            if price_match:
                price = float(price_match.group(1).replace(',', '.'))
                # nazwa — wszystko przed ceną
                name = re.sub(r'\s*\d+[.,]\d+\s*z[łl]?.*$', '', line).strip()
                # usuń numery porządkowe na początku np "I ", "II ", "1."
                name = re.sub(r'^[IVXivx]+\s+|^\d+\.\s*', '', name).strip()

                if not name or len(name) < 2:
                    continue

                # składniki — kolejna linia po daniu
                ingredients = ''

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