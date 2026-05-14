from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant

class Command(BaseCommand):
    help = 'Dodaje restauracje do bazy danych'

    def handle(self, *args, **kwargs):
        restaurants = [
            {
                'name': 'Połka i Allan',
                'phone': '669132617',
                'website_url': 'https://www.upajdygorlice.pl/',
                'facebook_url': None,
                'opening_time': '11:00',
                'closing_time': '22:00',
            },
            {
                'name': 'Dworcowa',
                'phone': '730022404',
                'website_url': None,
                'facebook_url': 'https://www.facebook.com/dworcowagorlice/',
                'opening_time': '08:00',
                'closing_time': '18:00',
            },
            {
                'name': 'Vesuvio',
                'phone': '669666455',
                'website_url': None,
                'facebook_url': 'https://www.facebook.com/people/Vesuvio-Pizza-Pasta/61585854013446/',
                'opening_time': '10:00',
                'closing_time': '21:00',
            },
            {
                'name': 'Dark Pub',
                'phone': '733575759',
                'website_url': 'https://darkpub.pl/menu-restauracji/',
                'facebook_url': None,
                'opening_time': '12:00',
                'closing_time': '23:00',
            },
            {
                'name': 'Mała Italia',
                'phone': '513402880',
                'website_url': None,
                'facebook_url': 'https://www.facebook.com/PizzeriaItaliaGorlice/',
                'opening_time': '11:00',
                'closing_time': '21:00',
            },
            {
                'name': 'Klitka u Witka',
                'phone': '531377362',
                'website_url': 'https://klitkauwitka.pl/',
                'facebook_url': None,
                'opening_time': '10:00',
                'closing_time': '20:00',
            },
            {
                'name': 'New York',
                'phone': '183536825',
                'website_url': 'https://barnewyorkgorlice.pl/wp-content/uploads/2023/11/menu-bistro-new-york-druk.pdf',
                'facebook_url': None,
                'opening_time': '10:00',
                'closing_time': '21:00',
            },
            {
                'name': 'Burger Bar',
                'phone': '735073060',
                'website_url': 'https://cdn.website.dish.co/media/1c/eb/9475896/Menu.jpg',
                'facebook_url': None,
                'opening_time': '11:00',
                'closing_time': '21:00',
            },
            {
                'name': 'Del Piero',
                'phone': '516461135',
                'website_url': 'https://delpiero.gorlice.pl/wp-content/uploads/2026/02/menu-delpiero-2026-bez-grubych.pdf',
                'facebook_url': None,
                'opening_time': '11:00',
                'closing_time': '21:00',
            },
            {
                'name': 'Rafaello',
                'phone': '507426428',
                'website_url': 'https://www.rafaello.gorlice.pl/',
                'facebook_url': None,
                'opening_time': '10:00',
                'closing_time': '21:00',
            },
            {
                'name': 'Bar Wojtek',
                'phone': '571243989',
                'website_url': 'https://barwojtekgorlice.pl/section:menu/polecane',
                'facebook_url': None,
                'opening_time': '09:00',
                'closing_time': '18:00',
            },
            {
                'name': 'Doner Kebab',
                'phone': '185346534',
                'website_url': 'https://www.donerking.pl/menu/',
                'facebook_url': None,
                'opening_time': '11:00',
                'closing_time': '22:00',
            },
            {
                'name': 'Zaza',
                'phone': '512785994',
                'website_url': None,
                'facebook_url': 'https://www.facebook.com/people/ZAZA-D%C3%96NER-Kebab-Gorlice/100063653014958/',
                'opening_time': '11:00',
                'closing_time': '22:00',
            },
            {
                'name': 'Kebab u Pajdy',
                'phone': '537614907',
                'website_url': 'https://www.upajdygorlice.pl/',
                'facebook_url': None,
                'opening_time': '11:00',
                'closing_time': '22:00',
            },
        ]

        for r in restaurants:
            restaurant, created = Restaurant.objects.get_or_create(
                name=r['name'],
                defaults={
                    'phone': r['phone'],
                    'website_url': r['website_url'],
                    'facebook_url': r['facebook_url'],
                    'opening_time': r['opening_time'],
                    'closing_time': r['closing_time'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Dodano: {restaurant.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Już istnieje: {restaurant.name}'))

        self.stdout.write(self.style.SUCCESS('Gotowe!'))