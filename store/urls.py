from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name="index"),

	path('store', views.store, name="store"),

	path('cart/', views.cart, name="cart"),

	path('checkout/', views.checkout, name="checkout"),

	path('login/', views.login, name="login"),

	path('registro/', views.registro, name="registro"),

	path('update_item/', views.updateItem, name="update_item"),

	path('process_order/', views.processOrder, name="process_order"),

	path('login/', views.login_view, name="login_view"),

]