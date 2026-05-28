from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem, OptionGroup, Option

MENU = {
    'Dania główne': [
        ('Kebab w bułce', 24.00, 'mięso, surówka, sos', [('Duży', 0), ('Mały', -4.00)], ['mięso do wyboru: kurczak lub wołowina (wpisać w notatce)', 'sos do wyboru: łagodny, średni, ostry, bardzo ostry (wpisać w notatce)']),
        ('Kebab w bułce + frytki', 26.00, 'mięso, surówka, sos, frytki w środku', [('Duży', 0)], ['mięso do wyboru: kurczak lub wołowina (wpisać w notatce)', 'sos do wyboru: łagodny, średni, ostry, bardzo ostry (wpisać w notatce)']),
        ('Kebab w cieście', 24.00, 'mięso, surówka, sos', [('Duży', 0), ('Mały', -4.00)], ['mięso do wyboru: kurczak lub wołowina (wpisać w notatce)', 'sos do wyboru: łagodny, średni, ostry, bardzo ostry (wpisać w notatce)']),
        ('Kebab w cieście + frytki', 26.00, 'mięso, surówka, sos, frytki w środku', [('Duży', 0)], ['mięso do wyboru: kurczak lub wołowina (wpisać w notatce)', 'sos do wyboru: łagodny, średni, ostry, bardzo ostry (wpisać w notatce)']),
        ('Kebab zestaw', 28.00, 'mięso, frytki, surówka', [('Duży', 0), ('Mały', -8.00)], ['mięso do wyboru: kurczak lub wołowina (wpisać w notatce)', 'sos do wyboru: łagodny, średni, ostry, bardzo ostry (wpisać w notatce)']),
        ('Kebab servets', 25.00, 'mięso, frytki, sos', [('Duży', 0), ('Mały', -5.00)], ['mięso do wyboru: kurczak lub wołowina (wpisać w notatce)', 'sos do wyboru: łagodny, średni, ostry, bardzo ostry (wpisać w notatce)']),
        ('Tortilla Vege', 20.00, 'warzywa, surówka, sos', [], ['sos do wyboru: łagodny, średni, ostry, bardzo ostry (wpisać w notatce)']),
        ('Sałatka z mięsem', 21.00, 'mięso, surówka, sos', [], ['mięso do wyboru: kurczak lub wołowina (wpisać w notatce)', 'sos do wyboru: łagodny, średni, ostry, bardzo ostry (wpisać w notatce)']),
        ('Zapiekanka', 12.00, '', [], []),
        ('Frytki', 9.00, '', [('Małe', 0), ('Duże', 1.00)], []),
    ],
    'Dodatki do dań': [
        ('Podwójne mięso', 8.00, '', [], []),
        ('Cebulka prażona', 1.00, '', [], []),
        ('Dodatkowy sos', 2.00, '', [], ['sos do wyboru: łagodny czosnek, łagodny koperek, średnio ostry, ostry, bardzo ostry, mix sosów (wpisać w notatce)']),
        ('Opakowanie na wynos', 1.00, '', [], []),
    ],
    'Napoje': [
        ('Napój puszka 0,33l', 6.00, '', [], ['wybór smaku: Pepsi, 7up, Mirinda, Lipton (wpisać w notatce)']),
        ('Napój butelka 0,5l', 8.00, '', [], ['wybór smaku: Pepsi, 7up, Mirinda, Lipton (wpisać w notatce)']),
        ('Woda', 4.00, '', [], []),
    ],
}


class Command(BaseCommand):
    help = 'Seed menu Kebab u Pajdy'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='Kebab u Pajdy')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono Kebab u Pajdy w bazie!'))
            return

        Category.objects.filter(restaurant=restaurant).delete()
        self.stdout.write('Usunięto stare dane.')

        for category_name, items in MENU.items():
            category, _ = Category.objects.get_or_create(
                name=category_name,
                restaurant=restaurant
            )
            self.stdout.write(f'\n[Kategoria] {category_name}')

            for name, price, ingredients, sizes, addons in items:
                menu_item = MenuItem.objects.create(
                    restaurant=restaurant,
                    category=category,
                    name=name,
                    price=price,
                    ingredients=ingredients,
                )
                self.stdout.write(self.style.SUCCESS(f'  Dodano: {name} — {price} zł'))

                if sizes:
                    group = OptionGroup.objects.create(
                        menu_item=menu_item,
                        name='Rozmiar',
                        type='single',
                        required=False,
                    )
                    for label, extra_price in sizes:
                        Option.objects.create(
                            group=group,
                            name=label,
                            extra_price=extra_price,
                            capacity=label,
                        )
                        self.stdout.write(f'    Rozmiar: {label} ({extra_price:+.2f} zł)')

                if addons:
                    group = OptionGroup.objects.create(
                        menu_item=menu_item,
                        name='Personalizacja',
                        type='single',
                        required=False,
                    )
                    for addon in addons:
                        Option.objects.create(
                            group=group,
                            name=addon,
                            extra_price=0,
                        )
                        self.stdout.write(f'    Personalizacja: {addon}')

        self.stdout.write(self.style.SUCCESS('\nGotowe!'))