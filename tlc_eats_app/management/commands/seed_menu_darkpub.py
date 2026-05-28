from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem, OptionGroup, Option

MENU = {
    'Przystawki': [
        ('Tatar z polędwicy wołowej', 52.00, 'siekany z poszatkowaną cebulą, grzybami, ogórkiem, anchois, kaparami i żółtkiem', []),
        ('Krewetki tygrysie', 49.00, 'czosnek, chilli, natka pietruszki, bułeczki', []),
        ('Przekąska piwna', 73.00, '', []),
        ('Skrzydełka', 36.00, 'na ostro lub z sosem BBQ (wpisz w notatce)', [('400g', 0)]),
        ('Ćwiartki', 25.00, 'ziemniaki z sosami', []),
        ('Paluchy drożdżowe', 22.00, 'z sosem', []),
        ('Frytki belgijskie', 23.00, 'z sosem', []),
    ],
    'Zupy': [
        ('Rosół', 17.00, 'drobiowo-wołowy z makaronem', []),
        ('Barszcz czerwony', 18.00, 'uszka faszerowane mięsem', []),
        ('Żurek', 18.00, 'jajko, kiełbasa, pieczywo', []),
    ],
    'Dania główne': [
        ('Stek', 140.00, 'polędwica wołowa, pieczarki, smażona cebula, kukurydza, frytki, sos pieprzowy', []),
        ('Łosoś', 51.00, 'puree ziemniaczane, zielone szparagi, pieczone buraki, sos maślany', []),
        ('Pierś z kaczki', 46.00, 'sos żurawinowy, gnocchi, zielona sałatka ze słodkim vinaigrette', []),
        ('Placek po Węgiersku', 35.00, 'placki ziemniaczane, gulasz wieprzowy, śmietana, ser żółty, zestaw surówek', [('Mały', 0), ('Duży', 9.00)]),
        ('Kurczak na gorącym półmisku', 50.00, 'marynata orientalna, smażony z cebulą, ryż, surówka z białej kapusty, sos nuoc chan', []),
        ('Golonka pieczona na gorącym półmisku', 47.00, 'masło ziołowe, opiekane ziemniaki z tymiankiem, ogórek kiszony, chrzan, musztarda', []),
        ('Kotlet schabowy', 40.00, 'ziemniaki, kapusta zasmażana', []),
        ('Żeberka pieczone', 42.00, 'frytki belgijskie, zielona sałatka, sos BBQ', []),
        ('Penne a\'la carbonara', 42.00, 'makaron pszenny, sos czosnkowo-śmietanowy, wędzonka, parmezan', []),
        ('Naleśniki z serem 2 szt.', 28.00, 'na słodko, konfitura borówkowa', []),
        ('Łosoś (mała porcja)', 30.00, '', [('150g', 0)]),
        ('Filet drobiowy (mała porcja)', 27.00, '', [('150g', 0)]),
        ('Kotlet schabowy (mała porcja)', 27.00, '', [('150g', 0)]),
        ('Pierogi po łemkowsku', 32.00, '', [('10szt', 0)]),
        ('Pierogi ruskie', 28.00, '', [('10szt', 0)]),
        ('Pierogi z mięsem', 29.00, '', [('10szt', 0)]),
        ('Pierogi z borówkami', 28.00, '', [('10szt', 0)]),
    ],
    'Burgery': [
        ('Chicken Burger', 39.00, 'bułka maślana, ser cheddar, karmelizowana cebula, rukola, sos curry, frytki; kurczak w chrupiącej panierce lub wege ser halloumi +2zł (wpisz w notatce)', []),
        ('Tortilla', 38.00, 'sałata lodowa, ogórek, pomidor, czerwona cebula, sos majonezowy chilli, frytki; kurczak w chrupiącej panierce lub wege ser halloumi +1zł (wpisz w notatce)', []),
    ],
    'Sałatki': [
        ('Sałatka grecka', 36.00, 'ser feta, sałata, ogórek, pomidor, cebula, oliwki, papryka, sos vinaigrette, bułka', []),
        ('Sałatka królewska', 41.00, 'kurczak w panierce, sałata, pomidor, ogórek, papryka, cebula, kukurydza, pestki dyni i słonecznika, oliwa z czosnkiem', []),
        ('Sałatka z krewetkami', 43.00, 'sałata lodowa, roszponka, krewetki, pomarańcza, awokado, czerwona cebula, czarny sezam, dressing, grzanka', []),
        ('Sałatka z kurczakiem', 40.00, 'sałata lodowa, kurczak, ogórek, pomidor, cebula, kukurydza, sos vinaigrette, grzanki', []),
        ('Sałatka z halloumi', 40.00, 'grylowany ser halloumi, sałata lodowa, szpinak, rukola, pomidor koktajlowy, ogórek', []),
    ],
    'Dodatki': [
        ('Frytki z batatów z sosami', 23.00, '', []),
        ('Ćwiartki ziemniaków', 16.00, '', [('150g', 0)]),
        ('Frytki', 15.00, '', []),
        ('Frytki z serem', 19.00, '', []),
        ('Ziemniaki', 9.00, '', []),
        ('Placek ziemniaczany', 9.00, '', []),
        ('Zestaw surówek', 16.00, '', []),
        ('Surówka z białej kapusty', 10.00, '', []),
        ('Surówka z marchewki', 10.00, '', []),
        ('Mizeria', 10.00, '', []),
        ('Zasmażana lub młoda kapusta', 13.00, '', []),
        ('Sos Majonezowy', 5.00, '', []),
        ('Sos Curry', 5.00, '', []),
        ('Sos Aioli', 5.00, '', []),
        ('Sos BBQ', 5.00, '', []),
        ('Sos Tatarski', 5.00, '', []),
        ('Sos Sweet-chilli', 5.00, '', []),
        ('Sos Majonez truflowy', 5.00, '', []),
        ('Sos Vinaigrette', 4.00, '', []),
        ('Oliwa czosnkowa', 4.00, '', []),
    ],
}

class Command(BaseCommand):
    help = 'Seed menu Dark Pub'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='Dark Pub')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono Dark Pub w bazie!'))
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