"""
Definition of views.
"""
from app.models import Pelicula, Critico
from django.http import HttpRequest
from datetime import datetime
from django.template import RequestContext
from app.forms import RegistroForm #formulario de registro creado en app/forms.py
from django.contrib.auth import authenticate, login as auth_login, logout as django_logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
#"from django.core.urlresolvers import reverse
from django.template import RequestContext, Context, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import Form
from app.forms import PeliculaForm
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Autor',
            'message':'',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
def login(request):  
	#Si ya ha realizado el login
    if request.user.is_authenticated():
        return render(request, 'app/index.html')
	#No esta logueado, se le pide que haga login
    if request.method == "GET":
        return render(request, 'app/login.html')	
	#Procesar la peticion de login
    if request.method == "POST": #""POST":
        error = False
        user = authenticate(username=request.POST['username'], password=request.POST['pass'])
        if user is not None:
            auth_login(request, user)
            return render(request, 'app/index.html')
        else: #Credenciales incorrectas
            error = True #Se indica al formulario que las credenciales son incorrectas
            return render(request, 'app/login.html', {'error': error})

def registro(request):
	#Si ya ha realizado el login
    if request.user.is_authenticated:
        return render(request, '/index.html')
	#GET se le muestra el formulario de registro
    if request.method == "GET":
        form = RegistroForm()
        return render(request, 'app/registro.html',{'form': form})
	#POST procesar peticion de registro
    if request.method == "POST":
        error = False
        form = RegistroForm(request.POST)
        if form.is_valid(): #El formulario enviado es valido
            if request.POST['pass1'] == request.POST['pass2']:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['pass1'])
                user.save()
                #se redirecciona a la pagina de login
                return HttpResponseRedirect('../login')
            else:
                error = True #Contraseñas no coinciden, se mostrara el error en el formulario de registro
                return render(request, 'app/registro.html', {'form': form, 'error': error})
        else: #Formulario no es valido
            return render(request, 'app/registro.html', {'form': form})

def peliculas(request):
	#Si el usuario no ha realizado el login ...
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/login')
	#Se obtienen y muestran las preguntas ordenadas por numero de votos, de mayor a menor
	else:
		film_lista = Pelicula.objects.all().order_by('-votos')
		paginator = Paginator(film_lista, 4) #Se indica que se mostraran 4 peliculas por pagina
		page = request.GET.get('page')
		try:
			pelis = paginator.page(page)
		except PageNotAnInteger:
			#Se muestra la primera pagina
			pelis = paginator.page(1)
		except EmptyPage:
			#Si esta fuera del rango se muestra la ultima
			pelis = paginator.page(paginator.num_pages)
		return render(request, 'app/peliculas.html', {'pelis': pelis})

def generos(request):
    return render(request, 'app/genero.html')
    
def voto(request):
    return render(request, 'app/voto.html')
    

def new_pelicula(request):
    if not request.user.is_authenticated:
        return render(request, 'app/index.html')

    if request.method == "GET":
        form = PeliculaForm()
        return render(request, 'app/new_pelicula.html',{'form': form})

    if request.method == "POST":
        error = False
        form = PeliculaForm(request.POST)
        if form.is_valid():
            titulo = request.POST['titulo']
            direccion = request.POST['direccion']
            anio = request.POST['anio']
            genero = request.POST['genero']
            sinopsis = request.POST['sinopsis']
            votos = request.POST['votos']
            pelicula, created = Pelicula.objects.get_or_create(titulo=titulo, direccion=direccion, anio=anio, 
                                                               genero=genero, sinopsis=sinopsis, votos=votos)
            if created:
                return HttpResponseRedirect('../peliculas')
            else:
                error = True
                return render(request, 'app/new_pelicula.html', {'form': form, 'error': error}) 
        else:
            return render(request, 'app/new_pelicula.html', {'form': form})