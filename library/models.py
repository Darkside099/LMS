from django.db import models


class User(models.Model):
    user_ID = models.CharField(max_length=8, unique=True, primary_key=True)
    user_name = models.CharField(max_length=100)
    user_phone = models.CharField(max_length=10, unique=True)
    user_address = models.CharField(max_length=250)
    user_dob = models.DateField()


class Item(models.Model):
    BOOK = "Book"
    AUDIO = "Audio"
    VIDEO = "Video"
    REFERENCE = "Reference"
    ITEM_TYPE_CHOICES = [
        (BOOK, "Book"),
        (AUDIO, "Audio"),
        (VIDEO, "Video"),
        (REFERENCE, "Reference"),
    ]

    item_ID = models.AutoField(primary_key=True, unique=True)
    item_name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=9, choices=ITEM_TYPE_CHOICES)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_stock = models.IntegerField()
    item_request = models.BooleanField(default=False)
    best_seller = models.BooleanField(default=False)


class Service(models.Model):
    service_ID = models.AutoField(primary_key=True, unique=True)
    user_ID = models.CharField(max_length=8)
    item_ID = models.CharField(max_length=100)
    issued_date = models.DateField()
    return_date = models.DateField()
    fine = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    renewed = models.BooleanField(default=False)
