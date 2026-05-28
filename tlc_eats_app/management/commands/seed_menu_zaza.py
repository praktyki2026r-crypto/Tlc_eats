from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem

MENU = {
    'Kebab': [
        ('Pita', 20, 'mięso, sałata, sos do wyboru',[('mała', 0), ('mega', 10)], []),
        ('Pita amerykańska', 34, 'mięso, frytki, ser, sałata, sos do wyboru'),
        ('Kebab w bułce', 25, 'mięso, sałata, sos do wyboru',[('klasyczna', 0), ('mega', 2)], []),
        ('Kebab w bułce z frytkami', 30, 'mięso, frytki, sałata, sos do wyboru'),
        ('Kebab tortilla', 24, 'mięso, sałata, sos do wyboru(wpisz w notatce)', [('klasyczna', 0), ('średnia', 3), ('mega', 5)], []),
        ('Kebab tortilla amerykańska', 36, 'mięso, frytki, ser, sałata, sos do wyboru'),
        ('Döner box', 24, 'mięso, frytki lub surówka, sos do wyboru', [('500ml', 0), ('750ml', 3),('500g(samo mięso)', 14)], []),
        ('Döner kebab na talerzu', 34, 'mięso, frytki lub surówka, sos do wyboru', [('klasyczny', 0), ('mega', 3)], []),
        ('Kapsalon zapiekany', 25, 'frytki, mięso, zapiekany ser, surówka, sos do wyboru', [('mały', 0), ('duży', 5)], []),
        ('Zapiekanka klasyczna', 17, 'pieczarki, ser, sos do wyboru'),
        ('Zapiekanka z mięsem', 20, 'mięso, pieczarki, ser, sos do wyboru'),
        ('Hamburger', 14, ''),
        ('Cheeseburger', 16, ''),
        ('Falafel w bułce', 19, 'cieciorka, sałata, sos do wyboru', [('4szt.', 0)], []),
        ('Falafel tortilla', 22, 'cieciorka, sałata, sos do wyboru',[('4szt.', 0)],[]),
        ('Falafel box', 21, 'cieciorka, frytki lub sałata, sos do wyboru',[('4szt.', 0)],[]),
        ('Falafel zestaw', 26, 'cieciorka, frytki, sałata, sos do wyboru',[('5szt.', 0)],[]),
    ],
    'Nuggetsy': [
        ('Nuggets w bułce', 19, 'nuggets 5szt, sałata, sos do wyboru'),
        ('Nuggets tortilla', 22, 'nuggets 5szt, sałata, sos do wyboru'),
        ('Nuggets box 750ml', 24, 'nuggets 5szt, frytki, sałata, sos do wyboru'),
        ('Nuggets zestaw', 30, 'nuggets 5szt, frytki, sałata, sos do wyboru'),
    ],
    'Sałatki': [
        ('Sałatka grecka', 22, ''),
        ('Sałatka z kurczakiem', 25, ''),
    ],
    'Frytki': [
        ('Frytki małe', 12, '',[('małe', 0), ('duże', 3)], []),
        ('Frytki duże', 15, ''),
    ],
    'Dodatki': [
        ('Dodatkowy sos', 3, ''),
        ('Dodatkowe mięso', 7, ''),
    ],
    'Napoje': [
        ('Cola, Fanta, Sprite 0,5l', 9, ''),
        ('Woda 0,5l', 5, ''),
        ('Sok 0,33l', 5, ''),
        ('Cola, Fanta, Sprite w puszce 0,33l', 7, ''),
    ],
}

class Command(BaseCommand):
    help = 'Seed menu Zaza Doner Kebab'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='Zaza')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono Zaza doner kebab w bazie!'))
            return

        Category.objects.filter(restaurant=restaurant).delete()
        self.stdout.write('Usunięto stare dane.')

        for category_name, items in MENU.items():
            category, _ = Category.objects.get_or_create(
                name=category_name,
                restaurant=restaurant
            )
            self.stdout.write(f'\n[Kategoria] {category_name}')

            for name, price, ingredients in items:
                MenuItem.objects.create(
                    restaurant=restaurant,
                    category=category,
                    name=name,
                    price=price,
                    ingredients=ingredients,
                )
                self.stdout.write(self.style.SUCCESS(f'  Dodano: {name} — {price} zł'))

        self.stdout.write(self.style.SUCCESS('\nGotowe!'))