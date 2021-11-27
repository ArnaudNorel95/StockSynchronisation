from django.urls import path
from stock.views import HomeView, CreateUserView, CreateStockView, GetStockView

app_name = 'stock'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('create_stock/', CreateStockView.as_view(), name='create_stock'),
    path('get_stock/', GetStockView.as_view(), name='get_stock')
]