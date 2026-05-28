from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, Category, MenuItem, OptionGroup, Option

MENU = {
    'Pizza': [
        ('Margherita', 26.0, 'sos pomidorowy / ser mozzarella', [], []),
        ('Wiejska Italia', 39.0, 'sos pomidorowy / ser mozzarella / kiełbasa / boczek / salami Milano / ser gorgonzola / cebula czerwona / pieczarki / kukurydza', [], []),
        ('Parma', 39.0, 'sos pomidorowy / ser mozzarella / szynka parmeńska / rukola / parmezan', [], []),
        ('Prosciutto Funghi', 36.0, 'sos pomidorowy / ser mozzarella / szynka / pieczarki', [], []),
        ('Salami', 36.0, 'sos pomidorowy / ser mozzarella / salami Milano', [], []),
        ('Capricciosa', 36.0, 'sos pomidorowy / ser mozzarella / papryka / szynka / oliwki / pieczarki', [], []),
        ('Diavola', 36.0, 'sos pomidorowy / ser mozzarella / ostre salami Ventricina', [], []),
        ('Quattro Formaggi', 39.0, 'ser mozzarella / gorgonzola / parmezan / feta / płatki chili', [], []),
        ('Tonno', 36.0, 'sos pomidorowy / ser mozzarella / tuńczyk / cebula czerwona / czosnek', [], []),
        ('Pollo', 36.0, 'sos pomidorowy / ser mozzarella / kurczak / kukurydza / cebula czerwona / jalapeno', [], []),
        ('Maiale', 36.0, 'sos pomidorowy / ser mozzarella / boczek / kiełbasa / czerwona cebula / kukurydza', [], []),
        ('Italia', 36.0, 'sos pomidorowy / ser mozzarella / ser gorgonzola / świeże pomidory / świeże liście bazylii', [], []),
        ('Vegetariana', 36.0, 'sos pomidorowy / ser mozzarella / kukurydza / papryka / cebula / czosnek / pieczarki / cukinia / karczochy', [], []),
        ('Hawaii', 36.0, 'sos pomidorowy / ser mozzarella / szynka / ananas', [], []),
        ('Angelo', 36.0, 'sos pomidorowy / ser mozzarella / kurczak / boczek / pieczarki', [], []),
        ('Mexicana', 36.0, 'sos pomidorowy / ser mozzarella / kurczak / kiełbasa Chorizo / jalapeno / fasola czerwona / cebula czerwona / kukurydza / papryka', [], []),
        ('Foresta', 39.0, 'sos pomidorowy / ser mozzarella / ser scamorza / kurczak / pieczarki / karmelizowana cebula / grzyby leśne / rozmaryn', [], []),
        ('Piccante', 36.0, 'sos pomidorowy / ser mozzarella / salami Milano / pieczarki / jalapeno / cebula', [], []),
        ('Calzone Mięsne', 36.0, 'calzone z sosem bolońskim i mozzarellą, rukolą i sosem czosnkowym', [], []),
        ('Calzone Wegetariańskie', 36.0, 'calzone z marchewką, cebulą, papryką, brokułem, pieczarkami, cukinią i mozzarellą, podany z rukolą i sosem pomidorowym', [], []),
        ('Pizza Bianca', 36.0, 'mozzarella, gorgonzola, feta, gruszka, orzechy włoskie, krem balsamiczny, rukola', [], []),
    ],
    'Makarony': [
        ('Spaghetti Bolognese', 34.5, 'tradycyjny wołowy sos boloński', [], []),
        ('Penne Secchi', 34.5, 'kurczak / suszone pomidory / czosnek / białe wino / śmietanka', [], []),
        ('Lasagne', 38.0, 'sos boloński / beszamel / mozzarella', [], []),
        ('Spaghetti Carbonara', 34.5, 'śmietanka / boczek / żółtko / parmezan', [], []),
        ('Penne Alfredo', 34.5, 'kurczak / pieczarka / boczek / brokuł / śmietanka', [], []),
        ('Tagliatelle al Gorgonzola', 38.0, 'gorgonzola / szpinak / czosnek / śmietanka / orzeszki pini / suszone pomidory / rukola', [], []),
        ('Gnocchi alla Sorentina', 29.0, 'sos pomidorowy / bazylia / mozzarella', [], []),
        ('Spaghetti Marinara', 49.5, 'makaron z owocami morza (kalmary, krewetki, małże) / łosoś / białe wino / oliwa / pietruszka / czosnek / chili / pomidorki koktajlowe', [], []),
        ('Spaghetti Pomodoro con Polo', 34.5, 'kurczak / pomidorki koktajlowe / czosnek / oliwa / świeża bazylia / parmezan', [], []),
        ('Gnocchi ai Funghi', 34.5, 'włoskie kopytka w sosie grzybowym / chipsy z szynki parmeńskiej / rukola / oliwa truflowa', [], []),
        ('Spaghetti con Gamberoni', 49.5, 'krewetki 8 szt / czosnek / pietruszka / białe wino / masło / pomidorki / płatki chili', [], []),
        ('Tagliatelle Funghi con Pollo', 34.5, 'grzyby leśne / kurczak / cebula / pietruszka / masło / białe wino / rozmaryn', [], []),
        ('Ravioli', 34.5, 'ravioli nadziewane szpinakiem i serem ricotta w sosie śmiet.-pomidor.', [], []),
        ('Penne all Amatriciana', 34.5, 'boczek / cebula / czosnek / czerwone wino / sos pomidorowy / płatki chili / pietruszka nać', [], []),
        ('Spaghetti al Tonno', 38.5, 'tuńczyk / oregano / czosnek / płatki chili / pomidorki koktajlowe / białe wino / pietruszka nać', [], []),
        ('Tagliatelle al Salmone', 38.0, 'łosoś / brokuł / marchew / zielony groszek / pomidorek suszony / śmietana / oliwa', [], []),
        ('Penne al Forno', 34.5, 'zapiekany makaron / sos Ragu / kurczak / kiełbasa Chorizo / cukinia / śmietanka / mozzarella', [], []),
        ('Penne Pesto con Pollo', 34.5, 'makaron penne / zielone pesto / cukinia / ziemniak / kurczak w panierce panko', [], []),
        ('Tagliatelle Maiale', 38.0, 'polędwiczka wieprzowa / boczek / czosnek / białe wino / grzyby leśne / fasolka szparagowa / śmietanka / parmezan', [], []),
        ('Tortellone con Funghi Porcini', 38.0, 'pierożki nadziewane serem ricotta i prawdziwkami w sosie grzybowo-trufl.', [], []),
    ],
    'Przekąski': [
        ('Focaccia', 15.0, 'czosnek / sól morska / oliwa / rozmaryn', [], []),
        ('Focaccia z serem', 18.0, 'mozzarella / oregano', [], []),
        ('Bruschetta', 28.0, '1 grzanka - pomidor / czosnek / bazylia, 2 grzanka - mozzarella / szynka parmeńska / rukola / płatki parmezanu, 3 grzanka - gorgonzola / salami Milano', [], []),
        ('Antipasto Italiano', 68.0, 'selekcja wędlin i serów z piklami podane z focaccią', [], []),
        ('Gamberoni Provincial', 49.5, 'krewetki 8 szt / pomidorki koktajlowe / wino / zioła / papryczka chili / rukola / masło / podane z focaccią', [], []),
    ],
    'Dania główne': [
        ('Polędwiczka wieprzowa', 39.5, 'w winnym sosie grzybowo cebulowym podana z włoskimi kopytkami gnocchi i mixem sałat', [], []),
        ('Schabowy', 39.5, 'schab z kością podany z opiekanymi ziemniakami z czosnkiem, rozmarynem oraz surówką Coleslaw', [], []),
        ('Żeberka Texas BBQ', 39.5, 'podane z frytkami, surówką Coleslaw i rukolą z sosem balsamicznym', [], []),
        ('Grill Lucanica', 38.5, 'włoska kiełbasa / cebula karmelizowana / podane z frytkami i orientalną sałatką', [], []),
        ('Chicken Ocini', 39.5, 'filet z kurczaka / sos pieczarkowy / śmietanka / białe wino / grillowane warzywa / mix sałat', [], []),
        ('Risotto alla Boscaiola', 34.5, 'risotto / leśne grzyby / kurczak / cebula / rozmaryn / białe wino / śmietanka / parmezan', [], []),
        ('Risotto alla Vegetariana', 34.5, 'risotto / warzywa / białe wino / śmietanka / rukola / parmezan', [], []),
        ('Gnocchi', 18.0, 'z masłem, cukrem i cynamonem', [], []),
        ('Polędwiczki panierowane z kurczaka', 27.0, 'podane z frytkami i surówką Coleslaw, panierka Panko', [], []),
        ('Spaghetti Napoli', 23.0, 'sos pomidorowy / parmezan', [], []),
        ('Penne', 23.0, 'sos śmietanowo-pomidorowy / parmezan', [], []),
        ('Spaghetti Burro', 18.0, 'makaron / masło / parmezan', [], []),
        ('Burger Tradycyjny', 34.5, 'mięso wołowe 180g / boczek / ser cheddar / cebula / ogórek / pomidor / sałata / ketchup / majonez', [], []),
        ('Burger Włoski', 34.5, 'mięso wołowe 180g / szynka parmeńska / mozzarella / rukola / pomidor / cebula karmelizowana / sos pomidorowy Napoli', [], []),
        ('Burger Pollo', 28.5, 'panierowany kurczak 180g / boczek / ser cheddar / cebula / sałata / ogórek / pomidor / majonez / ketchup', [], []),
        ('Burger Diablo', 34.5, 'mięso wołowe 180g / pikantna włoska wędlina ventricina / ser cheddar / ogórek / pomidor / cebula / sałata / jalapeno / sos BBQ / musztarda', [], []),
        ('Taco Chips', 34.5, 'sos boloński wołowy / frytki / świeża papryka / papryczka chili / mozzarella / cheddar / cebulka prażona', [], []),
        ('Salmone al Forno', 58.5, 'pieczony filet z łososia w sosie śmietanowo-kaparowym z rodzynkami i orzechami pini / warzywa saute / mix sałat', [], []),
        ('Brodetto', 59.5, 'owoce morza (kalmary, krewetki, małże) / łosoś w sosie winno-pomidorowym podane z focaccią', [], []),
        ('Krewetki Panierowane', 49.5, 'krewetki 8 szt podane z frytkami rucolą oraz sosem słodkie chili, czosnkowy, panierka panko', [], []),
    ],
    'Sałatki': [
        ('Sałatka Cesare', 34.5, 'mix sałat / pomidor / ogórek / kurczak / czerwona cebula / prażona szynka parmeńska / grzanki / parmezan / sos Cezara', [], []),
        ('Sałatka Greca', 34.5, 'mix sałat / pomidor / ogórek / papryka / czerwona cebula / ser feta / oliwki / dressing sałatkowy', [], []),
        ('Sałatka Girasole', 34.5, 'mix sałat / kurczak / pomidor / ogórek / czerwona cebula / słonecznik / dressing sałatkowy', [], []),
        ('Sałatka Tuna Nicoise', 38.5, 'mix sałat / tuńczyk / pomidor / ogórek / oliwki / czerwona cebula / anchovies / kapary / jajko w koszulce / opiekany ziemniak', [], []),
    ],
    'Dodatki': [
        ('Frytki', 9.0, '', [('250g', 0)], []),
        ('Ziemniaki opiekane z czosnkiem i rozmarynem', 15.0, '', [('250g', 0)], []),
        ('Gnocchi z rozmarynem', 15.0, '', [('200g', 0)], []),
        ('Colesław', 9.0, '', [], []),
        ('Mix sałat', 9.0, '', [], []),
        ('Parmezan', 6.0, '', [('20g', 0)], []),
    ],
    'Napoje': [
        ('Herbata', 7.0, '', [], []),
        ('Kawa czarna', 8.0, '', [], []),
        ('Kawa biała', 9.0, '', [], []),
        ('Kawa latte', 11.0, '', [], []),
        ('Sok Cappy', 8.5, '', [], []),
        ('Sprite, Fanta, Coca-cola 500ml', 9.5, '', [], []),
        ('Coca-Cola zero', 8.5, '', [], []),
        ('Bibite Italiane', 9.0, 'Lemon Soda, Orange, Mojito, Chinotto', [], []),
        ('Woda gazowana', 5.5, '', [], []),
        ('Woda niegazowana', 5.5, '', [], []),
        ('Oranżada', 7.0, 'czerwona, kiwi, gruszka', [], []),
    ],
}


class Command(BaseCommand):
    help = 'Seed menu Mała Italia'

    def handle(self, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(name='Mała Italia')
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Nie znaleziono Mała Italia w bazie!'))
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