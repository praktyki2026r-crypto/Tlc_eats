from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem, OptionGroup, Option

MENU = {
    'Pizza': [
        ('Margherita', 23.00, 'sos, ser, oregano', [('20cm', 0), ('30cm', 11.00), ('40cm', 17.00)], []),
        ('Capricciosa', 25.00, 'sos, ser, pieczarki, szynka, oregano', [('20cm', 0), ('30cm', 12.50), ('40cm', 20.00)], []),
        ('Podhale', 31.00, 'sos, ser, ogórek, oscypki, boczek, rukola, oregano', [('20cm', 0), ('30cm', 13.00), ('40cm', 22.00)], []),
        ('Vegetariana', 26.00, 'sos, ser, pieczarki, cebulka, pomidor, rukola, papryka, oregano', [('20cm', 0), ('30cm', 12.50), ('40cm', 20.00)], []),
        ('Don Wicio', 32.00, 'sos, ser, oregano', [('20cm', 0), ('30cm', 13.00), ('40cm', 22.00)], ['4 wybrane składniki (wpisać w notatce)']),
        ('Mexico', 29.00, 'sos, ser, czerwona fasola, kukurydza, ostra papryka, oregano', [('20cm', 0), ('30cm', 10.50), ('40cm', 19.00)], []),
        ('Curry', 26.00, 'sos, ser, curry, kurczak, ananas, oregano', [('20cm', 0), ('30cm', 12.50), ('40cm', 20.00)], []),
        ('Zbója', 29.00, 'sos, ser, oscypki, zielony pieprz, papryka, boczek, oregano', [('20cm', 0), ('30cm', 14.00), ('40cm', 22.00)], []),
        ('Rimini', 31.00, 'sos, ser, pieczarki, papryka, szynka, kukurydza, oregano', [('20cm', 0), ('30cm', 14.00), ('40cm', 22.00)], []),
        ('Kurczak Country', 27.50, 'sos, ser, pieczarki, kurczak, cebulka, papryka, kukurydza, oregano', [('20cm', 0), ('30cm', 13.50), ('40cm', 22.00)], []),
        ('Rusticana', 25.00, 'sos, ser, boczek, cebulka, oregano', [('20cm', 0), ('30cm', 10.00), ('40cm', 17.00)], []),
        ('Boloński Osioł', 27.00, 'sos, ser, cebulka, salami, oregano', [('20cm', 0), ('30cm', 11.50), ('40cm', 20.00)], []),
        ('Z Piekła Rodem', 28.00, 'sos, ser, cebulka, papryka, pomidor, ostra papryka, oregano', [('20cm', 0), ('30cm', 12.50), ('40cm', 20.00)], []),
        ('Neapolitana', 28.00, 'sos, ser, szynka, oliwki, pieczarki, pomidor, oregano', [('20cm', 0), ('30cm', 12.50), ('40cm', 20.00)], []),
        ('Color', 26.00, 'sos, ser, rukola, ogórek, papryka, szynka, oliwki, zielony pieprz, oregano', [('20cm', 0), ('30cm', 11.00), ('40cm', 17.00)], []),
        ('Familia', 29.00, 'sos, ser, pieczarki, kurczak, papryka, kukurydza, cebulka, oregano', [('20cm', 0), ('30cm', 14.00), ('40cm', 22.00)], []),
        ('Hawaii', 27.00, 'sos, ser, szynka, ananas, oregano', [('20cm', 0), ('30cm', 9.00), ('40cm', 16.00)], []),
        ('Bolonia', 29.00, 'sos, ser, salami, oliwki, pomidor, oregano', [('20cm', 0), ('30cm', 14.00), ('40cm', 22.00)], []),
        ('Country', 28.00, 'sos, ser, pieczarki, boczek, szynka, papryka, ogórek, oregano', [('20cm', 0), ('30cm', 11.00), ('40cm', 20.00)], []),
        ('Diavola', 26.00, 'sos, ser, ostra papryka, szynka, cebulka, oregano', [('20cm', 0), ('30cm', 12.50), ('40cm', 20.00)], []),
        ('Fromaggi', 31.00, 'sos, ser cheddar, ser, mozzarella, ser gouda, oscypki, oregano', [('20cm', 0), ('30cm', 13.50), ('40cm', 22.00)], []),
        ('Capri', 27.50, 'sos, ser, szynka, oliwki, papryka, cebulka, oregano', [('20cm', 0), ('30cm', 13.50), ('40cm', 22.00)], []),
        ('Mafioso', 29.50, 'sos, ser, salami, ostra papryka, zielony pieprz, papryka, oregano', [('20cm', 0), ('30cm', 10.00), ('40cm', 18.00)], []),
    ],
    'Śniadania': [
        ('Śniadanie Angielskie', 25.00, '2 jajka, 2 kiełbaski, boczek, pieczona fasolka, pieczarki, warzywa, pieczywo', [], []),
        ('Jajka taplane', 20.00, '3 jajka, pieczywo', [('Klasyczne', 0), ('Z pieczarkami', 3.00), ('Z boczkiem', 4.00)], []),
        ('Śniadanie Firmowe (dla 2 osób)', 49.00, '2 jajka, 2 rodzaje wędlin, 4 rodzaje sera, pomidor, ogórek, oliwki, przetwory owocowe, masło, pieczywo, sosy, kawa/herbata', [], []),
    ],
    'Dania główne': [
        ('Zapiekanka Klasyczna', 14.00, 'sos, ser, pieczarki, oregano', [], []),
        ('Zapiekanka Z Piekła Rodem', 16.00, 'sos, ser, pieczarki, ostra papryka, pomidor, oregano', [], []),
        ('Zapiekanka Kurczak Country', 17.00, 'sos, ser, kurczak, papryka, kukurydza, oregano', [], []),
        ('Zapiekanka Mięsna Fantazja', 17.50, 'sos, ser, kurczak, boczek, szynka, oregano', [], []),
        ('Zapiekanka Boloński Osioł', 17.50, 'sos, ser, salami, cebulka, papryka, oregano', [], []),
        ('Zapiekanka Don Wicio', 19.50, 'sos, ser, oregano', [], ['5 wybranych składników (wpisać w notatce)']),
        ('Zapiekanka Vegetariana', 16.00, 'sos, ser, ogórek, papryka, oliwki, cebulka, oregano', [], []),
        ('Zapiekanka Curry', 17.00, 'sos, ser, kurczak, curry, ananas, oregano', [], []),
        ('Zapiekanka Zbója', 17.00, 'sos, ser, oscypki, ziel. pieprz, papryka, oregano, boczek', [], []),
        ('Zapiekanka Mexico', 17.00, 'sos, ser, kurczak, cz. fasola, kukurydza, ostra papryka, oregano', [], []),
        ('Zapiekanka Pirata', 17.00, 'sos, ser, pieczarki, pomidorki, tuńczyk', [], []),
    ],
    'Sałatki': [
        ('Sałatka Grecka', 25.00, '', [], []),
        ("Sałatka A'la Cezar", 28.00, '', [], []),
        ('Sałatka z tuńczykiem', 25.00, '', [], []),
    ],
    'Dodatki do dań': [
        ('Frytki 300g', 15.00, '', [], []),
        ('Frytki z serem', 19.00, '', [], []),
        ('Frytkowa uczta 600g + 3 sosy', 28.00, '', [], []),
    ],
    'Napoje': [
        ('Kawa czarna', 10.00, '', [], []),
        ('Kawa biała', 12.00, '', [], []),
        ('Latte Macchiato', 13.00, '', [], []),
        ('Ciastko maślane latte', 16.50, '', [], []),
        ('Chocolate cookie latte', 16.50, '', [], []),
        ('Orzechowe latte', 16.50, '', [], []),
        ('Biała czekolada latte', 16.50, '', [], []),
        ('Pistacjowe latte', 16.50, '', [], []),
        ('Espresso', 10.00, '', [], []),
        ('Cappuccino', 13.00, '', [], []),
        ('White chocolate cappuccino', 16.50, '', [], []),
        ('Kolorowe Latte', 16.50, '', [], []),
        ('Herbata', 9.00, '', [], []),
        ('Herbata zimowa', 14.00, '', [], []),
        ('Herbata zimowa z rumem', 19.00, '', [], []),
        ('Gorąca czekolada', 16.00, '', [], []),
        ('Gorąca biała czekolada', 16.00, '', [], []),
        ('Gorąca różowa czekolada', 18.00, '', [], []),
        ('Gorąca niebieska czekolada', 18.00, '', [], []),
        ('Kawa mrożona', 16.00, '', [], []),
        ('Czekolada mrożona', 16.00, '', [], []),
        ('Biała czekolada mrożona', 16.00, '', [], []),
        ('Różowa/Niebieska czekolada mrożona', 18.00, '', [], []),
        ('Bubble Tea', 17.00, '', [], ['smak do wyboru: Granat, Truskawka lub Mango (wpisać w notatce)']),
        ('Woda', 8.00, '', [('300ml', 0), ('1L', 11.00)], []),
        ('Tymbark sok 1L', 24.00, '', [], []),
        ('Tymbark 250ml', 9.00, '', [], []),
        ('Coca-Cola', 9.00, '', [('250ml', 0), ('500ml', 3.00)], []),
        ('Pepsi 500ml', 12.00, '', [], []),
        ('Nestea 0,4L', 10.00, '', [], []),
        ('Kubuś Water 0,4L', 8.50, '', [], []),
    ],
}


class Command(BaseCommand):
    help = 'Seed menu Klitka u Witka Pizzeria'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='Klitka u Witka')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono Klitka u Witka Pizzeria w bazie!'))
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