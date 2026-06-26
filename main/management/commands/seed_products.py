import requests
from decimal import Decimal
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from main.models import Category, Product, ProductImage, Size, ProductSize

# твоя категория -> источники DummyJSON
CATEGORY_MAP = {
    "Men's Shirts":    ["mens-shirts"],
    "Men's Shoes":     ["mens-shoes"],
    "Women's Dresses": ["womens-dresses"],
    "Women's Shoes":   ["womens-shoes"],
    "Accessories":     ["womens-bags", "sunglasses"],
}
SIZES = ["XS", "S", "M", "L", "XL"]


class Command(BaseCommand):
    help = "Seed clothing products from DummyJSON"

    def add_arguments(self, parser):
        parser.add_argument("--per", type=int, default=10,
                            help="max products per category")

    def handle(self, *args, **opts):
        per = opts["per"]
        sizes = [Size.objects.get_or_create(name=s)[0] for s in SIZES]

        for cat_name, sources in CATEGORY_MAP.items():
            category, _ = Category.objects.get_or_create(name=cat_name)
            items = []
            for src in sources:
                url = f"https://dummyjson.com/products/category/{src}"
                items += requests.get(url, timeout=30).json().get("products", [])
            items = items[:per]

            for item in items:
                product, created = Product.objects.get_or_create(
                    name=item["title"],
                    defaults={
                        "category": category,
                        "color": item.get("color") or "Assorted",
                        "price": Decimal(str(item["price"])),
                        "description": item.get("description", ""),
                    },
                )
                if not created:
                    continue

                # главное фото
                thumb = item.get("thumbnail")
                if thumb:
                    r = requests.get(thumb, timeout=30)
                    if r.ok:
                        product.mainImage.save(
                            f"{product.slug}-main.jpg",
                            ContentFile(r.content), save=True)

                # pictures (4-5)
                for i, img_url in enumerate(item.get("images", [])[:5]):
                    r = requests.get(img_url, timeout=30)
                    if r.ok:
                        pi = ProductImage(product=product)
                        pi.image.save(
                            f"{product.slug}-{i}.jpg",
                            ContentFile(r.content), save=True)

                # размеры + сток
                total = item.get("stock", 20)
                for sz in sizes:
                    ProductSize.objects.create(
                        product=product, size=sz,
                        stock=max(total // len(sizes), 1))

            self.stdout.write(self.style.SUCCESS(
                f"{cat_name}: {len(items)} products"))