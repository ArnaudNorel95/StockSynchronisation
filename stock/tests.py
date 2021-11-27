from django.http import response
from django.test import TestCase
import unittest
from .models import User, Shop, Stock, Synchronisation, Product

class CreateUser(unittest.TestCase):
    def setUp(self):
        self.new_user_x = User.objects.create(
            username    = "user_X",
            password    = "codabene",
            email       = "arnaudnorel@yahoo.fr",
            full_name   = "Arnaud Test X"
        )

    def test_user_x_infos(self):
        self.assertIsNotNone(self.new_user_x.username)
        self.assertIsNotNone(self.new_user_x.password)
        self.assertIsNotNone(self.new_user_x.email)
        self.assertIsNotNone(self.new_user_x.full_name)
        self.assertIsNotNone(self.new_user_x.shop)

    def tearDown(self):
        self.new_user_x.delete()


class CreateProduct(unittest.TestCase):
    def setUp(self):
        self.new_product_a = Product.objects.create(
            name    = "shampoo",
            gtin    = 1123360005,
            price   = 3.55
        ) 

    def test_product_a_infos(self):
        self.assertIsNotNone(self.new_product_a.name)
        self.assertIsNotNone(self.new_product_a.gtin)
        self.assertIsNotNone(self.new_product_a.price)
        self.assertIsNotNone(self.new_product_a.shop)
    
    def tearDown(self):
        self.new_product_a.delete()


class CreateStock(unittest.TestCase):
    def setUp(self):
        self.new_user_x = User.objects.create(
            username    = "user_X",
            password    = "codabene",
            email       = "arnaudnorel@yahoo.fr",
            full_name   = "Arnaud Test X"
        )

        self.new_product_a = Product.objects.create(
            name    = "shampoo",
            gtin    = 1123360005,
            price   = 3.55
        )

        self.first_sync_x = Synchronisation.objects.create(
            user            = self.new_user_x,
            date_sent       = "2021-11-27 10:30:00",
            date_effective  = "2021-11-29 10:30:00"
        )
        self.stock_x = Stock.objects.create(
            product                 = self.new_product_a,
            shortest_expiry_date    = "2021-11-30",
            shortest_headcount      = 100,
            total_headcount         = 200,
            last_synchronisation    = self.first_sync_x
        )

    def test_sync_infos(self):
        self.assertIsNotNone(self.first_sync_x.user)
        self.assertIsNotNone(self.first_sync_x.date_sent)
        self.assertIsNotNone(self.first_sync_x.date_effective)
    
    def test_shop_infos(self):
        self.assertIsNotNone(self.stock_x.product)
        self.assertIsNotNone(self.stock_x.shortest_expiry_date)
        self.assertIsNotNone(self.stock_x.shortest_headcount)
        self.assertIsNotNone(self.stock_x.total_headcount)
        self.assertIsNotNone(self.stock_x.last_synchronisation)

    def tearDown(self):
        self.new_user_x.delete()
        self.new_product_a.delete()
        self.first_sync_x.delete()
        self.stock_x.delete()