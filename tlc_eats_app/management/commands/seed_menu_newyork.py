from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem, OptionGroup, Option

MENU = {
    'Śniadania': [
        ('Jajecznica', 12.00, 'jajecznica z 3 jajek na boczku lub maśle, ogórek, pomidor, pieczywo, masło', [], []),
        ('Kiełbasa na gorąco', 12.00, 'kiełbasa na gorąco, pieczywo, masło, musztarda, ketchup', [], []),
        ('Kiełbasa smażona', 12.00, 'kiełbasa smażona z cebulą, pieczywo, masło, ketchup, musztarda', [], []),
        ('Parówki drobiowe', 10.00, 'parówki drobiowe 2 szt., ogórek, pomidor, pieczywo, masło', [], []),
        ('Jajka sadzone', 11.00, 'jajko sadzone 2 szt., ogórek, pomidor, pieczywo, masło', [], []),
    ],
    'Zupy': [
        ('Żurek solo', 8.00, '', [], []),
        ('Żurek z jajkiem i kiełbasą', 12.00, '', [], []),
        ('Barszcz solo', 8.00, '', [], []),
        ('Barszcz z uszkami', 12.00, '', [], []),
        ('Barszcz + krokiet z mięsem', 16.00, '', [], []),
        ('Barszcz + krokiet z kapustą', 16.00, '', [], []),
        ('Rosół z makaronem', 9.00, '', [], []),
        ('Pomidorowa z makaronem lub ryżem', 9.00, '', [], []),
        ('Zupa dnia', 8.00, '', [], []),
    ],
    'Dania główne': [
        ('Flaczki z pieczywem', 18.00, '', [], []),
        ('Bigos z pieczywem', 18.00, '', [], []),
        ('Fasolka po bretońsku', 20.00, '', [], []),
        ('Stroganow', 18.00, '', [], []),
        ('Wątróbka z cebulką', 16.00, '', [], []),
        ('Wątróbka panierowana', 16.00, '', [], []),
        ('Kiełbasa z cebulką', 10.00, '', [], []),
        ('Gołąbki z sosem pomidorowym', 18.00, '', [('2 szt.', 0)], []),
        ('Pierogi ukraińskie z omastą', 18.00, 'twaróg, ziemniaki', [('10 szt.', 0)], []),
        ('Pierogi ukraińskie z pieczarkami', 18.00, 'twaróg, ziemniaki, pieczarki', [('10 szt.', 0)], []),
        ('Pierogi z mięsem', 18.00, '', [('10 szt.', 0)], []),
        ('Pierogi z kapustą', 18.00, '', [('10 szt.', 0)], []),
        ('Krokiet z mięsem', 12.00, '', [('1 szt.', 0)], []),
        ('Krokiet z kapustą', 12.00, '', [('1 szt.', 0)], []),
        ('Spaghetti bolognese', 20.00, '', [], []),
        ('Placki ziemniaczane ze śmietaną', 20.00, '', [('3 szt.', 0)], []),
        ('Kotlet z kurczaka panierowany', 24.00, 'do wyboru: ziemniaki, frytki lub ryż, surówka', [], []),
        ('Kotlet z kurczaka zapiekany z serem', 25.00, 'do wyboru: ziemniaki, frytki lub ryż, surówka', [], []),
        ('Kotlet z kurczaka po beskidzku', 27.00, 'do wyboru: ziemniaki, frytki lub ryż, surówka', [], []),
        ('Filet z kurczaka duszony w jarzynach', 26.00, 'do wyboru: ziemniaki, frytki lub ryż', [], []),
        ('Filet z kurczaka po parysku', 24.00, 'w cieście naleśnikowym, do wyboru: ziemniaki, frytki lub ryż, surówka', [], []),
        ('Stek z karkówką i cebulką', 25.00, 'do wyboru: ziemniaki, frytki lub ryż, surówka', [], []),
        ('Kotlet De\'volaille', 28.00, 'do wyboru: ziemniaki, frytki lub ryż, surówka', [], []),
        ('Kotlet schabowy', 26.00, 'do wyboru: ziemniaki, frytki lub ryż, surówka', [], []),
        ('Kotlet schabowy po góralsku', 28.00, 'do wyboru: ziemniaki, frytki lub ryż, surówka', [], []),
        ('Gulasz', 22.00, 'do wyboru: ziemniaki, frytki lub ryż, surówka', [], []),
        ('Klopsiki w sosie pomidorowym', 22.00, 'do wyboru: ziemniaki, frytki lub ryż, surówka', [], []),
        ('Wątróbka panierowana zestaw', 20.00, 'do wyboru: ziemniaki, frytki lub ryż, surówka', [], []),
        ('Wątróbka z cebulą zestaw', 22.00, 'do wyboru: ziemniaki, frytki lub ryż, surówka', [], []),
        ('Placek po węgiersku', 24.00, 'zestaw surówek', [('Mały', 0), ('Duży', 4.00)], []),
        ('Sznycel mielony', 22.00, 'do wyboru: ziemniaki, frytki lub ryż, surówka', [], []),
        ('Sznycel mielony po wiedeńsku', 25.00, 'jajko sadzone, do wyboru: ziemniaki, frytki lub ryż, surówka', [], []),
        ('Kluski śląskie z gulaszem', 26.00, 'zestaw surówek', [], []),
        ('Kotleciki szarpane z kurczaka', 26.00, 'siekany filet drobiowy, czerwona papryka, pieczarki, żółty ser, cebulka, zestaw surówek', [], []),
        ('Bitki schabowe', 24.00, 'do wyboru: ziemniaki, frytki lub ryż, surówka', [], []),
        ('Polędwiczki drobiowe panierowane', 24.00, 'do wyboru: ziemniaki, frytki lub ryż, surówka', [], []),
        ('Kebab w zestawie z frytkami i surówką', 22.00, 'frytki, surówka', [], []),
    ],
    'Dania rybne': [
        ('Filet z mintaja panierowany', 26.00, 'do wyboru: ziemniaki, frytki lub ryż, surówka', [], []),
        ('Filet z mintaja duszony w jarzynach', 26.00, 'do wyboru: ziemniaki, frytki lub ryż', [], []),
    ],
    'Sałatki': [
        ("Caesar's Salad", 22.00, 'sałata lodowa, pieczona polędwiczka z kurczaka, pomidor, ogórek, grzanki, sos musztardowy', [], []),
        ('Sałatka grecka', 22.00, 'sałata lodowa, pomidor, ogórek, oliwki, ser feta, oliwa, papryka', [], []),
        ('Sałatka z tuńczykiem', 24.00, 'sałata lodowa, tuńczyk, jajko, pomidor, ogórek, sos majonezowo-śmietanowy', [], []),
    ],
    'Desery': [
        ('Naleśniki z serem', 16.00, '', [('2 szt.', 0)], []),
        ('Naleśniki z dżemem', 13.00, '', [('2 szt.', 0)], []),
        ('Szarlotka', 13.00, '', [], []),
    ],
    'Dodatki do dań': [
        ('Trzy smaki (zestaw 3 surówek)', 10.00, '', [], []),
        ('Jajko sadzone', 3.00, '', [('1 szt.', 0)], []),
        ('Frytki', 8.00, '', [], []),
        ('Frytki zapiekane z żółtym serem', 12.00, '', [], []),
        ('Ryż / ziemniaki puree', 5.00, '', [], []),
        ('Pieczywo', 2.00, '', [], []),
        ('Ketchup, majonez, musztarda, chrzan', 2.00, '', [], []),
    ],
    'Napoje': [
        ('Kawa Ristretto', 7.00, '', [], []),
        ('Kawa espresso', 7.00, '', [('pojedyncza', 0), ('podwójna', 3.00)], []),
        ('Kawa z ekspresu', 7.00, '', [('mała', 0), ('duża', 4.00)], []),
        ('Kawa parzona', 6.00, '', [], []),
        ('Kawa rozpuszczalna', 7.00, '', [], []),
        ('Cappuccino', 11.00, '', [], []),
        ('Kawa Latte', 12.00, '', [], []),
        ('Herbata Dilmah', 5.00, '', [], []),
        ('Herbata Dilmah owocowa', 5.00, '', [], ['różne smaki (wpisać w notatce)']),
        ('Śmietanka do kawy lub mleko', 1.00, '', [], []),
        ('Cytryna', 1.00, '', [], []),
        ('Sok malinowy', 2.00, '', [], []),
        ('Coca-cola', 5.00, '', [('0,25l szkło', 0), ('0,33l puszka', 0)], []),
        ('Sprite', 6.00, '', [('0,25l szkło', 0), ('0,33l puszka', 0)], []),
        ('Fanta', 6.00, '', [('0,25l', 0)], []),
        ('Woda mineralna Wysowianka', 4.00, '', [('0,3l', 0)], []),
        ('Soki owocowe', 6.00, '', [('0,25l', 0)], []),
        ('Energy drink', 6.00, '', [('0,25l', 0)], []),
        ('Napoje smakowe Wysowianka', 5.00, '', [('0,3l', 0)], []),
    ],
}


class Command(BaseCommand):
    help = 'Seed menu New York'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='New York')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono New York w bazie!'))
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