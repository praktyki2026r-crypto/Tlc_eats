from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem

MENU = {
    'Kebab': [
        ('Pita mała', 20, 'mięso, sałata, sos do wyboru'),
        ('Pita średnia', 24, 'mięso, sałata, sos do wyboru'),
        ('Pita mega', 30, 'mięso, sałata, sos do wyboru'),
        ('Pita amerykańska', 34, 'mięso, frytki, ser, sałata, sos do wyboru'),
        ('Kebab w bułce klasyczny', 25, 'mięso, sałata, sos do wyboru'),
        ('Kebab w bułce mega', 27, 'podwójne mięso, sałata, sos do wyboru'),
        ('Kebab w bułce z frytkami', 30, 'mięso, frytki, sałata, sos do wyboru'),
        ('Kebab tortilla klasyczna', 24, 'mięso, sałata, sos do wyboru'),
        ('Kebab tortilla średnia', 27, 'mięso, sałata, sos do wyboru'),
        ('Kebab tortilla mega', 32, 'podwójne mięso, sałata, sos do wyboru'),
        ('Kebab tortilla amerykańska', 36, 'mięso, frytki, ser, sałata, sos do wyboru'),
        ('Döner box klasyczny 500ml', 24, 'mięso, frytki lub surówka, sos do wyboru'),
        ('Döner box mega 750ml', 27, 'podwójne mięso, frytki, sałata, sos do wyboru'),
        ('Döner box - samo mięso', 38, '500g, sos do wyboru'),
        ('Döner kebab na talerzu klasyczny', 34, 'mięso, frytki lub surówka, sos do wyboru'),
        ('Döner kebab na talerzu mega', 37, 'podwójne mięso, frytki, surówka, sos do wyboru'),
        ('Kapsalon zapiekany mały', 25, 'frytki, mięso, zapiekany ser, surówka, sos do wyboru'),
        ('Kapsalon zapiekany duży', 30, 'frytki, mięso, zapiekany ser, surówka, sos do wyboru'),
        ('Zapiekanka klasyczna', 17, 'pieczarki, ser, sos do wyboru'),
        ('Zapiekanka z mięsem', 20, 'mięso, pieczarki, ser, sos do wyboru'),
        ('Hamburger klasyczny', 14, ''),
        ('Cheeseburger', 16, ''),
    ],
    'Nuggetsy': [
        ('Nuggets w bułce', 19, 'nuggets 5szt, sałata, sos do wyboru'),
        ('Nuggets tortilla', 22, 'nuggets 5szt, sałata, sos do wyboru'),
        ('Nuggets box 750ml', 24, 'nuggets 5szt, frytki, sałata, sos do wyboru'),
        ('Nuggets zestaw', 30, 'nuggets 5szt, frytki, sałata, sos do wyboru'),
    ],
    'Dania wegetariańskie': [
        ('Falafel w bułce - 4 szt.', 19, 'cieciorka, sałata, sos do wyboru'),
        ('Falafel tortilla - 4 szt.', 22, 'cieciorka, sałata, sos do wyboru'),
        ('Falafel box - 4 szt.', 21, 'cieciorka, frytki lub sałata, sos do wyboru'),
        ('Falafel zestaw - 5 szt.', 26, 'cieciorka, frytki, sałata, sos do wyboru'),
    ],
    'Sałatki': [
        ('Sałatka grecka', 22, ''),
        ('Sałatka z kurczakiem', 25, ''),
    ],
    'Frytki': [
        ('Frytki małe', 12, ''),
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