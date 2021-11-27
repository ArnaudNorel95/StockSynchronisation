from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from stock.models import Shop, User, Stock, Product, Synchronisation
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
import pytz
from datetime import datetime
from django.forms.models import model_to_dict

def get_stock(product=0):
    context = {"stock":[]}
    my_complete_stock = Stock.objects.all()

    if(product != 0): 
        my_complete_stock = my_complete_stock.filter(product=product)

    index = 0
    for element in my_complete_stock:
        context["stock"].append(model_to_dict(element))
        context["stock"][index]["synchronisation"] = model_to_dict(element.last_synchronisation)
        index+=1
    
    return context

class CreateUserView(APIView):
    def post(self, request, *args, **kwargs):

        newUser = User(
            username    = request.data['username'],
            email       = request.data['email'],
            full_name   = request.data['full_name']
        )

        newUser.password = make_password(request.data['password'])
        newUser.save()

        return JsonResponse({"success": "user "+str(newUser.id)})

class HomeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        userConnected = request.user

        return JsonResponse({"welcome":userConnected.username})

class CreateStockView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user_connected = request.user
        context = {
            "message":"",
            "stock":[]
        }

        stock = []

        utc = pytz.UTC 
        date_sent = datetime.strptime(request.data['date_sent'], '%Y-%m-%d %H:%M:%S')
        date_sent = date_sent.astimezone(utc)

        new_synchronisation = Synchronisation(
            date_sent       = date_sent,
            date_effective  = datetime.now(),
            user            = user_connected
        )
        new_synchronisation.save()

        for element in request.data['stock']:
            try:
                my_product = Product.objects.get(gtin=element['GTIN'])

            except:
                return Response(
                    {
                        "Error": "GTIN doesn't exist in our stock"
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            try:
                # PRODUCT ALREADY EXIST IN STOCK
                new_stock = Stock.objects.get(product = my_product)
                print("produit existant dans le stock")

                # OVERRIDE STOCK IF OFFLINE DATE_SENT WAS AFTER LAST SYNCHRONISATION
                if(new_stock.last_synchronisation.date_effective < new_synchronisation.date_sent):
                    print("OVERRIDE STOCK")
                    new_stock.shortest_expiry_date   = element['sed']
                    new_stock.shortest_headcount     = element['quantity_sed']
                    new_stock.total_headcount        = element['quantity_total']
                    new_stock.last_synchronisation   = new_synchronisation
                    new_stock.save()

                # OTHERWISE DOESNT OVERRIDE STOCK
                else:
                    print("DOESNT OVERRIDE STOCK")

            except:
                new_stock = Stock(
                    product              = my_product,
                    shortest_expiry_date = element['sed'],
                    shortest_headcount   = element['quantity_sed'],
                    total_headcount      = element['quantity_total'],                    
                    last_synchronisation = new_synchronisation
                )
                new_stock.save()
                print("produit pas dans le stock on le crée")
            
        context["message"] = "New stock created with success"

        context["stock"] = get_stock()["stock"]

        return JsonResponse(context)


class GetStockView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        context = get_stock()

        if(request.GET.get('product')):
            context = get_stock(request.GET.get('product'))

        return JsonResponse(context)