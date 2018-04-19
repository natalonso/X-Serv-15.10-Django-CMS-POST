from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from .models import Page

formulario = """
<form action="" method="POST">
    Name: <input type="text" name="name"><br>
    Page: <input type="text" name="page"><br>
    <input type="submit" value="Enviar">
</form>
"""


@csrf_exempt
def home_anotated(request): #PAGINA PRINCIPAL

    if request.method == 'POST':

        newpage= Page(name=request.POST['name'], page=request.POST['page'])
        newpage.save()

    if request.user.is_authenticated():
        logged = 'Logged in as: ' + request.user.username + "<br><a href='/logout'>Logout</a><br><br>"
        permiso = True
    else:
        logged = "Not logged in. <br><a href='/login'>Login</a><br><br>"
        permiso = False

    lista = Page.objects.all()
    salida = "<h4>" + logged + "</h4><br>"
    salida += "<h1>Bienvenido al servidor CMS, estas son las paginas disponibles hasta el momento: </h1><br>"
    salida += "<ul>"
    for pagina in lista:
        salida += '<li><h3><a href=' + str(pagina.name) + '>' + pagina.name + '</a></h3>'
    salida += "</ul>"

    if permiso == True: #estas logeado
        salida += formulario
        template = get_template("terrafirma/index.html")
        c =({'title' : "SERVIDOR CMS", 'contenido' : salida})
        return HttpResponse(template.render(c))
    else: #no estas logeado
        template = get_template("terrafirma/index.html")
        c =({'title' : "SERVIDOR CMS", 'contenido' : salida})
        return HttpResponse(template.render(c))


@csrf_exempt
def home(request): #PAGINA PRINCIPAL

    if request.method == 'POST':
        newpage= Page(name=request.POST['name'], page=request.POST['page'])
        newpage.save()

    if request.user.is_authenticated():
        logged = 'Logged in as: ' + request.user.username
        permiso = True
    else:
        logged = 'Not logged in.'
        permiso = False

    lista = Page.objects.all()
    salida = "Bienvenido al servidor CMS, estas son las paginas disponibles hasta el momento: "
    salida += "<ul>"
    for pagina in lista:
        salida += '<li><a href=' + str(pagina.name) + '>' + pagina.name + '</a>'
    salida += "</ul>"

    if permiso == True: #estas logeado
        return HttpResponse(logged + '<br><a href= "/logout">Logout</a><br><br>' + salida + formulario )
    else: #no estas logeado
        return HttpResponse(logged + '<br><a href= "/login">Login</a><br><br>' + salida)

@csrf_exempt
def pagina(request, pagina):

    lista = Page.objects.all()
    for elemento in lista:
        if elemento.name == pagina:
            salida = elemento.page
            break
        else:
            salida = None
    if salida == None:
        return HttpResponse('Lo sentimos. La pagina no esta en la base de datos por el momento.')
    else:
        return HttpResponse(salida)

@csrf_exempt
def edit(request, nombre):

    if request.method == 'POST':

        if request.user.is_authenticated():
            logged = 'Logged in as: ' + request.user.username
            permiso = True
        else:
            logged = 'Not logged in.'
            permiso = False

        lista = Page.objects.all()
        for elemento in lista:
            if elemento.name == nombre:
                salida = elemento.page
                break
            else:
                salida = None
        if salida == None:
            if permiso == True:
                newpage= Page(name=nombre, page=request.POST['page'])
                newpage.save()
                return HttpResponse('La pagina no estaba en nuestra BD, ha sido añadida.' + "<form action='' method='POST'>Nuevo contenido:<br><input type='text' name='page' placeholder='" + str(elemento.page) + "'><br><input type='submit' value='Enviar'></form>")
            else:
                return HttpResponse("No estás autenticado.<br><a href='/login'>Login</a><br><br>")
        else:
            if permiso == True:
                elemento.page = request.POST['page']
                elemento.save()
                return HttpResponse("ACTUALIZADO" + "<form action='' method='POST'>Nuevo contenido:<br><input type='text' name='page' placeholder='" + str(elemento.page) + "'><br><input type='submit' value='Enviar'></form>")
            else:
                return HttpResponse("No estas autenticado.<br><a href='/login'>Login</a><br><br>")
    else:
        lista = Page.objects.all()
        for elemento in lista:
            if elemento.name == pagina:
                salida = elemento.page
                break
            else:
                salida = None
        if salida == None:
            return HttpResponse("<form action='' method='POST'>Nuevo contenido:<br><input type='text' name='page'><br><input type='submit' value='Enviar'></form>")
        else:
            return HttpResponse("<form action='' method='POST'>Nuevo contenido:<br><input type='text' name='page' placeholder='" + str(elemento.page) + "'><br><input type='submit' value='Enviar'></form>")
