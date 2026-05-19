from django.core.management.base import BaseCommand
from tlc_eats_app.models import Restaurant, RestaurantHours

class Command(BaseCommand):
    help = 'Dodaje restauracje do bazy danych'

    def handle(self, *args, **kwargs):
        restaurants = [
            {
                'name': 'Połka i Allan',
                'phone': '669132617',
                'website_url': None,
                'facebook_url': None,
                'hours': {
                    0: ('11:00', '22:00'), 1: ('11:00', '22:00'),
                    2: ('11:00', '22:00'), 3: ('11:00', '22:00'),
                    4: ('11:00', '22:00'), 5: ('11:00', '22:00'),
                    6: ('13:00', '21:00'),
                }
            },
            {
                'name': 'Lucy Bar',
                'phone': '723834440',
                'website_url': None,
                'facebook_url': None,
                'hours': {
                    0: ('08:00', '19:00'), 1: ('08:00', '19:00'),
                    2: ('08:00', '19:00'), 3: ('08:00', '19:00'),
                    4: ('08:00', '19:00'), 5: ('08:00', '19:00'),
                    6: ('11:00', '19:00'),
                }
            },
            {
                'name': 'Dworcowa',
                'phone': '730022404',
                'website_url': None,
                'facebook_url': None,
                'hours': {
                    0: ('11:00', '22:00'), 1: ('11:00', '22:00'),
                    2: ('11:00', '22:00'), 3: ('11:00', '22:00'),
                    4: ('11:00', '22:00'), 5: ('11:00', '22:00'),
                    6: ('13:00', '21:00'),
                }
            },
            {
                'name': 'Vesuvio',
                'phone': '669666455',
                'website_url': None,
                'facebook_url': None,
                'hours': {
                    0: (None, None, True),
                    1: (None, None, True),
                    2: ('13:00', '21:00'), 3: ('13:00', '21:00'),
                    4: ('13:00', '21:00'), 5: ('13:00', '21:00'),
                    6: ('12:00', '20:00'),
                }
            },
            {
                'name': 'Dark Pub',
                'phone': '733575759',
                'website_url': 'https://darkpub.pl/menu-restauracji/',
                'facebook_url': None,
                'hours': {
                    0: ('10:00', '21:00'), 1: ('10:00', '21:00'),
                    2: ('10:00', '21:00'), 3: ('10:00', '21:00'),
                    4: ('10:00', '22:00'), 5: ('10:00', '22:00'),
                    6: ('13:00', '21:00'),
                }
            },
            {
                'name': 'Mała Italia',
                'phone': '513402880',
                'website_url': None,
                'facebook_url': 'https://www.facebook.com/PizzeriaItaliaGorlice/',
                'hours': {
                    0: ('10:00', '21:00'), 1: ('10:00', '21:00'),
                    2: ('10:00', '21:00'), 3: ('10:00', '21:00'),
                    4: ('10:00', '22:00'), 5: ('10:00', '22:00'),
                    6: ('13:00', '21:00'),
                }
            },
            {
                'name': 'Klitka u Witka',
                'phone': '531377362',
                'website_url': 'https://klitkauwitka.pl/',
                'facebook_url': None,
                'hours': {
                    0: ('10:00', '21:00'), 1: ('10:00', '21:00'),
                    2: ('10:00', '21:00'), 3: ('10:00', '21:00'),
                    4: ('10:00', '22:00'), 5: ('10:00', '22:00'),
                    6: ('13:00', '21:00'),
                }
            },
            {
                'name': 'New York',
                'phone': '183536825',
                'website_url': 'https://barnewyorkgorlice.pl/wp-content/uploads/2023/11/menu-bistro-new-york-druk.pdf',
                'facebook_url': "https://www.facebook.com/barnewyorkgorlice/"
,
                'hours': {
                    0: ('09:00', '17:00'), 1: ('09:00', '17:00'),
                    2: ('09:00', '17:00'), 3: ('09:00', '17:00'),
                    4: ('09:00', '17:00'), 5: ('09:00', '17:00'),
                    6: ('10:00', '17:00'),
                }
            },
            {
                'name': 'Burger Bar',
                'phone': '735073060',
                'website_url': 'https://cdn.website.dish.co/media/1c/eb/9475896/Menu.jpg',
                'facebook_url': None,
                'hours': {
                    0: ('09:00', '17:00'), 1: ('09:00', '17:00'),
                    2: ('09:00', '17:00'), 3: ('09:00', '17:00'),
                    4: ('09:00', '17:00'), 5: ('09:00', '17:00'),
                    6: ('10:00', '17:00'),
                }
            },
            {
                'name': 'Del Piero',
                'phone': '516461135',
                'website_url': 'https://delpiero.gorlice.pl/wp-content/uploads/2026/02/menu-delpiero-2026-bez-grubych.pdf',
                'facebook_url': None,
                'hours': {
                    0: (None, None, True),
                    1: ('10:00', '21:00'), 2: ('10:00', '21:00'),
                    3: ('10:00', '21:00'), 4: ('10:00', '22:00'),
                    5: ('10:00', '22:00'), 6: ('12:00', '21:00'),
                }
            },
            {
                'name': 'Rafaello',
                'phone': '507426428',
                'website_url': 'https://www.rafaello.gorlice.pl/',
                'facebook_url': None,
                'hours': {
                    0: (None, None, True),
                    1: ('10:00', '21:00'), 2: ('10:00', '21:00'),
                    3: ('10:00', '21:00'), 4: ('10:00', '22:00'),
                    5: ('10:00', '22:00'), 6: ('12:00', '21:00'),
                }
            },
            {
                'name': 'Bar Wojtek',
                'phone': '571243989',
                'website_url': 'https://barwojtekgorlice.pl/section:menu/polecane',
                'facebook_url': None,
                'hours': {
                    0: ('10:00', '22:00'),
                    1: ('10:00', '21:00'), 2: ('10:00', '21:00'),
                    3: ('10:00', '21:00'), 4: ('10:00', '22:00'),
                    5: ('10:00', '22:00'), 6: (None, None, True),
                }
            },
            {
                'name': 'Doner Kebab',
                'phone': '185346534',
                'website_url': 'https://www.donerking.pl/menu/',
                'facebook_url': None,
                'hours': {
                    0: ('10:00', '22:00'), 1: ('10:00', '22:00'),
                    2: ('10:00', '22:00'), 3: ('10:00', '22:00'),
                    4: ('10:00', '23:00'), 5: ('10:00', '23:00'),
                    6: ('12:00', '22:00'),
                }
            },
            {
                'name': 'Zaza',
                'phone': '512785994',
                'website_url': None,
                'facebook_url': None,
                'hours': {
                    0: ('09:00', '22:00'), 1: ('09:00', '22:00'),
                    2: ('09:00', '22:00'), 3: ('09:00', '22:00'),
                    4: ('09:00', '23:00'), 5: ('09:00', '23:00'),
                    6: ('12:00', '22:00'),
                }
            },
            {
                'name': 'Kebab u Pajdy',
                'phone': '537614907',
                'website_url': 'https://www.upajdygorlice.pl/',
                'facebook_url': None,
                'hours': {
                    0: ('11:00', '21:00'), 1: ('11:00', '21:00'),
                    2: ('11:00', '21:00'), 3: ('11:00', '21:00'),
                    4: ('11:00', '21:00'), 5: ('11:00', '21:00'),
                    6: ('14:00', '21:00'),
                }
            },
        ]

        for r in restaurants:
            restaurant, created = Restaurant.objects.update_or_create(
                name=r['name'],
                defaults={
                    'phone': r['phone'],
                    'website_url': r['website_url'],
                    'facebook_url': r['facebook_url'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Dodano: {restaurant.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Zaktualizowano: {restaurant.name}'))

            for day, times in r['hours'].items():
                is_closed = len(times) == 3 and times[2] is True
                RestaurantHours.objects.update_or_create(
                    restaurant=restaurant,
                    day=day,
                    defaults={
                        'opening_time': None if is_closed else times[0],
                        'closing_time': None if is_closed else times[1],
                        'is_closed': is_closed,
                    }
                )

        self.stdout.write(self.style.SUCCESS('Wszystkie restauracje dodane!'))