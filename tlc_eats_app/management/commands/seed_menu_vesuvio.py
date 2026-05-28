from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem

MENU = {
    'Przystawki': [
        ('Tigelle Emiliane (3 szt.)', 10, 'Okrągłe chlebki pochodzące z regionu Emilia-Romania podawane z oliwą z oliwek extra virgin lub oliwą czosnkową'),
        ('Antipasti – deska serów i wędlin dla dwóch osób', 80, 'Gorgonzola, mozzarella di bufala, Grana Padano, Parmigiano Reggiano, prosciutto cotto, salami Napoli, szynka parmeńska, boczek rolowany, oliwki czarne, pomidory suszone, focaccia'),
    ],
    'Pizza Rosa': [
        ('Margherita (rosa)', 33, 'Pomidory San Marzano DOP, mozzarella Fior di Latte, parmigiano reggiano, oliwa z oliwek, świeża bazylia'),
        ('Cotto (rosa)', 36, 'Pomidory San Marzano DOP, mozzarella Fior di Latte, prosciutto cotto, oliwa z oliwek, świeża bazylia'),
        ('Regina (rosa)', 37, 'Pomidory San Marzano DOP, mozzarella Fior di Latte, prosciutto cotto, pieczarki, oliwa z oliwek, świeża bazylia'),
        ('Prosciutto di Parma (rosa)', 44, 'Pomidory San Marzano DOP, mozzarella Fior di Latte, szynka parmeńska, płatki parmezanu, rukola, oliwa z oliwek, świeża bazylia'),
        ('Capricciosa (rosa)', 40, 'Pomidory San Marzano DOP, mozzarella Fior di Latte, prosciutto cotto, karczochy, pieczarki, czarne oliwki, oliwa z oliwek, świeża bazylia'),
        ('Diavola Spinata Picante (rosa)', 44, 'Pomidory San Marzano DOP, mozzarella Fior di Latte, salami piccante, oliwa z oliwek, świeża bazylia'),
        ('Calabria (rosa)', 48, 'Pomidory San Marzano DOP, mozzarella fior di latte, parmigiano reggiano, salami picante, nduja, gorgonzola, oliwa z oliwek, świeża bazylia'),
        ('Wegetariana (rosa)', 46, 'Pomidory San Marzano DOP, mozzarella Fior di Latte, bakłażan, papryka, cukinia, oliwa z oliwek'),
        ('Ricotta (rosa)', 46, 'Pomidory San Marzano DOP, mozzarella Fior di Latte, salami napoli, ricotta, włoski boczek - pancetta, oliwa z oliwek, świeża bazylia'),
        ('Vesuvio (rosa)', 55, 'Cztery różne smaki - dwa rossa i dwa bianca - pomidory San Marzano DOP, mozzarella Fior di Latte, salami Piccante, salami łagodne, włoski boczek-pancetta, rukola, szynka parmeńska, parmigiano reggiano, oliwa z oliwek, świeża bazylia'),
        ('Bufalina (rosa)', 49, 'Pomidory San Marzano DOP, mozzarella di bufalo DOP, oliwa z oliwek, świeża bazylia'),
        ('Milano (rosa)', 37, 'Pomidory San Marzano DOP, mozzarella Fior di Latte, salami łagodne, pieczarki, oliwa z oliwek, świeża bazylia'),
        ('Calzone (rosa)', 37, 'ciasto w kszatlcie muszli, Pomidory San marzano dop, mozzarella Fior di Latte, salami Napoli, ricotta, oliwa z oliwek, świeża bazylia'),
    ],
    'Pizza Bianca': [
        ('Cinque Formaggi (bianca)', 43, 'Mozzarella Fior di Latte, scamarza, gorgonzola, parmezan, ricotta, oliwa z oliwek, świeża bazylia'),
        ('Pizza Pesto Verde (bianca)', 52, 'Mozzarella Fior di latte, Parmigiano Reggiano, pomidorki cherry, pomidory suszone, burrata, pesto bazyliowe'),
        ('Masaniello (bianca)', 49, 'Friarielli, mozzarella Fior di Latte, Parmigiano Reggiano, salsiccia napoletana, bazylia, oliwa z oliwek'),
        ('Tartufetta (bianca)', 55, 'Oliwa z oliwek, boczek włoski - pancetta, borowiki, mozzarella fior di latte, Parmigiano Reggiano, bazylia, krem truflowy'),
        ('Carbonara (bianca)', 37, 'Mozzarella Fior di Latte, boczek włoski - pancetta, jajko, pieprz, grana padano, oliwa z oliwek, świeża bazylia'),
        ('Crudo (bianca)', 44, 'Mozzarella Fior di Latte, pomidorki cherry, rukola, szynka parmeńska, płatki parmezanu, oliwa z oliwek, świeża bazylia'),
    ],
    'Makarony': [
        ('Carbonara', 42, 'żółtko, guanciale, pieprz, Parmigiano Reggiano'),
        ('Siciliana', 52, 'bakłażan, kiełbasa salsiccia, sos pomidorowy'),
        ('Tagliatelle bolognese', 36, 'tagliatelle, sos bolognese z wołowiną, bazylia'),
        ('Gnocchi alla Sorrentina', 32, 'gnocchi, sos pomidorowy, mozzarella, Parmigiano Reggiano, bazylia'),
        ('Penne alla pesto di basilico', 34, 'pesto bazyliowe, Parmigiano Reggiano, bazylia'),
        ('Spaghetti aglio olio peperoncino', 32, 'czosnek, oliwa, chili, pietruszka'),
        ('Tagliatelle gamberetti', 49, 'tagliatelle, krewetki, masło czosnkowe'),
        ('Tagliatelle alla romana', 44, 'guanciale, sos pomidorowy, gorgonzola, Parmigiano Reggiano, bazylia'),
    ],
    'Przekąski': [
        ('Frytki małe 140g', 14, ''),
        ('Frytki z parmigiano reggiano', 19, '140g, ser'),
        ('Frytki z guanciale i parmigiano reggiano' , 23, '140g, guanciale, ser'),
        ('Patatine Croccanti ', 18, '150g chrupiących frytek ze skórką w panierce'),
        ('Ćwiartki ziemniaków', 15, '150g'),
    ],
    'Desery': [
        ('Tiramisu', 19, ''),
        ('Angioletti fritti con Nutella', 21, 'Smażone paluchy z ciasta na głębokim oleju, podawane z cukrem pudrem i Nutellą'),
    ],
    'Napoje': [
        ('Pepsi/Coca cola 250ml', 8, ''),
        ('Pepsi/Coca cola 1l', 22, ''),
        ('Soki 250ml', 7, 'pomarańcza/ jabłko/ multiwitamina'),
        ('Soki 1l', 19, 'pomarańcza/ jabłko/ multiwitamina'),
        ('Herbata', 9, 'o dostępne smaki proszę zapytać naszą obsługę'),
        ('Woda 0,33l', 5, ''),
        ('Woda 1l', 15, ''),
    ],
}

class Command(BaseCommand):
    help = 'Seed menu Vesuvio'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='Vesuvio')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono Vesuvio w bazie!'))
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