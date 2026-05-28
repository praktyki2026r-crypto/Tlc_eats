from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem, OptionGroup, Option

MENU = {
    'Pizza': [
        ('Del Piero', 25.00, 'sos, mozzarella, pieczarki, szynka, kurczak, kukurydza, papryka kolorowa', [('23cm', 0), ('30cm', 7.00), ('40cm', 22.00)]),
        ('Margherita', 20.00, 'sos, mozzarella', [('23cm', 0), ('30cm', 8.00), ('40cm', 20.00)]),
        ('Capriciosa', 22.00, 'sos, mozzarella, pieczarki, szynka', [('23cm', 0), ('30cm', 8.00), ('40cm', 21.00)]),
        ('Caraib', 25.00, 'sos, mozzarella, szynka, salami, kukurydza, ananas, papryka kolorowa', [('23cm', 0), ('30cm', 7.00), ('40cm', 22.00)]),
        ('Wiejska', 25.00, 'sos, mozzarella, pieczarki, cebula, szynka, jajko, kiełbasa wiejska', [('23cm', 0), ('30cm', 7.00), ('40cm', 22.00)]),
        ('Marynarska', 28.00, 'sos, mozzarella, cebula, tuńczyk, kapary, oliwki', [('23cm', 0), ('30cm', 9.00), ('40cm', 27.00)]),
        ('Anchois', 28.00, 'sos, mozzarella, cebula, anchois, kapary, oliwki', [('23cm', 0), ('30cm', 9.00), ('40cm', 27.00)]),
        ('Włoska', 26.00, 'sos, mozzarella, szynka szwarcwaldzka, rukola, pomidory, pesto, biała mozzarella', [('23cm', 0), ('30cm', 7.00), ('40cm', 23.00)]),
        ('Norweska', 28.00, 'sos, mozzarella, krewetki, oliwki, cebula, masło czosnkowe', [('23cm', 0), ('30cm', 9.00), ('40cm', 27.00)]),
        ('Powiew Lata', 23.00, 'sos, mozzarella, pomidory, bazylia, czosnek, pesto', [('23cm', 0), ('30cm', 8.00), ('40cm', 21.00)]),
        ('Crunchy Becon', 25.00, 'sos, mozzarella, mięso mielone, cebula, boczek, chili, pomidory', [('23cm', 0), ('30cm', 7.00), ('40cm', 22.00)]),
        ('Idealna Kompozycja', 26.00, 'sos, mozzarella, 2 wybrane składniki mięsne, 2 wybrane składniki warzywne; wybór składników (wpisać w notatce)', [('23cm', 0), ('30cm', 8.00), ('40cm', 23.00)]),
        ('Peperoni', 25.00, 'sos, mozzarella, czosnek, kiełbasa peperoni, pomidory', [('23cm', 0), ('30cm', 7.00), ('40cm', 22.00)]),
        ('Skarby Jesieni', 26.00, 'sos, mozzarella, gruszka, gorgonzola, orzechy włoskie, pesto', [('23cm', 0), ('30cm', 8.00), ('40cm', 23.00)]),
        ('Diablo', 25.00, 'sos, mozzarella, mięso mielone, chili, fasolka szparagowa, cebula', [('23cm', 0), ('30cm', 7.00), ('40cm', 22.00)]),
        ('Wegetariańska', 24.00, 'sos, mozzarella, pieczarki, groszek, kukurydza, pomidory', [('23cm', 0), ('30cm', 7.00), ('40cm', 22.00)]),
        ('Królewska', 26.00, 'sos śmietanowy, mozzarella, boczek, szynka, pomidory, cheddar', [('23cm', 0), ('30cm', 8.00), ('40cm', 23.00)]),
        ('Cztery Sery', 27.00, 'sos, mozzarella, camembert, ser kozi, biała mozzarella, cheddar, orzechy włoskie, miód', [('23cm', 0), ('30cm', 9.00), ('40cm', 25.00)]),
        ('Jalapeno', 25.00, 'sos, mozzarella, cebula, kiełbasa peperoni, jalapeno', [('23cm', 0), ('30cm', 7.00), ('40cm', 22.00)]),
        ('Szkolna', 47.00, 'sos, mozzarella, ćwiartka margherita, ćwiartka pieczarki, ćwiartka szynka, ćwiartka salami', [('40cm', 0)]),
        ('Familijna', 61.00, 'sos, mozzarella, 1 wybrany składnik mięsny, 3 wybrane składniki warzywne; wybór składników (wpisać w notatce)', [('50cm', 0)]),
        ('Zawał Włocha', 35.00, 'sos, mozzarella, cebula, pieczarki, mięso gyros, frytki', []),
        ('Calzone', 36.00, 'sos, mozzarella, pieczarki, cebula, szynka, jajko', []),
    ],
    'Makarony': [
        ('Spaghetti carbonara', 29.00, 'jajka, grana padano, boczek', []),
        ('Spaghetti zielone pesto', 29.00, 'zielone pesto, chips z bekonu', []),
        ('Tagliatelle gorgonzola', 29.00, 'gorgonzola, gruszka, orzechy', []),
    ],
    'Przekąski': [
        ('Bruschetta', 17.00, '3 grzanki z salsą z pomidorów, czosnku, bazylii i oliwy', []),
        ('Crudo', 26.00, 'prosciutto crudo, włoski twaróg, pesto, rukola, pomidory koktajlowe', []),
        ('Salame', 26.00, 'salami, włoski twaróg, pomidory koktajlowe, rukola', []),
        ('Polacco', 26.00, 'kurczak, włoski twaróg, czerwona cebula, rukola, sos BBQ', []),
        ('Vege', 26.00, 'biała mozzarella, włoski twaróg, pomidory koktajlowe, balsamico, rukola', []),
    ],
    'Zupy': [
        ('Rosół z makaronem', 15.00, '', []),
        ('Pomidorowa', 15.00, '', []),
        ('Barszcz z uszkami', 19.00, '', []),
        ('Barszcz z krokietem', 17.00, '', []),
        ('Żurek', 17.00, 'jajko, kiełbasa', []),
        ('Flaczki', 17.00, '', []),
    ],
    'Dania główne': [
        ('Placek po zbójnicku', 35.00, '3 placki ziemniaczane, gulasz wieprzowy, śmietana, ser, zestaw surówek', []),
        ('Pierogi ruskie', 21.00, 'omasta', []),
        ('Pierogi z mięsem', 25.00, 'omasta', []),
        ('Schabowy', 35.00, 'kotlet schabowy, ziemniaki, kapusta zasmażana', []),
        ('Polędwiczka wieprzowa', 36.00, 'kluski śląskie, sos grzybowy, bukiet warzyw', []),
        ('Pierś z kurczaka', 33.00, 'filet drobiowy w chrupiącej panierce, ziemniaki, surówka z marchewki', []),
        ('Grand burger', 29.00, '4x strips, bekon, ser, sałata lodowa, ogórek, pomidor, sos BBQ, frytki', []),
        ('Kubełek strips', 46.00, '15 kawałków fileta z kurczaka, frytki, sosy', []),
        ('Kubełek hot-wings', 37.00, '15 skrzydełek w ostrej panierce, frytki, sosy', []),
        ('Kubełek mix', 41.00, '10 skrzydełek w ostrej panierce, 5 kawałków fileta z kurczaka, frytki, sosy', []),
        ('Ser panierowany', 27.00, '3 kawałki sera, kulki ziemniaczane, bukiet warzyw, żurawina', []),
        ('Gyros', 28.00, 'gyros z kurczaka, frytki, surówka; sos do wyboru: czosnkowy lub vinegrette (wpisać w notatce)', []),
        ('Zestaw strips', 22.00, '3 panierowane fileciki z kurczaka, frytki', []),
        ('Naleśniki', 27.00, 'dodatek do wyboru: ser, bita śmietana, polewa czekoladowa (wpisać w notatce)', []),
        ('Szarlotka', 19.00, 'na ciepło, lody, bita śmietana', []),
        ('Lody', 19.00, 'owoce, bita śmietana', []),
        ('Pancakes', 29.00, 'nutella, lody, orzeszki ziemne, słodycze', []),
        ('Filet rybny', 33.00, 'miruna panierowana, frytki, surówka z białej kapusty', []),
    ],
    'Sałatki': [
        ('Vitalite', 29.00, 'szpinak, kurczak, słonecznik, pieczarki, oliwa z oliwek, czosnek, cebula, grzanki', []),
        ('Sałatka z kurczakiem', 29.00, 'pekińska, papryka, pomidor, ogórek, kurczak, kukurydza, grzanki', []),
        ('Grecka', 29.00, 'sałata lodowa, pomidor, ogórek, oliwki, ser feta, oliwa z oliwek', []),
        ('Egzotyczna', 29.00, 'mix sałat, kurczak w chrupiącej panierce, pomidorki koktajlowe, owoce sezonowe, płatki migdałów, sos pikantny mango', []),
    ],
    'Dodatki': [
        ('Frytki', 9.00, '', []),
        ('Frytki z serem', 12.00, '', []),
        ('Ćwiartki ziemniaczane', 13.00, '', []),
        ('Kulki ziemniaczane', 10.00, '', []),
        ('Ziemniaki gotowane', 8.00, '', []),
        ('Placki ziemniaczane', 15.00, '', []),
        ('Zestaw surówek', 13.00, '', []),
        ('Warzywa gotowane', 11.00, '', []),
    ],
    'Napoje': [
        ('Espresso', 9.00, '', []),
        ('Espresso macchiato', 12.00, '', []),
        ('Americano', 11.00, '', []),
        ('Cappuccino', 12.00, '', []),
        ('Flat white', 12.00, '', []),
        ('Caffe latte macchiato', 14.00, '', []),
        ('Affogato', 16.00, 'espresso z lodami waniliowymi i syropem orzech laskowy', []),
        ('Kawa mrożona', 19.00, 'lody, syrop smakowy', []),
        ('Herbata', 9.00, 'wybór rodzaju (wpisać w notatce)', []),
        ('Herbata zimowa', 23.00, '', []),
        ('Coca-cola', 7.00, '', [('0,25l', 0), ('0,5l', 3.00)]),
        ('Coca-cola zero', 7.00, '', [('0,25l', 0), ('0,5l', 3.00)]),
        ('Fanta', 7.00, '', [('0,25l', 0), ('0,5l', 3.00)]),
        ('Sprite', 7.00, '', [('0,25l', 0), ('0,5l', 3.00)]),
        ('Tonic Kinley', 7.00, '', []),
        ('Kropla Beskidu', 8.00, 'gazowana lub niegazowana (wpisać w notatce)', []),
        ('Fuzetea', 10.00, 'wybór smaku (wpisać w notatce)', []),
        ('Cappy', 8.00, 'wybór smaku (wpisać w notatce)', [('0,33l', 0)]),
        ('Monster', 13.00, '', []),
        ('Lemoniada', 13.00, 'wybór smaku (wpisać w notatce)', [('0,35l', 0)]),
        ('Dzban soku', 24.00, 'wybór smaku (wpisać w notatce)', [('1l', 0)]),
        ('Shake Oreo', 27.00, '', []),
        ('Shake Banan - Wanilia', 27.00, '', []),
        ('Shake Masło Orzechowe', 27.00, '', []),
        ('Dzban wody', 17.00, 'gazowana lub niegazowana (wpisać w notatce)', [('1l', 0)]),
    ],
}

class Command(BaseCommand):
    help = 'Seed menu Del Piero Pizza Caffe'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='Del Piero')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono Del Piero w bazie!'))
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