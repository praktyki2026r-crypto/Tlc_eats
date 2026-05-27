from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem, OptionGroup, Option

MENU = {
    'Przystawki': [
        # (name, base_price, ingredients, sizes, addons)
        ('Tatar z polędwicy wołowej', 52.00, 'siekany z poszatkowaną cebulą, grzybami, ogórkiem, anchois, kaparami i żółtkiem', [], []),
        ('Krewetki tygrysie', 49.00, 'czosnek, chilli, natka pietruszki, bułeczki', [], []),
    ],
    'Zupy': [
        ('Rosół', 17.00, 'drobiowo-wołowy z makaronem', [], []),
        ('Barszcz czerwony', 18.00, 'uszka faszerowane mięsem', [], []),
        ('Żurek', 18.00, 'jajko, kiełbasa, pieczywo', [], []),
    ],
    'Dania Główne': [
        ('Stek', 140.00, 'polędwica wołowa, pieczarki, smażona cebula, kukurydza, frytki, sos pieprzowy', [], []),
        ('Łosoś', 51.00, 'puree ziemniaczane, zielone szparagi, pieczone buraki, sos maślany', [], []),
        ('Pierś z kaczki', 46.00, 'sos żurawinowy, gnocchi, zielona sałatka ze słodkim vinaigrette', [], []),
        ('Placek po Węgiersku', 35.00, 'placki ziemniaczane, gulasz wieprzowy, śmietana, ser żółty, zestaw surówek', [('Mały', 0), ('Duży', 9.00)], []),
        ('Kurczak na gorącym półmisku', 50.00, 'marynata orientalna, smażony z cebulą, ryż, surówka z białej kapusty, sos nuoc chan', [], []),
        ('Golonka pieczona na gorącym półmisku', 47.00, 'masło ziołowe, opiekane ziemniaki z tymiankiem, ogórek kiszony, chrzan, musztarda', [], []),
        ('Kotlet schabowy', 40.00, 'ziemniaki, kapusta zasmażana', [], []),
        ('Żeberka pieczone', 42.00, 'frytki belgijskie, zielona sałatka, sos BBQ', [], []),
        ('Chicken Burger / Wege', 39.00, 'bułka maślana, ser cheddar, karmelizowana cebula, rukola, sos curry, frytki', [('Chicken (kurczak w panierce)', 0), ('Wege (ser halloumi)', 2.00)], []),
        ('Tortilla / Wege', 38.00, 'sałata lodowa, ogórek, pomidor, czerwona cebula, sos majonezowy chilli, frytki', [('Kurczak w chrupiącej panierce', 0), ('Wege (ser halloumi)', 1.00)], []),
        ('Naleśniki z serem 2 szt.', 28.00, 'na słodko, konfitura borówkowa', [], []),
        ('Penne a\'la carbonara', 42.00, 'makaron pszenny, sos czosnkowo-śmietanowy, wędzonka, parmezan', [], []),
    ],
    'Małe Porcje': [
        ('Łosoś 150g', 30.00, '', [], []),
        ('Filet drobiowy 150g', 27.00, '', [], []),
        ('Kotlet schabowy 150g', 27.00, '', [], []),
    ],
    'Domowe Pierogi': [
        ('Pierogi po łemkowsku', 32.00, '', [('10szt', 0)], []),
        ('Pierogi ruskie', 28.00, '', [('10szt', 0)], []),
        ('Pierogi z mięsem', 29.00, '', [('10szt', 0)], []),
        ('Pierogi z borówkami', 28.00, '', [('10szt', 0)], []),
    ],
    'Sałatki': [
        ('Sałatka grecka', 36.00, 'ser feta, sałata, ogórek, pomidor, cebula, oliwki, papryka, sos vinaigrette, bułka', [], []),
        ('Sałatka królewska', 41.00, 'kurczak w panierce, sałata, pomidor, ogórek, papryka, cebula, kukurydza, pestki dyni i słonecznika, oliwa z czosnkiem', [], []),
        ('Sałatka z krewetkami', 43.00, 'sałata lodowa, roszponka, krewetki, pomarańcza, awokado, czerwona cebula, czarny sezam, dressing, grzanka', [], []),
        ('Sałatka z kurczakiem', 40.00, 'sałata lodowa, kurczak, ogórek, pomidor, cebula, kukurydza, sos vinaigrette, grzanki', [], []),
        ('Sałatka z halloumi', 40.00, 'grylowany ser halloumi, sałata lodowa, szpinak, rukola, pomidor koktajlowy, ogórek', [], []),
    ],
    'Przekąski': [
        ('Przekąska piwna', 73.00, '', [], []),
        ('Skrzydełka 400g', 36.00, '', [], ['do wyboru: na ostro lub z sosem BBQ']),
        ('Ćwiartki', 25.00, 'ziemniaki z sosami', [], []),
        ('Paluchy drożdżowe', 22.00, 'z sosem', [], []),
        ('Frytki belgijskie', 23.00, 'z sosem', [], []),
    ],
    'Sosy': [
        ('Majonezowy', 5.00, '', [], []),
        ('Curry', 5.00, '', [], []),
        ('Aioli', 5.00, '', [], []),
        ('BBQ', 5.00, '', [], []),
        ('Tatarski', 5.00, '', [], []),
        ('Sweet-chilli', 5.00, '', [], []),
        ('Majonez truflowy', 5.00, '', [], []),
        ('Sos vinaigrette', 4.00, '', [], []),
        ('Oliwa czosnkowa', 4.00, '', [], []),
    ],
    'Dodatki': [
        ('Frytki z batatów z sosami', 23.00, '', [], []),
        ('Ćwiartki ziemniaków 150g', 16.00, '', [], []),
        ('Frytki', 15.00, '', [], []),
        ('Frytki z serem', 19.00, '', [], []),
        ('Ziemniaki', 9.00, '', [], []),
        ('Placek ziemniaczany', 9.00, '', [], []),
        ('Zestaw surówek', 16.00, '', [], []),
        ('Surówka z białej kapusty', 10.00, '', [], []),
        ('Surówka z marchewki', 10.00, '', [], []),
        ('Mizeria', 10.00, '', [], []),
        ('Zasmażana lub młoda kapusta', 13.00, '', [], []),
    ],
}

class Command(BaseCommand):
    help = 'Seed menu Dark Pub'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='darkpub')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono darkpub w bazie!'))
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