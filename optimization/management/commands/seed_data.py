from django.core.management.base import BaseCommand
from optimization.models import Factory, Product


class Command(BaseCommand):
    help = 'Seeds factories and products based on Nassau Candy requirements'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding Factories...")

        # 1. Create Factories
        factories_data = [
            {"name": "Lot's O' Nuts", "lat": 32.881893, "lon": -111.768036},
            {"name": "Wicked Choccy's", "lat": 32.076176, "lon": -81.088371},
            {"name": "Sugar Shack", "lat": 48.11914, "lon": -96.18115},
            {"name": "Secret Factory", "lat": 41.446333, "lon": -90.565487},
            {"name": "The Other Factory", "lat": 35.1175, "lon": -89.971107},
        ]

        factory_objs = {}
        for f in factories_data:
            obj, created = Factory.objects.update_or_create(
                name=f["name"],
                defaults={"latitude": f["lat"], "longitude": f["lon"]}
            )
            factory_objs[f["name"]] = obj

        self.stdout.write("Seeding Products...")

        # 2. Create Products linked to specific Factories (per requirements)
        products_data = [
            ("Chocolate", "Wonka Bar - Nutty Crunch Surprise", "Lot's O' Nuts"),
            ("Chocolate", "Wonka Bar - Fudge Mallows", "Lot's O' Nuts"),
            ("Chocolate", "Wonka Bar -Scrumdiddlyumptious", "Lot's O' Nuts"),
            ("Chocolate", "Wonka Bar - Milk Chocolate", "Wicked Choccy's"),
            ("Chocolate", "Wonka Bar - Triple Dazzle Caramel", "Wicked Choccy's"),
            ("Sugar", "Laffy Taffy", "Sugar Shack"),
            ("Sugar", "SweeTARTS", "Sugar Shack"),
            ("Sugar", "Nerds", "Sugar Shack"),
            ("Sugar", "Fun Dip", "Sugar Shack"),
            ("Other", "Fizzy Lifting Drinks", "Sugar Shack"),
            ("Sugar", "Everlasting Gobstopper", "Secret Factory"),
            ("Sugar", "Hair Toffee", "The Other Factory"),
            ("Other", "Lickable Wallpaper", "Secret Factory"),
            ("Other", "Wonka Gum", "Secret Factory"),
            ("Other", "Kazookles", "The Other Factory"),
        ]

        for division, name, f_name in products_data:
            Product.objects.update_or_create(
                name=name,
                defaults={
                    "division": division,
                    "current_factory": factory_objs[f_name]
                }
            )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))