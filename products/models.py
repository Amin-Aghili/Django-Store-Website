from django.db import models


class Product(models.Model):
    online = models.BooleanField(default=True)
    name = models.CharField(max_length=255, null=True)
    price = models.IntegerField(null=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    size = models.CharField(max_length=255, null=True, blank=True)
    link = models.CharField(max_length=255, null=True, blank=True)
    image_url = models.CharField(max_length=255, null=True, blank=True)
    price_tl = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            if self.online:
                url = self.image_url
            else:
                url = self.image.url

        except:
            url = ''
        return url
