from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem, OptionGroup, Option

MENU = {
    'Pizza na grubym cieście': [
        # (name, base_price(mała), ingredients, sizes[(label, extra_price)], addons)
        ('Rafaello - specjalność zakładu', 14.50, 'sos pomidorowy, ser, szynka, pieczarki, kurczak, kukurydza', [('Mała', 0), ('Średnia', 6.00), ('Duża', 13.00), ('B. duża', 21.00)], []),
        ('Neapolitana', 14.50, 'sos pomidorowy, ser, pieczarki, cebula, salami, oliwki zielone, ananas, bazylia', [('Mała', 0), ('Średnia', 6.00), ('Duża', 13.00), ('B. duża', 21.00)], []),
        ('Tropicana', 14.00, 'sos pomidorowy, ser, szynka, ananas', [('Mała', 0), ('Średnia', 5.00), ('Duża', 12.00), ('B. duża', 20.50)], []),
        ('Marinara', 14.50, 'sos pomidorowy, ser, tuńczyk, kukurydza', [('Mała', 0), ('Średnia', 5.00), ('Duża', 12.00), ('B. duża', 19.50)], []),
        ('Capriciossa', 13.50, 'sos pomidorowy, ser, szynka, pieczarki', [('Mała', 0), ('Średnia', 4.50), ('Duża', 12.00), ('B. duża', 20.00)], []),
        ('Wegetariańska', 15.50, 'sos pomidorowy, ser, pieczarki, cebula, kukurydza, papryka, groszek zielony, szparaga', [('Mała', 0), ('Średnia', 5.00), ('Duża', 12.50), ('B. duża', 20.50)], []),
        ('Princessa', 15.00, 'sos pomidorowy, ser, szynka, cebula, papryka, oliwki', [('Mała', 0), ('Średnia', 6.00), ('Duża', 13.00), ('B. duża', 21.00)], []),
        ('Pepperoni - pikantna', 15.50, 'sos pomidorowy, ser, pieczarki, cebula, czosnek, salami, papryka, chili', [('Mała', 0), ('Średnia', 6.00), ('Duża', 13.00), ('B. duża', 20.50)], []),
        ('Amore', 14.50, 'sos pomidorowy, ser, szynka, pieczarki, kurczak', [('Mała', 0), ('Średnia', 5.50), ('Duża', 12.50), ('B. duża', 20.50)], []),
        ('Roberto', 15.00, 'sos pomidorowy, ser, pieczarki, boczek, czosnek, cebula', [('Mała', 0), ('Średnia', 6.00), ('Duża', 12.50), ('B. duża', 20.50)], []),
        ('Indiana', 15.50, 'sos pomidorowy, ser, tuńczyk, oliwki, majonez', [('Mała', 0), ('Średnia', 5.50), ('Duża', 12.00), ('B. duża', 20.50)], []),
        ('La Bella', 15.50, 'sos pomidorowy, ser, szynka, tuńczyk, papryka', [('Mała', 0), ('Średnia', 5.50), ('Duża', 11.50), ('B. duża', 19.50)], []),
        ('Amigo', 14.50, 'sos pomidorowy, ser, salami, cebula, papryka, oliwki', [('Mała', 0), ('Średnia', 6.00), ('Duża', 12.50), ('B. duża', 21.50)], []),
        ('Pigala', 15.50, 'sos pomidorowy, ser, tuńczyk, cebula, jajko', [('Mała', 0), ('Średnia', 5.50), ('Duża', 12.00), ('B. duża', 20.50)], []),
        ('Matador', 15.50, 'sos pomidorowy, ser, szynka, cebula, boczek, salami, peperoni', [('Mała', 0), ('Średnia', 6.00), ('Duża', 13.00), ('B. duża', 20.50)], []),
        ('Classica', 15.50, 'sos pomidorowy, ser, kiełbasa wiejska, cebula, boczek, pieczarki, jajko, oregano', [('Mała', 0), ('Średnia', 6.00), ('Duża', 13.00), ('B. duża', 20.50)], []),
        ('Frutti di mare', 16.50, 'sos pomidorowy, ser, małże, krewetki, ośmiornice, kraby, papryka', [('Mała', 0), ('Średnia', 6.00), ('Duża', 13.50), ('B. duża', 21.50)], []),
        ('Meksikana', 14.50, 'sos pomidorowy, ser, kurczak, pieczarki, groszek zielony, kukurydza, cebula', [('Mała', 0), ('Średnia', 6.50), ('Duża', 13.00), ('B. duża', 21.50)], []),
        ('Primawera', 15.00, 'sos pomidorowy, ser, szynka, pieczarki, cebula, kiełbasa wiejska', [('Mała', 0), ('Średnia', 6.50), ('Duża', 13.50), ('B. duża', 21.50)], []),
        ('Killer - pizza do piwa', 15.50, 'sos pomidorowy, ser, salami, wieprzowina, pepperoni, oliwki, pieczarki, sos tabasco', [('Mała', 0), ('Średnia', 6.50), ('Duża', 13.50), ('B. duża', 21.00)], []),
        ('Exotica', 14.50, 'sos pomidorowy, ser, kurczak, ananas, kukurydza', [('Mała', 0), ('Średnia', 5.50), ('Duża', 13.00), ('B. duża', 20.50)], []),
        ('Max Boss', 15.50, 'sos pomidorowy, ser, pieczarki, wieprzowina, kiełbasa wiejska, cebula, papryka, ogórek', [('Mała', 0), ('Średnia', 6.50), ('Duża', 13.50), ('B. duża', 21.00)], []),
        ('Verona', 15.00, 'sos pomidorowy, ser, pieczarki, cebula, papryka, szynka, pomidory', [('Mała', 0), ('Średnia', 6.00), ('Duża', 13.00), ('B. duża', 21.00)], []),
        ('Tosca', 15.00, 'sos pomidorowy, ser, pieczarki, cebula, szynka, groszek, fasolka czerwona, pomidory, ogórek', [('Mała', 0), ('Średnia', 6.00), ('Duża', 13.00), ('B. duża', 21.00)], []),
        ('Fantazja - kompozycja własna (grube ciasto)', 12.50, 'sos pomidorowy, ser', [('Mała', 0), ('Średnia', 4.00), ('Duża', 9.50), ('B. duża', 17.00)], ['wybór składników (wpisać w notatce)']),
    ],
    'Pizza na cienkim cieście': [
        ('Rafaello (cienkie)', 21.00, 'sos pomidorowy, ser, szynka, pieczarki, kurczak, kukurydza', [('24cm', 0), ('30cm', 7.00)], []),
        ('Tomaso', 18.00, 'sos pomidorowy, ser, szynka, pieczarki', [('24cm', 0), ('30cm', 6.50)], []),
        ('Toledo', 20.50, 'sos pomidorowy, ser, kurczak, boczek, kukurydza, pomidor', [('24cm', 0), ('30cm', 7.00)], []),
        ('Wezuvio', 20.50, 'sos pomidorowy, ser, salami, peperoni, pieczarki, chili', [('24cm', 0), ('30cm', 7.00)], []),
        ('Mista', 20.00, 'sos pomidorowy, ser, pieczarki, wieprzowina, ogórek, fasolka czerwona', [('24cm', 0), ('30cm', 7.00)], []),
        ('Napolli', 19.00, 'sos pomidorowy, ser, salami, pieczarki, cebula, oliwki', [('24cm', 0), ('30cm', 7.00)], []),
        ('Calzone (w kształcie muszli)', 23.50, 'sos pomidorowy, ser, szynka, oliwki, kukurydza', [('24cm', 0), ('30cm', 3.00)], []),
        ('Tonno', 20.00, 'sos pomidorowy, ser, tuńczyk, oliwki, papryka', [('24cm', 0), ('30cm', 7.00)], []),
        ('Di Pollo', 20.00, 'sos pomidorowy, ser, pieczarki, groszek, pomidor, kukurydza, fasolka czerwona', [('24cm', 0), ('30cm', 7.00)], []),
        ('Salerno', 20.50, 'sos pomidorowy, ser, pieczarki, mięso grillowane, cebula, oliwki, sos czosnkowy', [('24cm', 0), ('30cm', 7.00)], []),
        ('Fantazja - kompozycja własna (cienkie ciasto)', 16.50, 'sos pomidorowy, ser', [('24cm', 0), ('30cm', 5.00)], ['wybór składników (wpisać w notatce)']),
    ],
    'Dodatki do pizzy': [
        ('Warzywa i owoce', 1.50, 'czosnek, cebula, kukurydza, papryka, pomidor, pieczarki, groszek zielony, oliwki, peperoni, fasolka, ananas, banan, ogórek', [('Mała 19cm', 0), ('Średnia 23cm', 0.50), ('Duża 27cm', 1.00), ('B. duża 31cm', 1.50)], []),
        ('Mięsne', 2.00, 'szynka, kurczak, salami, boczek, kiełbasa wiejska, wieprzowina', [('Mała 19cm', 0), ('Średnia 23cm', 0.50), ('Duża 27cm', 1.50), ('B. duża 31cm', 2.00)], []),
        ('Ketchup', 0.50, '', [('Mała 19cm', 0), ('Średnia 23cm', 0.50), ('Duża 27cm', 0.50), ('B. duża 31cm', 1.00)], []),
        ('Tuńczyk', 1.50, '', [('Mała 19cm', 0), ('Średnia 23cm', 1.00), ('Duża 27cm', 2.00), ('B. duża 31cm', 2.50)], []),
        ('Owoce morza', 3.00, '', [('Mała 19cm', 0), ('Średnia 23cm', 1.00), ('Duża 27cm', 2.00), ('B. duża 31cm', 3.00)], []),
        ('Jajko', 1.00, '', [], []),
        ('Ser', 2.50, '', [('Mała 19cm', 0), ('Średnia 23cm', 0.50), ('Duża 27cm', 1.00), ('B. duża 31cm', 2.00)], []),
        ('Opakowanie do pizzy', 1.00, '', [('Mała 19cm', 0), ('Średnia 23cm', 0.50), ('Duża 27cm', 0.50), ('B. duża 31cm', 1.00)], []),
        ('Opakowanie na pozostałe dania', 1.00, '', [], []),
        ('Sos do wyboru', 2.00, '', [], ['pomidorowo-czosnkowy, czosnkowy lub majonez (wpisać w notatce)']),
    ],
    'Sałatki / Dania Barowe': [
        ('Sałatka Morska', 14.00, 'kapusta pekińska, pomidor, kukurydza, papryka, groszek zielony, tuńczyk, cebula, sos vinaigrette', [], []),
        ('Sałatka Wegetariańska', 12.00, 'kapusta pekińska, kukurydza, papryka, pomidor, groszek zielony, sos vinaigrette', [], []),
        ('Sałatka z kurczakiem', 13.00, 'kapusta pekińska, kurczak, pomidor, kukurydza, papryka, cebula, groszek zielony, sos vinaigrette', [], []),
        ('Sałatka z szynką', 13.00, 'kapusta pekińska, pomidor, kukurydza, papryka, groszek zielony, szynka, sos vinaigrette', [], []),
        ('Sałatka z serem Feta', 14.50, 'kapusta pekińska, ser Feta, pomidor, ogórek, oliwki, cebula, sos vinaigrette', [], []),
        ('Bułeczki Rafaello (3 szt)', 4.50, '', [], []),
        ('Pierogi ruskie', 16.00, '', [('12 szt', 0)], []),
        ('Pierogi ruskie z boczkiem i śmietaną', 17.00, 'boczek, śmietana', [('12 szt', 0)], []),
        ('Pierogi ruskie w sosie borowikowo-pieczarkowym', 17.00, 'sos borowikowo-pieczarkowy', [('12 szt', 0)], []),
        ('Pierogi z kapustą', 17.00, '', [('12 szt', 0)], []),
        ('Pierogi z kapustą i mięsem', 18.00, '', [('12 szt', 0)], []),
        ('Naleśniki z pieczarkami i żółtym serem', 14.00, 'pieczarki, żółty ser', [('2 szt', 0)], []),
        ('Lasagne', 15.00, '', [], []),
        ('Frytki', 6.00, '', [('150g', 0), ('250g', 3.00)], []),
        ('Frytki z serem', 6.50, '', [('170g', 0), ('300g', 3.50)], []),
        ('Zapiekanka', 11.00, '', [], []),
        ('Hamburger', 9.50, '', [], []),
    ],
    'Napoje': [
        ('Coca Cola 0,5l', 9.00, '', [], []),
        ('Fanta 0,5l', 9.00, '', [], []),
        ('Sprite 0,5l', 9.00, '', [], []),
    ],
}

class Command(BaseCommand):
    help = 'Seed menu Rafaello Pizzeria'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='Rafaello Pizzeria')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono Rafaello Pizzeria w bazie!'))
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