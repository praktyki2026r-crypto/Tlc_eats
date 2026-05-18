from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem, OptionGroup, Option

MENU = {
    'Zupy': [
        ('Żurek solo', 10, ''),
        ('Żurek z jajkiem i kiełbasą', 18, ''),
        ('Barszcz solo', 10, ''),
        ('Barszcz z uszkami', 18, ''),
        ('Pomidorowa z makaronem lub ryżem', 12, ''),
    ],
    'Drób': [
        ('Filet z kurczaka w panierce/sotte', 20, ''),
        ('Filet w cieście naleśnikowym', 22, ''),
        ('Filet w płatkach kukurydzianych', 22, ''),
        ('Kotlet de volaille z serem', 22, ''),
        ('Roladka z kurczaka', 24, 'ogórek konserwowy, papryka, ser żółty'),
        ('Filet drobiowy sotte w jarzynach', 26, ''),
        ('Polędwiczki drobiowe (4 sztuki)', 22, ''),
        ('Nuggetsy (4 sztuki)', 24, ''),
    ],
    'Ryby': [
        ('Filet z miruny w panierce', 25, ''),
        ('Ryba (miruna) w jarzynach', 29, ''),
        ('Dorsz', 32, ''),
    ],
    'Wieprzowina': [
        ('Kotlet schabowy w panierce', 20, ''),
        ('Kotlet schabowy pod chmurką', 24, 'pieczarki, ser żółty'),
        ('Bitki schabowe z sosem pieczarkowym', 24, ''),
        ('Karkówka z cebulką', 24, ''),
        ('Gulasz wieprzowy', 20, ''),
        ('Sznycel mielony', 20, ''),
        ('Kotlet schabowy po kapitańsku', 28, 'boczek, jajko sadzone'),
        ('Koperta schabowa', 24, ''),
    ],
    'Surówki': [
        ('Surówka dnia', 8, ''),
        ('Zestaw 3 surówek', 15, ''),
        ('Mizeria', 8, ''),
        ('Buraczki czerwone', 8, ''),
        ('Ogórek konserwowy', 8, ''),
        ('Kapusta zasmażana', 12, ''),
        ('Surówka z marchewki i jabłkiem', 8, ''),
    ],
    'Sałatki': [
        ('Sałatka Cezar', 32, 'sałata lodowa, kurczak, pomidor, ogórek, grzanki, sos musztardowy'),
        ('Sałatka Grecka', 32, 'sałata, boczek, pomidor, ogórek, oliwki, ser feta, cebula czerwona, sos winegret'),
        ('Sałatka z tuńczykiem', 32, 'sałata, tuńczyk, kukurydza, cebula czerwona, pomidor, ogórek, sos majonezowo-śmietanowy'),
    ],
    'Fast Food': [
        ('Frytki', 10, ''),
        ('Frytki z serem', 15, ''),
        ('Ćwiartki z ziemniaków', 12, ''),
        ('Chiken Burger', 30, ''),
    ],
    'Deser': [
        ('Szarlotka na ciepło', 14, ''),
    ],
    'Dania barowe': [
        ('Fasolka po bretońsku', 22, ''),
        ('Bigos', 22, ''),
        ('Wątróbka z cebulką', 18, ''),
        ('Pierogi domowe (12szt)', 22, ''),
        ('Pierogi z kapustą (12szt.)', 22, ''),
        ('Pierogi z mięsem (12szt.)', 22, ''),
        ('Krokiet z mięsem', 15, ''),
        ('Krokiet z kapustą', 15, ''),
        ('Placki ziemniaczane (3szt.)', 18, ''),
        ('Naleśniki z serem (2szt.)', 18, ''),
        ('Naleśniki z dżemem (2szt.)', 18, ''),
        ('Placek po Węgiersku (mały)', 30, ''),
        ('Placek po Węgiersku (duży)', 36, ''),
        ('Kebab na talerzu z frytkami i surówką', 30, ''),
    ],
    'Każdego dnia coś innego': [
        ('Zestaw dnia (zupa + II danie)', 29, ''),
        ('II danie', 26, ''),
        ('Zupa dnia', 9, ''),
    ],
    'Śniadania': [
        ('Jajecznica z 4 jajek na boczku/maśle', 16, 'ogórek, pomidor, pieczywo'),
        ('Kiełbasa na gorąco', 16, 'ogórek, pomidor, musztarda, ketchup, pieczywo'),
        ('Omlet z 4 jajek ze szczypiorkiem', 16, 'pomidor, ogórek, pieczywo'),
    ],
    'Napoje gorące': [
        ('Kawa Espresso', 7, ''),
        ('Kawa z ekspresu mała', 7, ''),
        ('Kawa z ekspresu duża', 10, ''),
        ('Kawa Latte', 12, ''),
        ('Kawa parzona', 7, ''),
        ('Kawa rozpuszczalna', 8, ''),
        ('Cappuccino', 11, ''),
        ('Herbata czarna', 5, ''),
        ('Herbata owocowa', 5, ''),
    ],
}

class Command(BaseCommand):
    help = 'Seed menu Lucy Bar'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='Lucy bar')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono Lucy bar w bazie!'))
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