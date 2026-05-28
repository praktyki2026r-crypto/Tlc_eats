from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem, OptionGroup, Option

MENU = {
    'Zupy': [
        ('Rosół z makaronem', 10, '', []),
        ('Rosół z pierożkami z mięsem', 18, '', []),
        ('Barszczyk z uszkami z mięsem', 18, '', []),
        ('Barszczyk solo', 8, '', []),
        ('Żurek z jajkiem i kiełbasą', 18, '', []),
        ('Żurek solo', 8, '', []),
        ('Pomidorowa z makaronem lub z ryżem', 13, '', []),
        ('Flaczki z pieczywem', 20, '', []),
    ],
    'Dania główne': [
        ('Kotlet schabowy', 20, '', []),
        ('Karkówka duszona z cebulką', 20, '', []),
        ('Schab duszony z cebulką', 20, '', []),
        ('Stek ze schabu', 20, '', []),
        ('Koperta schabowa panierowana', 27, 'pieczarki i ser lub ananas i ser (wpisz w notatce)', []),
        ('Kotlet mielony lub befsztyk z cebulą', 20, 'kotlet mielony lub befsztyk (wpisz w notatce)', []),
        ('Gulasz wieprzowy', 20, '', []),
        ('Bitki schabowe w sosie pieczarkowym', 30, '2szt.', []),
        ('Polędwiczki w sosie kurkowym', 30, '', []),
        ('Filet drobiowy panierowany', 20, '', []),
        ('Pierś grillowana', 22, '', []),
        ('Pierś grillowana z sosem serowym', 26, '', []),
        ('De Volaille z masłem', 20, '', []),
        ('Roladka ze szpinakiem', 22, '', []),
        ('Roladka z ogórkiem i papryką', 22, '', []),
        ('Roladka z pieczarkami i serem panierowana', 22, '', []),
        ('Koperta drobiowa z serem pleśniowym panierowana', 27, '', []),
        ('Kurczak po cygańsku', 25, '', []),
        ('Kurczak w sosie śmietanowo-porowym', 25, '', []),
        ('Nuggetsy', 20, '',[('5 szt.', 0)], []),
        ('Bitki duszone z cebulką', 25, '2szt.', []),
        ('Cordon Blue', 27, 'szynka, ser żółty panierowany', []),
        ('Placki solo + sos pieczarkowy', 25, '', []),
        ('Placek po węgiersku mały', 25, 'Placek po węgiersku mały, dwie surówki', []),
        ('Placek po węgiersku duży', 40, 'Placek po węgiersku duży, trzy surówki', []),
        ('Placki ziemniaczane solo', 15, '',[('3 szt.', 0)], []),
        ('Półmisek wegetariański', 45, 'frytki, kulki, ser prażony żółty lub pleśniowy, zestaw 3 surówek; ser do wyboru (wpisz w notatce)', []),
        ('Ser żółty prażony z żurawiną', 20, '', []),
        ('Paluszki serowe', 27, 'frytki lub kulki, sos', []),
        ('Makaron wstążki z łososiem w sosie śmietanowym', 45, '', []),
        ('Makaron ze szpinakiem', 30, '', []),
        ('Kurczak w sosie serowym z ryżem', 30, '', []),
        ('Jajecznica, masło, pieczywo', 17, 'jajecznica z 3 jajek', []),
        ('Kiełbasa grillowana', 22, 'kiełbasa z pieczywem oraz musztarda', []),
        ('Wątróbka drobiowa z cebulką', 15, '', []),
        ('Hamburger', 16, '', []),
        ('Cheeseburger', 20, '', []),
        ('Zapiekanka z pieczarkami', 13, '', []),
        ('Frytki duże', 12, '',[('350 g', 0)], []),
        ('Łosoś w sosie porowym', 35, '',[('150 g', 0)], []),
        ('Ryba Miruna', 22, 'panierowana lub w cieście (wpisz w notatce)', []),
        ('Ryba Sola', 22, 'panierowana lub w cieście (wpisz w notatce)', []),
        ('Paluszki rybne', 12, '',[('4 szt.', 0)], []),
        ('Pierogi ruskie z cebulką', 20, '',[('12 szt.', 0)], []),
        ('Pierogi ruskie z pieczarkami', 23, '',[('12 szt.', 0)], []),
        ('Pierogi z kapustą', 20, '',[('12 szt.', 0)], []),
        ('Pierogi z kapustą kiszoną i mięsem', 20, '',[('12 szt.', 0)], []),
        ('Pierogi z mięsem', 20, '',[('12 szt.', 0)], []),
        ('Pierogi ze szpinakiem i twarożkiem', 20, 'Pierogi ze szpinakiem i twarożkiem, sos czosnkowy',[('12 szt.', 0)], []),
        ('Naleśniki z dżemem', 20, 'naleśniki, dżem',[('3 szt.', 0)],  []),
        ('Naleśniki z serem', 20, 'naleśniki, ser',[('2 szt.', 0)], []),
        ('Naleśniki z dżemem, owocami i bitą śmietaną', 17, ' naleśniki, dżem, owoce, bita śmietana',[('1 szt.', 0)], []),
        ('Naleśniki ze szpinakiem', 22, 'Naleśniki ze szpinakiem, sos czosnkowy',[('2 szt.', 0)], []),
        ('Naleśniki z pieczarkami i serem', 22, 'naleśniki z pieczarkami i serem, ketchup', [('2 szt.', 0)],[]),
    ],
    
    'Sałatki': [
        ('Sałatka szefa kuchni', 35, 'ryż, kurczak, winogrona, słonecznik prażony', []),
        ('Sałatka firmowa', 35, 'seler naciowy, kurczak, ananas, sos majonezowy', []),
        ('Sałatka cesar', 35, 'sałata lodowa, kurczak, anchois, kapary, boczek, grzanki, sos winegret', []),
        ('Sałatka grecka', 25, 'sałata lodowa, ser feta, pomidor, ogórek, oliwki, cebula czerwona, sos winegret', []),
        ('Sałatka z tuńczykiem', 35, 'kapusta pekińska, tuńczyk, pomidor, ogórek, kukurydza, cebula czerwona, sos jogurtowo-majonezowy', []),
    ],

    'Dodatki': [
        ('Ziemniaki', 7, '', []),
        ('Frytki lub kulki ziemniaczane', 9, '200g', []),
        ('Ćwiartki ziemniaczane', 14, '', []),
        ('Ryż', 8, '', []),
        ('Kasza kuskus, jęczmienna lub gryczana', 8, 'kuskus, jęczmienna lub gryczana (wpisz w notatce)', []),
        ('Zestaw 3 surówek', 16, '', []),
        ('Bukiet warzyw gotowany', 16, '', []),
        ('Marchewka z jabłkiem', 8, '', []),
        ('Surówka z czerwonej kapusty', 8, '', []),
        ('Buraczki z chrzanem', 8, '', []),
        ('Kapusta zasmażana', 9, '', []),
        ('Ogórki konserwowe', 6, '', []),
        ('Mizeria', 10, '', []),
        ('Surówka z białej kapusty i pora', 8, '', []),
        ('Pieczywo / pieczarki', 3, 'pieczywo lub pieczarki (wpisz w notatce)', []),
        ('Ser żółty', 3, '', []),
        ('Śmietana', 2, '', []),
        ('Sos czosnkowy / ketchup', 3, 'sos czosnkowy lub ketchup (wpisz w notatce)', []),
    ],

    'Desery': [
        ('Gofry z owocami i bitą śmietaną', 25, 'gofry, bita śmietana',[('2 szt.', 0)], []),
        ('Gofry z cukrem pudrem', 18, 'gofry, cukier puder',[('2 szt.', 0)], []),
        ('Gofry z dżemem', 20, 'gofry, dżem',[('2 szt.', 0)], []),
        ('Sernik', 7, '', []),
        ('Szarlotka', 7, '', []),
        ('Koktajl jogurtowo-owocowy', 14, '', []),
    ],
    'Napoje': [
        ('Kawa Espresso', 10, '', []),
        ('Kawa Latte', 14, '', []),
        ('Kawa parzona', 8, '', []),
        ('Kawa rozpuszczalna', 8, '', []),
        ('Cappuccino', 14, '', []),
        ('Herbata z cytryną', 5, '', []),
        ('Herbata zielona / owocowa', 8, 'zielona lub owocowa (wpisz w notatce)', []),
        ('Kompot', 3, '', []),
        ('Woda mineralna', 4, 'gazowana lub niegazowana (wpisz w notatce)', [('0.2l', 0), ('0.5l', 1)]),
        ('Napój Tymbark 0.5l', 7, '', []),
        ('Pepsi 0.5l', 8, '', []),
        ('Sok 100% 0.3l', 8, '', []),
    ],
}


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
                        )
                        self.stdout.write(f'    Rozmiar: {label} ({extra_price:+.2f} zł)')

        self.stdout.write(self.style.SUCCESS('\nGotowe!'))