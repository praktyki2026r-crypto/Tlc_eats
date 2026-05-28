from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem, OptionGroup, Option

MENU = {
    'Zupy': [
        ('Tradycyjny rosół', 19, 'z makaronem', [], []),
        ('Azja Udon', 23, 'azjatycka zupa z makaronem udon z karmazynem, zielona cebulka, jajko, sos rybny, sos sojowy, czosnek, imbir, chilli, azjatyckie grzyby', [], []),
        ('Francuska zupa Vichyssoise', 23, 'z pora i ziemniaka z nutką śmietany serwowana na zimno', [], []),
    ],
    'Przekąski': [
        ('Terrine', 30, 'zimna przystawka z pora serwowana z kremowym sosem na bazie śmietany i sera koziego', [], []),
        ('Mule', 42, 'serwowane w maślanym sosie na bazie masła i białego wina z czosnkiem, cebulą i natką pietruszki podane z domowym pieczywem prosto z pieca', [], []),
        ('Tatar', 52, 'polędwica wołowa, czerwona cebula, anchois, musztarda, rydze, żółtko serwowany z pieczywem prosto z pieca', [], []),
        ('Oscypek', 31, 'zawinięty w boczek podawany z konfiturą z żurawiny i mixem sałat', [], []),
        ('Koszyk Mix', 45, 'nuggetsy, krążki cebulowe, frytki z batatów, pieczarki faszerowane cheddarem serwowane z sosem czosnkowym', [], []),
        ('Frytki taco', 35, 'frytki z mięsem mielonym w meksykańskich przyprawach podane z paprykowym sosie i serem cheddar', [], []),
        ('Nuggetsy z kurczaka', 30, '10 szt. z sosem czosnkowym', [], []),
        ('Krążki cebulowe', 18, 'z sosem czosnkowym', [], []),
        ('Frytki z ketchupem', 18, '', [], []),
        ('Frytki z serem', 21, '', [], []),
        ('Frytki z batatów', 26, '', [], []),
        ('Wrap Ceasare cajun', 42, 'kurczak w przyprawie cajun, sałata, pomidor, boczek, parmezan, sos ceasare', [], []),
        ('Wrap Serowy kurczak', 42, 'panierowany kurczak, sałata, pomidor, ser cheddar, sos czosnkowy', [], []),
        ('Wrap Alla burito', 42, 'mięso mielone w meksykańskich przyprawach, sałata, pomidor, kolendra, fasola pinto, jalapeno, czerwona papryka, ser cheddar i kwaśna śmietana', [], []),
    ],
    'Sałatki': [
        ('Sałatka z Buratta', 33, 'włoska buratta, bazylia, pomidor, pesto, oliwa z oliwek i sos balsamiczny', [], []),
        ('Sałatka z wołowiną', 53, 'polędwica wołowa, mix sałat, ogórek, pomidorki koktailowe, papryka, czerwona cebula, pestki sezamu, marchewka, chilli, sos musztardowo miodowy', [], []),
        ('Domowa sałatka cezar', 42, 'sałata lodowa, kurczak, boczek, grzanki, pomidory, sos cesarski i parmezanem', [], []),
        ('Sałatka Grecka', 36, 'mix sałat, ogórek, pomidorki koktailowe, papryka, czerwona cebula, oliwki, ser feta podany z domowym sosem winegrette', [], []),
        ('Sałatka z Kurczakiem i krewetkami', 49, 'mix sałat, pomidorki koktajlowe, kurczak i krewetki w przyprawie cajun, jabłko, orzechy włoskie, ogórek, sos marie rose', [], []),
    ],
    'Makarony': [
        ('Pappardelle gamberetto', 50, 'krewetki, pomidorki koktajlowe, cukinia, czosnek, świeże chilli serwowane z sosem na bazie białego wina, masła, oliwy z oliwek, natka pietruszki i parmezan', [], []),
        ('Linguine alla carbonara', 48, 'kurczak, cebula, czosnek, pieczarki, boczek w kremowym sosie na bazie śmietany z parmezanem', [], []),
        ('Linguine aglio e olio', 42, 'oliwa z oliwek, czosnek, świeże chilli, natka pietruszki i parmezan', [], []),
        ('Rigatoni al forno', 50, 'polędwiczka wieprzowa, szpinak, mascarpone, sos pomidorowy, czosnek, cebula, nduja zapiekane z parmezanem, serwowane w gorącym półmisku prosto z pieca', [], []),
    ],
    'Dania główne': [
        ('Tradycyjne FISH AND CHIPS', 43, 'morszczuk (180g) serwowany w cieście piwnym z frytkami, sosem tatarskim oraz sałatką colesław', [], []),
        ('Ryba Karmazyn', 48, 'z patelni serwowany z salsą z mango i mięty podawany z ryżem jaśminowym z kurkumą', [], []),
        ('Stek z kałamarnicy', 48, 'podawany w sosie na bazie białego wina, masła, soku z cytryny, czosnku i świeżej natki pietruszki serwowany z mixem z rukoli i sezonowych warzyw', [], []),
        ('Nachos', 48, 'chrupiące nachos z wołowiną w meksykańskich przyprawach z jalapeno, czosnkiem, guacamole, salsa z pomidorków czosnku i cebuli z kolendrą', [], []),
        ('Stek z zielonym pieprzem', 150, 'polędwica wołowa (200g+) serwowany z sosem z zielonego pieprzu z nutką śmietany', [], []),
        ('Stek z masłem czosnkowym', 150, 'z zielonego pieprzu z nutką śmietany', [], []),
        ('Polędwica wieprzowa', 51, 'w kremowym sosie na bazie demi glassu z pieczarkami i nutką śmietany, opiekane ziemniaki z rozmarynem i grillowana cukinia z papryką', [], []),
        ('Udon', 53, 'azjatycki makaron udon z polędwiczką wieprzową w orientalnym sosie ostrygowym z cebulą, imbirem, czosnkiem i marchewką, papryką, zieloną cebulką i prażonymi pestki sezamu', [], []),
        ('Saltimbocca', 49, 'plastry polędwicy wieprzowej z szynką parmeńską i szałwią w sosie z zielonego pieprzu i nutką śmietany na bazie demi glasu serwowana z opiekanymi ziemniakami z rozmarynem i mixem sałat', [], []),
        ('Żeberka wieprzowe', 48, 'serwowane z frytkami i sałatką colesław', [], []),
    ],
    'Pizza': [
        ('Maryśka', 32, 'sos pomidorowy, mozzarella, oliwa z oliwek, oregano', [('30 cm', 0)], []),
        ('Biała Kula', 41, 'sos pomidorowy, mozzarella, burrata, świeże pomidory, pesto bazyliowe, oregano', [('30 cm', 0)], []),
        ('Skurczybyk', 42, 'sos pomidorowy, mozzarella, nduja, mascarpone, czerwona cebula, spianata piccante, oregano', [('30 cm', 0)], []),
        ('Crunchy chicken', 39, 'sos pomidorowy, mozzarella, czerwona cebula, panierowane kawałki kurczaka, świeże pomidorki, oregano', [('30 cm', 0)], []),
        ('Fiflok', 38, 'sos pomidorowy, mozzarella, salami pepperoni, czerwona cebula, oliwki, oregano', [('30 cm', 0)], []),
        ('Americana', 36, 'sos pomidorowy, mozzarella, salami pepperoni, oregano', [('30 cm', 0)], []),
        ('Śniegowy kurczok', 38, 'mozzarella, boczek, kurczak, pieczarki, cebula, parmezan, oregano', [('30 cm', 0)], []),
        ('Diavola', 38, 'sos pomidorowy, mozzarella, spianata piccante, oregano', [('30 cm', 0)], []),
        ('Szyneczka', 34, 'sos pomidorowy, mozzarella, szynka, oregano', [('30 cm', 0)], []),
        ('Grzybowa szynka', 37, 'sos pomidorowy, mozzarella, szynka, pieczarki, oregano', [('30 cm', 0)], []),
        ('Parma', 44, 'sos pomidorowy, mozzarella, szynka parmeńska, rucola, oliwa z oliwek, parmezan, oregano', [('30 cm', 0)], []),
        ('Wydydany dyd', 42, 'sos BBQ, mozzarella, wołowina z pieca, cebula, kurczak, boczek, oregano', [('30 cm', 0)], []),
        ('Quatro formaggi', 40, 'mozzarella, gorgonzola, parmezan, camambert, oregano', [('30 cm', 0)], []),
        ('Dunder świśnie', 41, 'sos pomidorowy, mozzarella, kurczak, boczek, pieczona papryka, płatki chilli, oregano', [('30 cm', 0)], []),
        ('Szybki lopez', 40, 'sos pomidorowy, mozzarella, wołowina z pieca, karmelizowana cebula, parmezan, oregano', [('30 cm', 0)], []),
        ('Kulawy Joe', 40, 'sos pomidorowy, mozzarella, salami pepperoni, cebula, kukurydza, pieczona papryka, oregano', [('30 cm', 0)], []),
        ('Diobeł tasmański', 44, 'sos pomidorowy, mozzarella, salami pepperoni, wołowina z pieca, pieczona papryka, jalapeno, płatki chilli, rucola, oregano', [('30 cm', 0)], []),
        ('Suszony pomidor', 41, 'sos pomidorowy, mozzarella, boczek, suszone pomidory, rucola, sos cesarski, oregano', [('30 cm', 0)], []),
        ('Capriciosa', 39, 'sos pomidorowy, mozzarella, szynka, pieczarki, oliwki, oregano', [('30 cm', 0)], []),
        ('Krejzi wege', 37, 'sos pomidorowy, mozzarella, pieczarki, cebula, pieczona papryka, kukurydza, oregano', [('30 cm', 0)], []),
        ('Łoscypek', 41, 'sos żurawinowy, mozzarella, oscypek, boczek, kurczak, oregano', [('30 cm', 0)], []),
        ('Kreweta', 49, 'sos pomidorowy, mozzarella, krewetki, czosnek, oliwa z oliwek, chilli, pomidory koktajlowe, świeża bazylia, oregano', [('30 cm', 0)], []),
    ],
    'Dodatki': [
        ('Sos czosnkowy / ketchup', 3, '', [], []),
        ('Mięso / wędliny', 8, '', [], []),
        ('Warzywa', 4, '', [], []),
        ('Sery', 8, '', [], []),
        ('Krewetki', 26, '', [], []),
        ('Opakowanie na wynos', 2, '', [], []),
        ('Mix sałat z winegretem', 14, '', [], []),
        ('Opiekane ziemniaki z rozmarynem', 12, '', [], []),
        ('Pieczywo', 7, '', [], []),
        ('Colesław', 8, '', [], []),
    ],
    'Burgery': [
        ('Burger z podwójnym mięsem', 52, 'do wyboru z listy poniżej', [], []),
        ('Burger nowy', 41, 'mięso, sałata, pomidor, ser cheddar, pikle, boczek, czerwona cebula', [('180g', 0)], []),
        ('Smash burger', 42, '2 plastry wołowiny, sałata, cebula, cheddar, pikle', [], []),
        ('Burger drwala', 42, 'mięso, sałata, camembert w panierce', [('180g', 0)], []),
        ('Baca burger', 42, 'mięso, sałata, oscypek, boczek, karmelizowana cebula', [('180g', 0)], []),
        ('Blue bacon burger', 42, 'mięso, sałata, pomidor, boczek, ser pleśniowy', [('180g', 0)], []),
        ('Cheese burger', 42, 'mięso, sałata, pomidor, pikle, ser cheddar', [('180g', 0)], []),
        ('Chilli burger', 42, 'mięso, sałata, pomidor, smażona cebula, jalapeno', [('180g', 0)], []),
        ('Boczek burger', 42, 'mięso, sałata, pomidor, boczek, jajko', [('180g', 0)], []),
        ('Klasyczny burger', 40, 'mięso, sałata, pomidor', [('180g', 0)], []),
        ('Nachos burger', 40, 'filet z kurczaka z panierce z nachosów, sałata, pomidor i guacamole', [], []),
        ('Wege burger', 39, 'sałata, ser cammebert, pomidor, czerwona cebula, guacamole', [], []),
    ],
    'Desery': [
        ('Czekoladowy fondant', 30, 'ciasto czekoladowe serwowane na ciepło z lodami waniliowymi i bitą śmietaną', [], []),
        ('Truskawkowe tiramisu', 32, 'inna odmiana włoskiego deseru, w naszym wydaniu z truskawkami', [], []),
    ],
}


class Command(BaseCommand):
    help = 'Seed menu Połka i Allan'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='Połka i Allan')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono Połka i Allan w bazie!'))
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
