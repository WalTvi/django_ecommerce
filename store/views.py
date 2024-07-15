from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from .forms import ProductForm, CustomerForm

def index(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'store/index.html', context)

	
def login(request):
	context = {}
	return render(request, 'store/login.html',context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZW50YXMiOiJ0b2tlbl92ZW50YXMifQ._EO1cFamwcGzpJ47DWAHcRB2JqndgLgZOccsGVUukC0'
        
        # Datos para la solicitud POST
        payload = json.dumps({
            "username": username,
            "password": password,
            "token": token
        })
        
        headers = {
            'Content-Type': 'application/json'
        }

        # URL del endpoint de validación
        url = 'https://qic534o8o0.execute-api.us-east-1.amazonaws.com/validacionUsuarios/'
        
        # Realizar la solicitud POST
        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('valid', False):
                # Autenticar al usuario en Django
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Inicio de sesión exitoso')
                    return redirect('index')
                else:
                    messages.error(request, 'No se pudo autenticar al usuario en el sistema local')
            else:
                messages.error(request, 'Credenciales inválidas')
        else:
            messages.error(request, 'Error en la validación de usuario')
        
    return render(request, 'store/index.html')

def registro(request):
    data= {'form': CustomerForm()}

    if request.method =='POST':
        formulario=CustomerForm(data=request.POST,files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"]= "guardado corretamente"

        else:
            data['form']=formulario
    return render( request,'store/registro.html',data)


def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)




def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)