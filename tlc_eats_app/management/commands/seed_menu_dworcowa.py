from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem

MENU = {
    'Zestawy lunchowe': [
        ('Zestaw dnia (zupa, II danie, kompot)', 30, ''),
        ('Zupa dnia', 10, ''),
        ('II danie z kompotem', 25, ''),
    ],
    'Zupy': [
        ('Rosół z makaronem', 10, ''),
        ('Rosół z pierożkami z mięsem', 18, ''),
        ('Barszczyk z uszkami z mięsem', 18, ''),
        ('Barszczyk solo', 8, ''),
        ('Żurek z jajkiem i kiełbasą', 18, ''),
        ('Żurek solo', 8, ''),
        ('Pomidorowa z makaronem lub z ryżem', 13, ''),
        ('Flaczki z pieczywem', 20, ''),
    ],
    'Mięsa wieprzowe': [
        ('Kotlet schabowy', 20, ''),
        ('Karkówka duszona z cebulką', 20, ''),
        ('Schab duszony z cebulką', 20, ''),
        ('Stek ze schabu', 20, ''),
        ('Koperta schabowa panierowana z pieczarkami i serem lub ananasem i serem', 27, ''),
        ('Kotlet mielony lub befsztyk z cebulą 2 szt', 20, ''),
        ('Gulasz wieprzowy', 20, ''),
        ('Bitki schabowe (2 szt.) w sosie pieczarkowym', 30, ''),
        ('Polędwiczki w sosie kurkowym', 30, ''),
    ],
    'Mięsa drobiowe': [
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
        ('Nuggetsy (5 szt.)', 20, ''),
        ('Bitki (2 szt.) duszone z cebulką', 25, ''),
        ('Cordon Blue (szynka + ser żółty panierowany)', 27, ''),
    ],
    'Dania z ryb': [
        ('Łosoś (150g) w sosie porowym', 35, ''),
        ('Miruna panierowana lub w cieście', 22, ''),
        ('Sola panierowana lub w cieście', 22, ''),
        ('Paluszki rybne (4 szt.)', 12, ''),
    ],
    'Dodatki': [
        ('Ziemniaki', 7, ''),
        ('Frytki lub kulki ziemniaczane (200g)', 9, ''),
        ('Ćwiartki ziemniaczane', 14, ''),
        ('Ryż', 8, ''),
        ('Kasza kuskus, jęczmienna lub gryczana', 8, ''),
    ],
    'Surówki': [
        ('Zestaw 3 surówek', 16, ''),
        ('Bukiet warzyw gotowany', 16, ''),
        ('Marchewka z jabłkiem', 8, ''),
        ('Surówka z czerwonej kapusty', 8, ''),
        ('Buraczki z chrzanem', 8, ''),
        ('Kapusta zasmażana', 9, ''),
        ('Ogórki konserwowe', 6, ''),
        ('Mizeria', 10, ''),
        ('Surówka z białej kapusty i pora', 8, ''),
    ],
    'Pierogi': [
        ('Pierogi ruskie z cebulką (12 szt.)', 20, ''),
        ('Pierogi ruskie z pieczarkami (12 szt.)', 23, ''),
        ('Pierogi z kapustą (12 szt.)', 20, ''),
        ('Pierogi z kapustą kiszoną i mięsem (12 szt.)', 20, ''),
        ('Pierogi z mięsem (12 szt.)', 20, ''),
        ('Pierogi ze szpinakiem i twarożkiem z sosem czosnkowym (12 szt.)', 20, ''),
    ],
    'Naleśniki': [
        ('Naleśniki z dżemem (3 szt.)', 20, ''),
        ('Naleśniki z serem (2 szt.)', 20, ''),
        ('Naleśniki z dżemem, owocami i bitą śmietaną (1 szt.)', 17, ''),
        ('Naleśniki ze szpinakiem (2 szt.) + sos czosnkowy', 22, ''),
        ('Naleśniki z pieczarkami i serem (2 szt.) + ketchup', 22, ''),
    ],
    'Dania różne': [
        ('Placki solo + sos pieczarkowy', 25, ''),
        ('Placek po węgiersku mały + 2 surówki', 25, ''),
        ('Placek po węgiersku duży + 3 surówki', 40, ''),
        ('Placki ziemniaczane solo (3 szt.)', 15, ''),
        ('Półmisek wegetariański', 45, 'frytki, kulki, ser prażony żółty lub pleśniowy, zestaw 3 surówek'),
        ('Ser żółty prażony z żurawiną', 20, ''),
        ('Paluszki serowe, frytki lub kulki + sos', 27, ''),
        ('Makaron wstążki z łososiem w sosie śmietanowym', 45, ''),
        ('Makaron ze szpinakiem', 30, ''),
        ('Kurczak w sosie serowym z ryżem', 30, ''),
        ('Jajecznica (3 jajka), masło, pieczywo', 17, ''),
        ('Kiełbasa grillowana z musztardą i pieczywem', 22, ''),
        ('Wątróbka drobiowa z cebulką', 15, ''),
        ('Hamburger własnej produkcji', 16, ''),
        ('Cheeseburger własnej produkcji', 20, ''),
        ('Zapiekanka z pieczarkami, serem i ketchupem', 13, ''),
        ('Frytki duże (350g)', 12, ''),
    ],
    'Sałatki': [
        ('Szefa kuchni', 35, 'ryż, kurczak, winogrona, słonecznik prażony'),
        ('Firmowa', 35, 'seler naciowy, kurczak, ananas, sos majonezowy'),
        ('Cesar', 35, 'sałata lodowa, kurczak, anchois, kapary, boczek, grzanki, sos winegret'),
        ('Grecka', 25, 'sałata lodowa, ser feta, pomidor, ogórek, oliwki, cebula czerwona, sos winegret'),
        ('Z tuńczykiem', 35, 'kapusta pekińska, tuńczyk, pomidor, ogórek, kukurydza, cebula czerwona, sos jogurtowo-majonezowy'),
    ],
    'Dodatki do dań': [
        ('Pieczywo / pieczarki', 3, ''),
        ('Ser żółty', 3, ''),
        ('Śmietana', 2, ''),
        ('Sos czosnkowy / ketchup', 3, ''),
    ],
    'Desery': [
        ('Gofry z owocami i bitą śmietaną (2 szt.)', 25, ''),
        ('Gofry z cukrem pudrem (2 szt.)', 18, ''),
        ('Gofry z dżemem (2 szt.)', 20, ''),
        ('Sernik', 7, ''),
        ('Szarlotka', 7, ''),
        ('Szarlotka z lodami i bitą śmietaną', 20, ''),
        ('Pucharek lodowy z owocami i bitą śmietaną', 20, ''),
        ('Koktajl jogurtowo-owocowy', 14, ''),
    ],
    'Napoje gorące': [
        ('Kawa Espresso', 10, ''),
        ('Kawa Latte', 14, ''),
        ('Kawa parzona', 8, ''),
        ('Kawa rozpuszczalna', 8, ''),
        ('Cappuccino', 14, ''),
        ('Herbata z cytryną', 5, ''),
        ('Herbata zielona lub owocowa', 8, ''),
        ('Śmietanka do kawy (2 szt.)', 2, ''),
        ('Cytryna', 2, ''),
        ('Kompot', 3, ''),
    ],
    'Napoje zimne': [
        ('Woda mineralna 0.2l', 4, ''),
        ('Woda mineralna 0.5l', 5, ''),
        ('Napój Tymbark 0.5l', 7, ''),
        ('Pepsi 0.5l', 8, ''),
        ('Sok 100% 0.3l', 8, ''),
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