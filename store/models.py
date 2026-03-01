from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nazwa produktu")
    description = models.TextField(blank=True, verbose_name="Opis")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena podstawowa")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Produkt"
        verbose_name_plural = "Produkty"

class Color(models.Model):
    product = models.ForeignKey(Product, related_name='colors', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Nazwa koloru")
    hex_code = models.CharField(max_length=7, default="#FFFFFF", verbose_name="Kod Hex (np. #FF0000)")
    image = models.ImageField(upload_to='products/colors/', blank=True, null=True, verbose_name="Zdjęcie wariantu")
    extra_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Dodatkowa cena")

    def __str__(self):
        return f"{self.name} (+{self.extra_price} zł)"

    class Meta:
        verbose_name = "Kolor"
        verbose_name_plural = "Kolory"

class SubOption(models.Model):
    product = models.ForeignKey(Product, related_name='options', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Nazwa opcji")
    extra_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Dodatkowa cena")

    def __str__(self):
        return f"{self.name} (+{self.extra_price} zł)"

    class Meta:
        verbose_name = "Podopcja"
        verbose_name_plural = "Podopcje"
