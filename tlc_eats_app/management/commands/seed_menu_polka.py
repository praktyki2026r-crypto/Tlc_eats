from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem

MENU = {
    'Zupy': [
        ('Tradycyjny rosół', 19, 'z makaronem'),
        ('Azja Udon', 23, 'azjatycka zupa z makaronem udon z karmazynem, zielona cebulka, jajko, sos rybny, sos sojowy, czosnek, imbir, chilli, azjatyckie grzyby'),
        ('Francuska zupa Vichyssoise', 23, 'z pora i ziemniaka z nutką śmietany serwowana na zimno'),
    ],
    'Przystawki': [
        ('Terrine', 30, 'zimna przystawka z pora serwowana z kremowym sosem na bazie śmietany i sera koziego'),
        ('Mule', 42, 'serwowane w maślanym sosie na bazie masła i białego wina z czosnkiem, cebulą i natką pietruszki podane z domowym pieczywem prosto z pieca'),
        ('Tatar', 52, 'polędwica wołowa, czerwona cebula, anchois, musztarda, rydze, żółtko serwowany z pieczywem prosto z pieca'),
        ('Oscypek', 31, 'zawinięty w boczek podawany z konfiturą z żurawiny i mixem sałat'),
    ],
    'Przekąski': [
        ('Koszyk Mix', 45, 'nuggetsy, krążki cebulowe, frytki z batatów, pieczarki faszerowane cheddarem serwowane z sosem czosnkowym'),
        ('Frytki taco', 35, 'frytki z mięsem mielonym w meksykańskich przyprawach podane z paprykowym sosie i serem cheddar'),
        ('Nuggetsy z kurczaka', 30, '10 szt. z sosem czosnkowym'),
        ('Krążki cebulowe', 18, 'z sosem czosnkowym'),
        ('Frytki z ketchupem', 18, ''),
        ('Frytki z serem', 21, ''),
        ('Frytki z batatów', 26, ''),
    ],
    'Sałatki': [
        ('Buratta', 33, 'włoska buratta, bazylia, pomidor, pesto, oliwa z oliwek i sos balsamiczny'),
        ('Z wołowiną', 53, 'polędwica wołowa, mix sałat, ogórek, pomidorki koktailowe, papryka, czerwona cebula, pestki sezamu, marchewka, chilli, sos musztardowo miodowy'),
        ('Domowa sałatka cezar', 42, 'sałata lodowa, kurczak, boczek, grzanki, pomidory, sos cesarski i parmezanem'),
        ('Grecka', 36, 'mix sałat, ogórek, pomidorki koktailowe, papryka, czerwona cebula, oliwki, ser feta podany z domowym sosem winegrette'),
        ('Z Kurczakiem i krewetkami', 49, 'mix sałat, pomidorki koktajlowe, kurczak i krewetki w przyprawie cajun, jabłko, orzechy włoskie, ogórek, sos marie rose'),
    ],
    'Makarony': [
        ('Pappardelle gamberetto', 50, 'krewetki, pomidorki koktajlowe, cukinia, czosnek, świeże chilli serwowane z sosem na bazie białego wina, masła, oliwy z oliwek, natka pietruszki i parmezan'),
        ('Linguine alla carbonara', 48, 'kurczak, cebula, czosnek, pieczarki, boczek w kremowym sosie na bazie śmietany z parmezanem'),
        ('Linguine aglio e olio', 42, 'oliwa z oliwek, czosnek, świeże chilli, natka pietruszki i parmezan'),
        ('Rigatoni al forno', 50, 'polędwiczka wieprzowa, szpinak, mascarpone, sos pomidorowy, czosnek, cebula, nduja zapiekane z parmezanem, serwowane w gorącym półmisku prosto z pieca'),
    ],
    'Ryby': [
        ('Tradycyjne FISH AND CHIPS', 43, 'morszczuk (180g) serwowany w cieście piwnym z frytkami, sosem tatarskim oraz sałatką colesław'),
        ('Karmazyn', 48, 'z patelni serwowany z salsą z mango i mięty podawany z ryżem jaśminowym z kurkumą'),
        ('Stek z kałamarnicy', 48, 'podawany w sosie na bazie białego wina, masła, soku z cytryny, czosnku i świeżej natki pietruszki serwowany z mixem z rukoli i sezonowych warzyw'),
    ],
    'Pizza 30cm': [
        ('Maryśka', 32, 'sos pomidorowy, mozzarella, oliwa z oliwek, oregano'),
        ('Biała Kula', 41, 'sos pomidorowy, mozzarella, burrata, świeże pomidory, pesto bazyliowe, oregano'),
        ('Skurczybyk', 42, 'sos pomidorowy, mozzarella, nduja, mascarpone, czerwona cebula, spianata piccante, oregano'),
        ('Crunchy chicken', 39, 'sos pomidorowy, mozzarella, czerwona cebula, panierowane kawałki kurczaka, świeże pomidorki, oregano'),
        ('Fiflok', 38, 'sos pomidorowy, mozzarella, salami pepperoni, czerwona cebula, oliwki, oregano'),
        ('Americana', 36, 'sos pomidorowy, mozzarella, salami pepperoni, oregano'),
        ('Śniegowy kurczok', 38, 'mozzarella, boczek, kurczak, pieczarki, cebula, parmezan, oregano'),
        ('Diavola', 38, 'sos pomidorowy, mozzarella, spianata piccante, oregano'),
        ('Szyneczka', 34, 'sos pomidorowy, mozzarella, szynka, oregano'),
        ('Grzybowa szynka', 37, 'sos pomidorowy, mozzarella, szynka, pieczarki, oregano'),
        ('Parma', 44, 'sos pomidorowy, mozzarella, szynka parmeńska, rucola, oliwa z oliwek, parmezan, oregano'),
        ('Wydydany dyd', 42, 'sos BBQ, mozzarella, wołowina z pieca, cebula, kurczak, boczek, oregano'),
        ('Quatro formaggi', 40, 'mozzarella, gorgonzola, parmezan, camambert, oregano'),
        ('Dunder świśnie', 41, 'sos pomidorowy, mozzarella, kurczak, boczek, pieczona papryka, płatki chilli, oregano'),
        ('Szybki lopez', 40, 'sos pomidorowy, mozzarella, wołowina z pieca, karmelizowana cebula, parmezan, oregano'),
        ('Kulawy Joe', 40, 'sos pomidorowy, mozzarella, salami pepperoni, cebula, kukurydza, pieczona papryka, oregano'),
        ('Diobeł tasmański', 44, 'sos pomidorowy, mozzarella, salami pepperoni, wołowina z pieca, pieczona papryka, jalapeno, płatki chilli, rucola, oregano'),
        ('Suszony pomidor', 41, 'sos pomidorowy, mozzarella, boczek, suszone pomidory, rucola, sos cesarski, oregano'),
        ('Capriciosa', 39, 'sos pomidorowy, mozzarella, szynka, pieczarki, oliwki, oregano'),
        ('Krejzi wege', 37, 'sos pomidorowy, mozzarella, pieczarki, cebula, pieczona papryka, kukurydza, oregano'),
        ('Łoscypek', 41, 'sos żurawinowy, mozzarella, oscypek, boczek, kurczak, oregano'),
        ('Kreweta', 49, 'sos pomidorowy, mozzarella, krewetki, czosnek, oliwa z oliwek, chilli, pomidory koktajlowe, świeża bazylia, oregano'),
    ],
    'Dodatki do pizzy': [
        ('Sos czosnkowy / ketchup', 3, ''),
        ('Mięso / wędliny', 8, ''),
        ('Warzywa', 4, ''),
        ('Sery', 8, ''),
        ('Krewetki', 26, ''),
        ('Opakowanie na wynos', 2, ''),
    ],
    'Dodatki': [
        ('Mix sałat z winegretem', 14, ''),
        ('Opiekane ziemniaki z rozmarynem', 12, ''),
        ('Pieczywo', 7, ''),
        ('Colesław', 8, ''),
    ],
    'Wołowina': [
        ('Nachos', 48, 'chrupiące nachos z wołowiną w meksykańskich przyprawach z jalapeno, czosnkiem, guacamole, salsa z pomidorków czosnku i cebuli z kolendrą'),
        ('Stek z zielonym pieprzem', 150, 'polędwica wołowa (200g+) serwowany z sosem z zielonego pieprzu z nutką śmietany'),
        ('Stek z masłem czosnkowym', 150, 'z zielonego pieprzu z nutką śmietany'),
    ],
    'Wieprzowina': [
        ('Polędwica wieprzowa', 51, 'w kremowym sosie na bazie demi glassu z pieczarkami i nutką śmietany, opiekane ziemniaki z rozmarynem i grillowana cukinia z papryką'),
        ('Udon', 53, 'azjatycki makaron udon z polędwiczką wieprzową w orientalnym sosie ostrygowym z cebulą, imbirem, czosnkiem i marchewką, papryką, zieloną cebulką i prażonymi pestki sezamu'),
        ('Saltimbocca', 49, 'plastry polędwicy wieprzowej z szynką parmeńską i szałwią w sosie z zielonego pieprzu i nutką śmietany na bazie demi glasu serwowana z opiekanymi ziemniakami z rozmarynem i mixem sałat'),
        ('Żeberka wieprzowe u Połki i Allana', 48, 'serwowane z frytkami i sałatką colesław'),
    ],
    'Drób': [
        ('Kurczak supreme', 43, 'grillowany filet z kurczaka w aksamitnym cytrynowo maślanym sosie podawany z mixem sałat i sosem winegrette'),
        ('Kurczak fricasse', 48, 'udziec z kurczaka bez kości serwowany w sosie na bazie białego wina z porem, pieczarkami, cebulą, czosnkiem i szpinakiem podawany z ziemniakami pure'),
        ('Pollo escobar', 42, 'udziec z kurczaka bez kości panierowany w nachosach serwowany z salsą z mango i mięty podawany z ryżem jaśminowym i kurkumą'),
    ],
    'Burgery': [
        ('Burger z podwójnym mięsem', 52, 'do wyboru z listy poniżej'),
        ('Burger nowy', 41, 'mięso (180g), sałata, pomidor, ser cheddar, pikle, boczek, czerwona cebula'),
        ('Smash burger', 42, '2 plastry wołowiny, sałata, cebula, cheddar, pikle'),
        ('Burger drwala', 42, 'mięso (180g), sałata, camembert w panierce'),
        ('Baca burger', 42, 'mięso (180g), sałata, oscypek, boczek, karmelizowana cebula'),
        ('Blue bacon burger', 42, 'mięso (180g), sałata, pomidor, boczek, ser pleśniowy'),
        ('Cheese burger', 42, 'mięso (180g), sałata, pomidor, pikle, ser cheddar'),
        ('Chilli burger', 42, 'mięso (180g), sałata, pomidor, smażona cebula, jalapeno'),
        ('Boczek burger', 42, 'mięso (180g), sałata, pomidor, boczek, jajko'),
        ('Klasyczny burger', 40, 'mięso (180g), sałata, pomidor'),
        ('Nachos burger', 40, 'filet z kurczaka z panierce z nachosów, sałata, pomidor i guacamole'),
        ('Wege burger', 39, 'sałata, ser cammebert, pomidor, czerwona cebula, guacamole'),
    ],
    'Wrapy': [
        ('Ceasare cajun', 42, 'kurczak w przyprawie cajun, sałata, pomidor, boczek, parmezan, sos ceasare'),
        ('Serowy kurczak', 42, 'panierowany kurczak, sałata, pomidor, ser cheddar, sos czosnkowy'),
        ('Alla burito', 42, 'mięso mielone w meksykańskich przyprawach, sałata, pomidor, kolendra, fasola pinto, jalapeno, czerwona papryka, ser cheddar i kwaśna śmietana'),
    ],
    'Desery': [
        ('Czekoladowy fondant', 30, 'ciasto czekoladowe serwowane na ciepło z lodami waniliowymi i bitą śmietaną'),
        ('Truskawkowe tiramisu', 0, 'inna odmiana włoskiego deseru, w naszym wydaniu z truskawkami'),
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