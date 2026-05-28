from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem, OptionGroup, Option

def create_item(restaurant, category, name, base_price, ingredients, addons=None, sizes=None):
    item = MenuItem.objects.create(
        restaurant=restaurant,
        category=category,
        name=name,
        price=base_price,
        ingredients=ingredients,
    )
    if sizes:
        group = OptionGroup.objects.create(
            menu_item=item,
            name='Rozmiar',
            type='single',
            required=False,
        )
        for size_name, extra in sizes:
            Option.objects.create(
                group=group,
                name=size_name,
                extra_price=extra,
            )
    return item

class Command(BaseCommand):
    help = 'Seed menu Doner King'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='Doner King')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono Doner King w bazie!'))
            return

        Category.objects.filter(restaurant=restaurant).delete()
        self.stdout.write('Usunięto stare dane.')

        # DONER
        cat = Category.objects.create(name='Kebab', restaurant=restaurant)
        self.stdout.write('\n[Kategoria] Kebab')

        # GRAND
        create_item(restaurant, cat,
            'Grand Classic', 39.90,
            'mięso doner, frytki, biała kapusta, czerwona kapusta, mix sałat, pomidor, cebula, rukola, 2x sos; mięso do wyboru: kurczak +0zł, wołowina +5zł (wpisz w notatce)')
        self.stdout.write(self.style.SUCCESS('  Dodano: Grand Classic'))

        create_item(restaurant, cat,
            'Grand Meatlovers', 45.90,
            'mięso doner, frytki, ser żółty, kukurydza, cebula, rukola, 2x sos; mięso do wyboru: kurczak +0zł, wołowina +7zł (wpisz w notatce)')
        self.stdout.write(self.style.SUCCESS('  Dodano: Grand Meatlovers'))

        create_item(restaurant, cat,
            'Grand Fit', 42.90,
            'mięso doner, pomidor, serek turecki, papryka peperoni; mięso do wyboru: kurczak +0zł, wołowina +7zł (wpisz w notatce)')
        self.stdout.write(self.style.SUCCESS('  Dodano: Grand Fit'))

        create_item(restaurant, cat,
            'Donerdilla', 31.90,
            'tortilla, mięso doner, ser żółty, kukurydza, prażona cebulka, sos bbq; mięso do wyboru: kurczak +0zł, wołowina +3zł (wpisz w notatce)')
        self.stdout.write(self.style.SUCCESS('  Dodano: Donerdilla'))

        create_item(restaurant, cat,
            'Doner w bułce', 25.90,
            'biała kapusta, czerwona kapusta, mix sałat, pomidor, cebula, rukola; mięso do wyboru: kurczak, wołowina, mix mięs (wpisz w notatce)',
            sizes=[('S (120g)', 0), ('L (200g)', 8.00), ('XL (300g)', 16.00)])
        self.stdout.write(self.style.SUCCESS('  Dodano: Doner w bułce'))

        create_item(restaurant, cat,
            'Doner tortilla/pita', 24.90,
            'biała kapusta, czerwona kapusta, mix sałat, pomidor, cebula, rukola; mięso do wyboru: kurczak, wołowina, mix mięs (wpisz w notatce)',
            sizes=[('S (120g)', 0), ('L (200g)', 8.00), ('XL (300g)', 15.00)])
        self.stdout.write(self.style.SUCCESS('  Dodano: Doner tortilla/pita'))

        create_item(restaurant, cat,
            'Doner box', 24.90,
            'biała kapusta, czerwona kapusta, mix sałat, pomidor, cebula, rukola; mięso do wyboru: kurczak, wołowina, mix mięs (wpisz w notatce)',
            sizes=[('S (100g)', 0), ('L (150g)', 6.00), ('XL (200g)', 9.00)])
        self.stdout.write(self.style.SUCCESS('  Dodano: Doner box'))

        create_item(restaurant, cat,
            'Fresh box', 24.90,
            'mięso, frytki, biała kapusta, czerwona kapusta, mix sałat, pomidor, cebula, rukola; sos do wyboru (wpisz w notatce)')
        self.stdout.write(self.style.SUCCESS('  Dodano: Fresh box'))

        create_item(restaurant, cat,
            "King's box", 24.90,
            'mięso, frytki, ser żółty; kukurydza lub cebula (wpisz w notatce); sos do wyboru (wpisz w notatce)')
        self.stdout.write(self.style.SUCCESS("  Dodano: King's box"))

        create_item(restaurant, cat,
            'Greco box', 24.90,
            'mięso, frytki, mix sałat, ser grecki, oliwki czarne, pomidor, cebula, rukola; sos do wyboru (wpisz w notatce)')
        self.stdout.write(self.style.SUCCESS('  Dodano: Greco box'))

        create_item(restaurant, cat,
            'Greco w bułce', 27.90,
            'mięso, mix sałat, ser grecki, oliwki, pomidor, cebula, rukola; mięso do wyboru: kurczak, wołowina, mix mięs (wpisz w notatce)',
            sizes=[('S (120g)', 0), ('L (200g)', 8.00), ('XL (300g)', 16.00)])
        self.stdout.write(self.style.SUCCESS('  Dodano: Greco w bułce'))

        create_item(restaurant, cat,
            'Greco tortilla/pita', 26.90,
            'mięso, mix sałat, ser grecki, oliwki, pomidor, cebula, rukola; mięso do wyboru: kurczak, wołowina, mix mięs (wpisz w notatce)',
            sizes=[('S (120g)', 0), ('L (200g)', 8.00), ('XL (300g)', 15.00)])
        self.stdout.write(self.style.SUCCESS('  Dodano: Greco tortilla/pita'))

        create_item(restaurant, cat,
            "King's Wrap", 26.90,
            'mięso, frytki, ser żółty; kukurydza lub cebula (wpisz w notatce); sos do wyboru (wpisz w notatce)',
            sizes=[('S (100g)', 0), ('L (200g)', 7.00), ('XL (200g)', 12.00)])
        self.stdout.write(self.style.SUCCESS("  Dodano: King's Wrap"))

        create_item(restaurant, cat,
            'Góral tortilla/pita', 26.90,
            'mięso, mix sałat, cebula, pomidor, ser góralski; mięso do wyboru: kurczak, wołowina, mix mięs (wpisz w notatce)',
            sizes=[('S (120g)', 0), ('L (200g)', 8.00), ('XL (300g)', 16.00)])
        self.stdout.write(self.style.SUCCESS('  Dodano: Góral tortilla/pita'))

        create_item(restaurant, cat,
            'Drwal tortilla/pita', 30.90,
            'mięso, prażona cebulka, pieczony ser gouda, mix sałat, pomidor; mięso do wyboru: kurczak, wołowina, mix mięs (wpisz w notatce)',
            sizes=[('S (100g)', 0), ('L (150g)', 6.00), ('XL (200g)', 12.00)])
        self.stdout.write(self.style.SUCCESS('  Dodano: Drwal tortilla/pita'))

        create_item(restaurant, cat,
            'Jalapenos tortilla', 26.90,
            'mięso, mix sałat, nachos, jalapeno, ser, cebula; mięso do wyboru: kurczak, wołowina, mix mięs (wpisz w notatce)',
            sizes=[('S (120g)', 0), ('L (200g)', 8.00), ('XL (300g)', 16.00)])
        self.stdout.write(self.style.SUCCESS('  Dodano: Jalapenos tortilla'))

        create_item(restaurant, cat,
            'Mini tortilla', 27.90,
            'mięso 70g, soczyste, krówki')
        self.stdout.write(self.style.SUCCESS('  Dodano: Mini tortilla'))

        create_item(restaurant, cat,
            "Mini King's box", 27.90,
            'mięso 50g, soczyste, krówki')
        self.stdout.write(self.style.SUCCESS("  Dodano: Mini King's box"))

        create_item(restaurant, cat,
            'Mini Nuggets box', 25.90,
            'frytki, nuggets 4szt, soczyste, krówki; sos do wyboru: ketchup lub sos (wpisz w notatce)')
        self.stdout.write(self.style.SUCCESS('  Dodano: Mini Nuggets box'))

        create_item(restaurant, cat,
            'Falafel Classic', 23.90,
            'tortilla, falafel, kapusta biała, kapusta czerwona, mix sałat, pomidor, cebula, rukola; sos do wyboru (wpisz w notatce)',
            sizes=[('S', 0), ('L', 3.00)])
        self.stdout.write(self.style.SUCCESS('  Dodano: Falafel Classic'))

        create_item(restaurant, cat,
            'Falafel Box', 23.90,
            'frytki, falafel, kapusta biała, kapusta czerwona, mix sałat, pomidor, cebula; sos do wyboru (wpisz w notatce)',
            sizes=[('S', 0), ('L', 4.00)])
        self.stdout.write(self.style.SUCCESS('  Dodano: Falafel Box'))

        create_item(restaurant, cat,
            'Falafel Greco', 25.90,
            'tortilla, falafel, mix sałat, pomidor, rukola, cebula, oliwki czarne, ser grecki; sos do wyboru (wpisz w notatce)',
            sizes=[('S', 0), ('L', 2.00)])
        self.stdout.write(self.style.SUCCESS('  Dodano: Falafel Greco'))

        create_item(restaurant, cat,
            'Falafel Greco Box', 25.90,
            'frytki, falafel, mix sałat, pomidor, rukola, cebula, oliwki czarne, ser grecki; sos do wyboru (wpisz w notatce)',
            sizes=[('S', 0), ('L', 4.00)])
        self.stdout.write(self.style.SUCCESS('  Dodano: Falafel Greco Box'))

        # SAŁATKI
        cat = Category.objects.create(name='Sałatki', restaurant=restaurant)
        self.stdout.write('\n[Kategoria] Sałatki')

        create_item(restaurant, cat,
            'Sałatka Doner', 29.90,
            'mix sałat, mięso 150g, pomidor, cebula, kukurydza, paluszki chlebowe; mięso do wyboru: kurczak +0zł, wołowina +4zł (wpisz w notatce); sos do wyboru (wpisz w notatce)')
        self.stdout.write(self.style.SUCCESS('  Dodano: Sałatka Doner'))

        create_item(restaurant, cat,
            'Sałatka Greco', 29.90,
            'mix sałat, mięso 150g, pomidor, rukola, cebula, oliwki czarne, ser grecki, paluszki chlebowe; mięso do wyboru: kurczak +0zł, wołowina +4zł (wpisz w notatce); sos do wyboru (wpisz w notatce)')
        self.stdout.write(self.style.SUCCESS('  Dodano: Sałatka Greco'))

        create_item(restaurant, cat,
            'Sałatka Góralska', 33.90,
            'mix sałat, mięso 150g, ser góralski, pomidor, paluszki chlebowe; mięso do wyboru: kurczak +0zł, wołowina +4zł (wpisz w notatce); sos do wyboru (wpisz w notatce)')
        self.stdout.write(self.style.SUCCESS('  Dodano: Sałatka Góralska'))

        # NUGGETS & PRZEKĄSKI
        cat = Category.objects.create(name='Nuggets', restaurant=restaurant)
        self.stdout.write('\n[Kategoria] Nuggets')

        create_item(restaurant, cat,
            'Nuggets', 15.90,
            'ketchup lub sos (wpisz w notatce)',
            sizes=[('4 szt.', 0), ('8 szt.', 6.00)])
        self.stdout.write(self.style.SUCCESS('  Dodano: Nuggets'))

        create_item(restaurant, cat,
            'Nuggets zestaw', 19.90,
            'frytki; sos do wyboru: ketchup lub sos (wpisz w notatce)',
            sizes=[('4 szt.', 0), ('8 szt.', 6.00)])
        self.stdout.write(self.style.SUCCESS('  Dodano: Nuggets zestaw'))

        create_item(restaurant, cat,
            'Serki Gouda', 13.90,
            'w chrupiącej panierce',
            sizes=[('4 szt.', 0), ('8 szt.', 3.00)])
        self.stdout.write(self.style.SUCCESS('  Dodano: Serki Gouda'))

        # FRYTKI
        cat = Category.objects.create(name='Frytki', restaurant=restaurant)
        self.stdout.write('\n[Kategoria] Frytki')

        create_item(restaurant, cat,
            'Frytki', 13.90, '',
            sizes=[('S (120g)', 0), ('L (190g)', 2.00)])
        self.stdout.write(self.style.SUCCESS('  Dodano: Frytki'))

        create_item(restaurant, cat,
            'Frytki belgijskie', 15.90, '',
            sizes=[('S (150g)', 0), ('L (180g)', 2.00)])
        self.stdout.write(self.style.SUCCESS('  Dodano: Frytki belgijskie'))

        self.stdout.write(self.style.SUCCESS('\nGotowe!'))