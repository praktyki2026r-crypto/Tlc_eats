from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem, OptionGroup, Option

def create_item(restaurant, category, name, base_price, ingredients, sizes=None):
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
    help = 'Seed menu Dworcowa'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='Dworcowa')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono Dworcowa w bazie!'))
            return

        Category.objects.filter(restaurant=restaurant).delete()
        self.stdout.write('Usunięto stare dane.')

        # ZUPY
        cat = Category.objects.create(name='Zupy', restaurant=restaurant)
        self.stdout.write('\n[Kategoria] Zupy')
        items = [
            ('Rosół z makaronem', 10, ''),
            ('Rosół z pierożkami z mięsem', 18, ''),
            ('Barszczyk z uszkami z mięsem', 18, ''),
            ('Barszczyk solo', 8, ''),
            ('Żurek z jajkiem i kiełbasą', 18, ''),
            ('Żurek solo', 8, ''),
            ('Pomidorowa z makaronem lub z ryżem', 13, ''),
            ('Flaczki z pieczywem', 20, ''),
        ]
        for name, price, ing in items:
            create_item(restaurant, cat, name, price, ing)
            self.stdout.write(self.style.SUCCESS(f'  Dodano: {name}'))

        # MIĘSA WIEPRZOWE
        cat = Category.objects.create(name='Mięsa wieprzowe', restaurant=restaurant)
        self.stdout.write('\n[Kategoria] Mięsa wieprzowe')
        items = [
            ('Kotlet schabowy', 20, ''),
            ('Karkówka duszona z cebulką', 20, ''),
            ('Schab duszony z cebulką', 20, ''),
            ('Stek ze schabu', 20, ''),
            ('Koperta schabowa panierowana z pieczarkami i serem lub ananasem i serem', 27, 'pieczarki i ser lub ananas i ser (wpisz w notatce)'),
            ('Kotlet mielony lub befsztyk z cebulą 2 szt', 20, 'kotlet mielony lub befsztyk (wpisz w notatce)'),
            ('Gulasz wieprzowy', 20, ''),
            ('Bitki schabowe (2 szt.) w sosie pieczarkowym', 30, ''),
            ('Polędwiczki w sosie kurkowym', 30, ''),
        ]
        for name, price, ing in items:
            create_item(restaurant, cat, name, price, ing)
            self.stdout.write(self.style.SUCCESS(f'  Dodano: {name}'))

        # MIĘSA DROBIOWE
        cat = Category.objects.create(name='Mięsa drobiowe', restaurant=restaurant)
        self.stdout.write('\n[Kategoria] Mięsa drobiowe')
        items = [
            ('Filet drobiowy panierowany', 20, ''),
            ('Pierś grillowana', 22, ''),
            ('Pierś grillowana z sosem serowym', 26, ''),
            ('De Volaille z masłem', 20, ''),
            ('Roladka ze szpinakiem', 22, ''),
            ('Roladka z ogórkiem i papryką', 22, ''),
            ('Roladka z pieczarkami i serem panierowana', 22, ''),
            ('Koperta drobiowa z serem pleśniowym panierowana', 27, ''),
            ('Kurczak po cygańsku', 25, ''),
            ('Kurczak w sosie śmietanowo-porowym', 25, ''),
            ('Nuggetsy 5 szt.', 20, ''),
            ('Bitki 2 szt. duszone z cebulką', 25, ''),
            ('Cordon Blue (szynka + ser żółty panierowany)', 27, ''),
        ]
        for name, price, ing in items:
            create_item(restaurant, cat, name, price, ing)
            self.stdout.write(self.style.SUCCESS(f'  Dodano: {name}'))

        # DANIA Z RYB
        cat = Category.objects.create(name='Dania z ryb', restaurant=restaurant)
        self.stdout.write('\n[Kategoria] Dania z ryb')
        items = [
            ('Łosoś (150g) w sosie porowym', 35, ''),
            ('Miruna panierowana lub w cieście', 22, 'panierowana lub w cieście (wpisz w notatce)'),
            ('Sola panierowana lub w cieście', 22, 'panierowana lub w cieście (wpisz w notatce)'),
            ('Paluszki rybne (4 szt.)', 12, ''),
        ]
        for name, price, ing in items:
            create_item(restaurant, cat, name, price, ing)
            self.stdout.write(self.style.SUCCESS(f'  Dodano: {name}'))

        # DODATKI
        cat = Category.objects.create(name='Dodatki', restaurant=restaurant)
        self.stdout.write('\n[Kategoria] Dodatki')
        items = [
            ('Ziemniaki', 7, ''),
            ('Frytki lub kulki ziemniaczane (200g)', 9, 'frytki lub kulki ziemniaczane (wpisz w notatce)'),
            ('Ćwiartki ziemniaczane', 14, ''),
            ('Ryż', 8, ''),
            ('Kasza kuskus, jęczmienna lub gryczana', 8, 'kuskus, jęczmienna lub gryczana (wpisz w notatce)'),
        ]
        for name, price, ing in items:
            create_item(restaurant, cat, name, price, ing)
            self.stdout.write(self.style.SUCCESS(f'  Dodano: {name}'))

        # SURÓWKI
        cat = Category.objects.create(name='Surówki', restaurant=restaurant)
        self.stdout.write('\n[Kategoria] Surówki')
        items = [
            ('Zestaw 3 surówek', 16, ''),
            ('Bukiet warzyw gotowany', 16, ''),
            ('Marchewka z jabłkiem', 8, ''),
            ('Surówka z czerwonej kapusty', 8, ''),
            ('Buraczki z chrzanem', 8, ''),
            ('Kapusta zasmażana', 9, ''),
            ('Ogórki konserwowe', 6, ''),
            ('Mizeria', 10, ''),
            ('Surówka z białej kapusty i pora', 8, ''),
        ]
        for name, price, ing in items:
            create_item(restaurant, cat, name, price, ing)
            self.stdout.write(self.style.SUCCESS(f'  Dodano: {name}'))

        # PIEROGI
        cat = Category.objects.create(name='Pierogi', restaurant=restaurant)
        self.stdout.write('\n[Kategoria] Pierogi')
        items = [
            ('Pierogi ruskie z cebulką (12 szt.)', 20, ''),
            ('Pierogi ruskie z pieczarkami (12 szt.)', 23, ''),
            ('Pierogi z kapustą (12 szt.)', 20, ''),
            ('Pierogi z kapustą kiszoną i mięsem (12 szt.)', 20, ''),
            ('Pierogi z mięsem (12 szt.)', 20, ''),
            ('Pierogi ze szpinakiem i twarożkiem z sosem czosnkowym (12 szt.)', 20, ''),
        ]
        for name, price, ing in items:
            create_item(restaurant, cat, name, price, ing)
            self.stdout.write(self.style.SUCCESS(f'  Dodano: {name}'))

        # NALEŚNIKI
        cat = Category.objects.create(name='Naleśniki', restaurant=restaurant)
        self.stdout.write('\n[Kategoria] Naleśniki')
        items = [
            ('Naleśniki z dżemem', 20, '3 szt. naleśników, dżem'),
            ('Naleśniki z serem', 20, '2 szt. naleśników, ser'),
            ('Naleśniki z dżemem, owocami i bitą śmietaną', 17, '1 szt. naleśników, dżem, owoce, bita śmietana'),
            ('Naleśniki ze szpinakiem', 22, '2 szt. naleśników ze szpinakiem, sos czosnkowy'),
            ('Naleśniki z pieczarkami i serem', 22, '2 szt. naleśników z pieczarkami i serem, ketchup'),
        ]
        for name, price, ing in items:
            create_item(restaurant, cat, name, price, ing)
            self.stdout.write(self.style.SUCCESS(f'  Dodano: {name}'))

        # DANIA RÓŻNE
        cat = Category.objects.create(name='Dania główne', restaurant=restaurant)
        self.stdout.write('\n[Kategoria] Dania główne')
        items = [
            ('Placki solo + sos pieczarkowy', 25, ''),
            ('Placek po węgiersku mały + 2 surówki', 25, ''),
            ('Placek po węgiersku duży + 3 surówki', 40, ''),
            ('Placki ziemniaczane solo (3 szt.)', 15, ''),
            ('Półmisek wegetariański', 45, 'frytki, kulki, ser prażony żółty lub pleśniowy, zestaw 3 surówek; ser do wyboru (wpisz w notatce)'),
            ('Ser żółty prażony z żurawiną', 20, ''),
            ('Paluszki serowe, frytki lub kulki + sos', 27, 'frytki lub kulki (wpisz w notatce)'),
            ('Makaron wstążki z łososiem w sosie śmietanowym', 45, ''),
            ('Makaron ze szpinakiem', 30, ''),
            ('Kurczak w sosie serowym z ryżem', 30, ''),
            ('Jajecznica (3 jajka), masło, pieczywo', 17, ''),
            ('Kiełbasa grillowana z musztardą i pieczywem', 22, ''),
            ('Wątróbka drobiowa z cebulką', 15, ''),
            ('Hamburger własnej produkcji', 16, ''),
            ('Cheeseburger własnej produkcji', 20, ''),
            ('Zapiekanka z pieczarkami', 13, ''),
            ('Frytki duże (350g)', 12, ''),
        ]
        for name, price, ing in items:
            create_item(restaurant, cat, name, price, ing)
            self.stdout.write(self.style.SUCCESS(f'  Dodano: {name}'))

        # SAŁATKI
        cat = Category.objects.create(name='Sałatki', restaurant=restaurant)
        self.stdout.write('\n[Kategoria] Sałatki')
        items = [
            ('Szefa kuchni', 35, 'ryż, kurczak, winogrona, słonecznik prażony'),
            ('Firmowa', 35, 'seler naciowy, kurczak, ananas, sos majonezowy'),
            ('Cesar', 35, 'sałata lodowa, kurczak, anchois, kapary, boczek, grzanki, sos winegret'),
            ('Grecka', 25, 'sałata lodowa, ser feta, pomidor, ogórek, oliwki, cebula czerwona, sos winegret'),
            ('Z tuńczykiem', 35, 'kapusta pekińska, tuńczyk, pomidor, ogórek, kukurydza, cebula czerwona, sos jogurtowo-majonezowy'),
        ]
        for name, price, ing in items:
            create_item(restaurant, cat, name, price, ing)
            self.stdout.write(self.style.SUCCESS(f'  Dodano: {name}'))

        # DODATKI DO DAŃ
        cat = Category.objects.create(name='Dodatki', restaurant=restaurant)
        self.stdout.write('\n[Kategoria] Dodatki')
        items = [
            ('Pieczywo / pieczarki', 3, 'pieczywo lub pieczarki (wpisz w notatce)'),
            ('Ser żółty', 3, ''),
            ('Śmietana', 2, ''),
            ('Sos czosnkowy / ketchup', 3, 'sos czosnkowy lub ketchup (wpisz w notatce)'),
        ]
        for name, price, ing in items:
            create_item(restaurant, cat, name, price, ing)
            self.stdout.write(self.style.SUCCESS(f'  Dodano: {name}'))

        # DESERY
        cat = Category.objects.create(name='Desery', restaurant=restaurant)
        self.stdout.write('\n[Kategoria] Desery')
        items = [
            ('Gofry z owocami i bitą śmietaną', 25, '2 szt. gofrów, bita śmietana'),
            ('Gofry z cukrem pudrem', 18, '2 szt. gofrów, cukier puder'),
            ('Gofry z dżemem', 20, '2 szt. gofrów, dżem'),
            ('Sernik', 7, 'sernik'),
            ('Szarlotka', 7, 'szarlotka'),
            ('Szarlotka z lodami i bitą śmietaną', 20, 'szarlotka, lody, bita śmietana'),
            ('Pucharek lodowy z owocami i bitą śmietaną', 20, 'lody, owoce, bita śmietana'),
            ('Koktajl jogurtowo-owocowy', 14, 'Koktajl jogurtowo-owocowy'),
        ]
        for name, price, ing in items:
            create_item(restaurant, cat, name, price, ing)
            self.stdout.write(self.style.SUCCESS(f'  Dodano: {name}'))

        # NAPOJE GORĄCE
        cat = Category.objects.create(name='Napoje', restaurant=restaurant)
        self.stdout.write('\n[Kategoria] Napoje')
        items = [
            ('Kawa Espresso', 10, ''),
            ('Kawa Latte', 14, ''),
            ('Kawa parzona', 8, ''),
            ('Kawa rozpuszczalna', 8, ''),
            ('Cappuccino', 14, ''),
            ('Herbata z cytryną', 5, ''),
            ('Herbata zielona / owocowa', 8, 'zielona lub owocowa (wpisz w notatce)'),
            ('Kompot', 3, ''),
        ]
        for name, price, ing in items:
            create_item(restaurant, cat, name, price, ing)
            self.stdout.write(self.style.SUCCESS(f'  Dodano: {name}'))

        # NAPOJE ZIMNE
        cat = Category.objects.create(name='Napoje', restaurant=restaurant)
        self.stdout.write('\n[Kategoria] Napoje')

        create_item(restaurant, cat,
            'Woda mineralna', 4, 'gazowana lub niegazowana (wpisz w notatce)',
            sizes=[('0.2l', 0), ('0.5l', 1)])
        self.stdout.write(self.style.SUCCESS('  Dodano: Woda mineralna'))

        items = [
            ('Napój Tymbark 0.5l', 7, ''),
            ('Pepsi 0.5l', 8, ''),
            ('Sok 100% 0.3l', 8, ''),
        ]
        for name, price, ing in items:
            create_item(restaurant, cat, name, price, ing)
            self.stdout.write(self.style.SUCCESS(f'  Dodano: {name}'))

        self.stdout.write(self.style.SUCCESS('\nGotowe!'))