from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login #se utiliza para iniciar la sesion
from django.contrib.auth import logout #se utiliza para cerrar la sesion
from django.contrib import messages#para enviar mensajes desde el servidor al cliente

from .forms import RegisterForm

#from django.contrib.auth.models import User #importamos el modelo de user de django
from users.models import User

def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.user.is_authenticated: #si el usuario ya está autenticado lo redirigimos al index
        return redirect('index')
    
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)#buscara en la base de datos credenciales que coincidan con los valores
        if user:
            login(request, user) #para iniciar la sesion le pasamos a la funcion la petición y el 
            messages.success(request, 'Bienvenido {}'.format(user.username))
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña no validos')
        
    return render(request, 'users/login.html')

def logout_view(request):
    logout (request)
    messages.success(request,'Sesión cerrada exitosamente')
    return redirect('login')

def register(request):
    
    if request.user.is_authenticated: #si el usuario ya está autenticado lo redirigimos al index
        return redirect('index')
    
    form = RegisterForm(request.POST or None) #si la peticion es por metodo post entonces genera un formulario con los datos ingresados, sino sera un formulario con los campos vacios
    
    #obtener informacion a partir de un formulario basado en clases
    if request.method == 'POST' and form.is_valid():#is_valid permite saber si el formulario es valido o no
        user = form.save()
        
        if user:
            login(request,user)#generamos la sesion
            messages.success(request,'Usuario creado exitosamente')
            return redirect('index')
        
    return render(request, 'users/register.html',{
        'form': form #le pasamos el form definido en forms como registerform al template register.html
    })