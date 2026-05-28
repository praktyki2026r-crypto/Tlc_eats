from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem, OptionGroup, Option

MENU = {
    'Dania główne': [
        ('Schabowy zestaw', 17.50, '2 kotlety, 3 gałki ziemniaków lub frytki, zestaw surówek', []),
        ('Drobiowy zestaw', 16.50, '2 kotlety, 3 gałki ziemniaków lub frytki, zestaw surówek', []),
        ('Ser prażony zestaw', 14.50, '2 kawałki sera, ziemniaki lub frytki', []),
        ('Wątróbka zestaw', 13.50, 'wątróbka z cebulką, ziemniaki lub frytki, zestaw surówek', []),
        ('Placek po węgiersku', 16.50, 'Placek po węgiersku, zestaw surówek', []),
        ('Placki ziemniaczane', 6.50, 'Placki ziemniaczane, śmietana', []),
        ('Fasolka po bretońsku', 9.00, '', [('500ml', 0)]),
        ('Flaki wołowe', 9.00, '', [('500ml', 0)]),
        ('Ryba dorsz', 17.50, '2 kawałki ryby, ziemniaki lub frytki, zestaw surówek', []),
        ('Ryba miruna', 16.00, '2 kawałki ryby, ziemniaki lub frytki, zestaw surówek', []),
        ('Naleśniki z serem', 5.50, '', []),
        ('Naleśniki z dżemem truskawkowym', 5.50, 'Naleśniki, dżem truskawkowym', []),
        ('Naleśniki z czekoladą', 5.50, 'Naleśniki, czekolada', []),
        ('Naleśniki z serem i musem', 6.50, 'Naleśniki z serem i musem', []),
        ('Pierogi ruskie', 9.50, '', [('12szt', 0)]),
        ('Pierogi z kapustą', 9.50, '', [('12szt', 0)]),
        ('Pierogi z mięsem', 10.00, '', [('12szt', 0)]),
        ('Pierogi z truskawkami', 9.50, 'śmietana', [('12szt', 0)]),
        ('Pierogi z jagodami', 9.50, 'śmietana', [('12szt', 0)]),
        ('Pierogi z jabłkiem', 8.50, '', [('12szt', 0)]),
        ('Pierogi ze słodkim serem', 9.50, 'mus truskawkowy', [('12szt', 0)]),
    ],
    'Zupy': [
        ('Barszcz czerwony z uszkami', 7.50, 'barszcz, 12 uszek', [('500ml', 0)]),
        ('Żurek z jajkiem i kiełbasą', 6.50, 'jajko, kiełbasa', [('500ml', 0)]),
        ('Barszcz czerwony solo', 6.00, '', [('500ml', 0), ('300ml', -2.00)]),
        ('Żurek solo', 4.50, '', [('200ml', 0)]),
    ],
    
}

class Command(BaseCommand):
    help = 'Seed menu Bar Mleczny Wojtek Gorlice'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='Bar Wojtek')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono Bar Mleczny Wojtek Gorlice w bazie!'))
            return

        Category.objects.filter(restaurant=restaurant).delete()
        self.stdout.write('Usunięto stare dane.')

        for category_name, items in MENU.items():
            category, _ = Category.objects.get_or_create(
                name=category_name,
                restaurant=restaurant
            )
            self.stdout.write(f'\n[Kategoria] {category_name}')

            for name, price, ingredients, sizes in items:
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

        self.stdout.write(self.style.SUCCESS('\nGotowe!'))