from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem, OptionGroup, Option

MENU = {
    'Doner klasyczny': [
        # (nazwa, cena_bazowa, składniki, opcje: [(nazwa, extra_price)])
        ('Doner w bułce S', 25.90, 'mięso 120g, biała kapusta, czerwona kapusta, mix sałat, pomidor, cebula, rukola, sos', []),
        ('Doner w bułce L', 33.90, 'mięso 200g, biała kapusta, czerwona kapusta, mix sałat, pomidor, cebula, rukola, sos', []),
        ('Doner w bułce XL', 41.90, 'mięso 300g, biała kapusta, czerwona kapusta, mix sałat, pomidor, cebula, rukola, sos', []),
        ('Doner tortilla/pita S', 24.90, 'mięso 120g, biała kapusta, czerwona kapusta, mix sałat, pomidor, cebula, rukola, sos', []),
        ('Doner tortilla/pita L', 32.90, 'mięso 200g, biała kapusta, czerwona kapusta, mix sałat, pomidor, cebula, rukola, sos', []),
        ('Doner tortilla/pita XL', 39.90, 'mięso 300g, biała kapusta, czerwona kapusta, mix sałat, pomidor, cebula, rukola, sos', []),
        ('Doner box S', 24.90, 'mięso 100g, biała kapusta, czerwona kapusta, mix sałat, pomidor, cebula, rukola, sos', []),
        ('Doner box L', 30.90, 'mięso 150g, biała kapusta, czerwona kapusta, mix sałat, pomidor, cebula, rukola, sos', []),
        ('Doner box XL', 33.90, 'mięso 200g, biała kapusta, czerwona kapusta, mix sałat, pomidor, cebula, rukola, sos', []),
    ],
    'Fresh & King': [
        ('Fresh box', 0, 'mięso, frytki, biała kapusta, czerwona kapusta, mix sałat, pomidor, cebula, rukola, sos', []),
        ('King\'s box', 0, 'mięso, frytki, ser żółty, kukurydza lub cebula, sos', []),
        ('Greco box', 0, 'mięso, frytki, mix sałat, ser grecki, oliwki czarne, pomidor, cebula, rukola, sos', []),
    ],
    'Greco & Specialty': [
        ('Greco w bułce S', 27.90, 'mięso, mix sałat, ser grecki, oliwki, pomidor, cebula, rukola, sos', []),
        ('Greco w bułce L', 35.90, 'mięso, mix sałat, ser grecki, oliwki, pomidor, cebula, rukola, sos', []),
        ('Greco w bułce XL', 43.90, 'mięso, mix sałat, ser grecki, oliwki, pomidor, cebula, rukola, sos', []),
        ('Greco tortilla/pita S', 26.90, 'mięso, mix sałat, ser grecki, oliwki, pomidor, cebula, rukola, sos', []),
        ('Greco tortilla/pita L', 34.90, 'mięso, mix sałat, ser grecki, oliwki, pomidor, cebula, rukola, sos', []),
        ('Greco tortilla/pita XL', 41.90, 'mięso, mix sałat, ser grecki, oliwki, pomidor, cebula, rukola, sos', []),
        ('King\'s Wrap S', 26.90, 'mięso, frytki, ser żółty, kukurydza lub cebula, sos', []),
        ('King\'s Wrap L', 33.90, 'mięso, frytki, ser żółty, kukurydza lub cebula, sos', []),
        ('King\'s Wrap XL', 38.90, 'mięso, frytki, ser żółty, kukurydza lub cebula, sos', []),
        ('Góral tortilla/pita S', 26.90, 'mięso, mix sałat, cebula, pomidor, ser góralski, sos', []),
        ('Góral tortilla/pita L', 34.90, 'mięso, mix sałat, cebula, pomidor, ser góralski, sos', []),
        ('Góral tortilla/pita XL', 42.90, 'mięso, mix sałat, cebula, pomidor, ser góralski, sos', []),
        ('Drwal tortilla/pita S', 30.90, 'mięso, prażona cebulka, pieczony ser gouda, mix sałat, pomidor, sos', []),
        ('Drwal tortilla/pita L', 36.90, 'mięso, prażona cebulka, pieczony ser gouda, mix sałat, pomidor, sos', []),
        ('Drwal tortilla/pita XL', 42.90, 'mięso, prażona cebulka, pieczony ser gouda, mix sałat, pomidor, sos', []),
        ('Jalapenos tortilla S', 26.90, 'mięso, mix sałat, nachos, jalapeno, ser, cebula, sos', []),
        ('Jalapenos tortilla L', 34.90, 'mięso, mix sałat, nachos, jalapeno, ser, cebula, sos', []),
        ('Jalapenos tortilla XL', 42.90, 'mięso, mix sałat, nachos, jalapeno, ser, cebula, sos', []),
    ],
    'Mini Doner': [
        ('Mini tortilla', 27.90, 'mięso 70g, soczyste, krówki'),
        ('Mini King\'s box', 27.90, 'mięso 50g, soczyste, krówki'),
        ('Mini Nuggets box', 25.90, 'frytki, nuggets 4szt, ketchup lub sos, soczyste, krówki'),
    ],
    'Falafel': [
        ('Falafel Classic S', 23.90, 'tortilla, falafel, kapusta biała, kapusta czerwona, mix sałat, pomidor, cebula, rukola, sos'),
        ('Falafel Classic L', 26.90, 'tortilla, falafel, kapusta biała, kapusta czerwona, mix sałat, pomidor, cebula, rukola, sos'),
        ('Falafel Box S', 23.90, 'frytki, falafel, kapusta biała, kapusta czerwona, mix sałat, pomidor, cebula, sos'),
        ('Falafel Box L', 27.90, 'frytki, falafel, kapusta biała, kapusta czerwona, mix sałat, pomidor, cebula, sos'),
        ('Falafel Greco S', 25.90, 'tortilla, falafel, mix sałat, pomidor, rukola, cebula, oliwki czarne, ser grecki, sos'),
        ('Falafel Greco L', 27.90, 'tortilla, falafel, mix sałat, pomidor, rukola, cebula, oliwki czarne, ser grecki, sos'),
        ('Falafel Greco Box S', 25.90, 'frytki, falafel, mix sałat, pomidor, rukola, cebula, oliwki czarne, ser grecki, sos'),
        ('Falafel Greco Box L', 29.90, 'frytki, falafel, mix sałat, pomidor, rukola, cebula, oliwki czarne, ser grecki, sos'),
    ],
    'Sałatki': [
        ('Sałatka Doner', 29.90, 'mix sałat, mięso 150g, pomidor, cebula, kukurydza, sos, paluszki chlebowe'),
        ('Sałatka Greco', 29.90, 'mix sałat, mięso 150g, pomidor, rukola, cebula, oliwki czarne, ser grecki, sos, paluszki chlebowe'),
        ('Sałatka Góralska', 33.90, 'mix sałat, mięso 150g, ser góralski, pomidor, sos, paluszki chlebowe'),
    ],
    'Nuggets & Przekąski': [
        ('Nuggets 4szt.', 15.90, 'ketchup lub sos'),
        ('Nuggets 8szt.', 21.90, 'ketchup lub sos'),
        ('Nuggets zestaw 4szt.', 19.90, 'frytki, ketchup lub sos'),
        ('Nuggets zestaw 8szt.', 25.90, 'frytki, ketchup lub sos'),
        ('Serki Gouda 4szt.', 13.90, 'w chrupiącej panierce'),
        ('Serki Gouda 8szt.', 16.90, 'w chrupiącej panierce'),
    ],
    'Frytki': [
        ('Frytki S', 13.90, '120g'),
        ('Frytki L', 15.90, '190g'),
        ('Frytki belgijskie S', 15.90, '150g'),
        ('Frytki belgijskie L', 17.90, '180g'),
    ],
    'Grand': [
        ('Grand Classic', 39.90, 'mięso doner, frytki, biała kapusta, czerwona kapusta, mix sałat, pomidor, cebula, rukola, 2x sos'),
        ('Grand Meatlovers', 45.90, 'mięso doner, frytki, ser żółty, kukurydza, cebula, rukola, 2x sos'),
        ('Grand Fit', 42.90, 'mięso doner, pomidor, serek turecki, papryka peperoni'),
        ('Donerdilla', 31.90, 'tortilla, mięso doner, ser żółty, kukurydza, prażona cebulka, sos bbq, sos'),
    ],
}

class Command(BaseCommand):
    help = 'Seed menu Doner King'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='Doner King')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono Doner king w bazie!'))
            return

        Category.objects.filter(restaurant=restaurant).delete()
        self.stdout.write('Usunięto stare dane.')

        for category_name, items in MENU.items():
            category, _ = Category.objects.get_or_create(
                name=category_name,
                restaurant=restaurant
            )
            self.stdout.write(f'\n[Kategoria] {category_name}')

            for item in items:
                name, price, ingredients = item[0], item[1], item[2]
                MenuItem.objects.create(
                    restaurant=restaurant,
                    category=category,
                    name=name,
                    price=price,
                    ingredients=ingredients,
                )
                self.stdout.write(self.style.SUCCESS(f'  Dodano: {name} — {price} zł'))

        self.stdout.write(self.style.SUCCESS('\nGotowe!'))

       