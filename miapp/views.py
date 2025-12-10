from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Practica, Cancion

# Vista principal (1-vista.html)
def primeravista(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    usuario_id = request.session['usuario_id']
    
    # Obtener canciones del usuario actual
    canciones_usuario = Cancion.objects.filter(usuario_id=usuario_id)
    
    context = {
        'user': {
            'username': request.session.get('usuario_nombre', 'Invitado')
        },
        'playlists': [], 
        'artistas': [],
        'canciones': canciones_usuario,
    }
    return render(request, '1-vista.html', context)

# Vista de gestión (2-vista.html) - MODIFICADA CON FORMULARIOS SIMPLES
def segundavista(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    usuario_id = request.session['usuario_id']
    usuario = Practica.objects.get(id=usuario_id)
    
    # Obtener canciones del usuario
    canciones = Cancion.objects.filter(usuario=usuario)
    
    if request.method == "POST":
        # Verificar qué acción se está realizando
        if 'agregar' in request.POST:
            # Agregar nueva canción
            titulo = request.POST.get('titulo')
            artista = request.POST.get('artista')
            
            if titulo and artista:
                Cancion.objects.create(
                    titulo=titulo,
                    artista=artista,
                    usuario=usuario
                )
        
        elif 'editar' in request.POST:
            # Editar canción existente
            cancion_id = request.POST.get('cancion_id')
            titulo = request.POST.get('titulo')
            artista = request.POST.get('artista')
            
            if cancion_id and titulo and artista:
                cancion = get_object_or_404(Cancion, id=cancion_id, usuario=usuario)
                cancion.titulo = titulo
                cancion.artista = artista
                cancion.save()
        
        elif 'eliminar' in request.POST:
            # Eliminar canción
            cancion_id = request.POST.get('cancion_id')
            if cancion_id:
                cancion = get_object_or_404(Cancion, id=cancion_id, usuario=usuario)
                cancion.delete()
        
        # Redirigir a la misma página para recargar
        return redirect('gestion')
    
    # GET request - mostrar página con formulario vacío
    context = {
        'canciones': canciones,
        'usuario': usuario,
    }
    return render(request, '2-vista.html', context)

# Vista para editar canción (opcional, separada)
def editar_cancion(request, id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    usuario_id = request.session['usuario_id']
    usuario = Practica.objects.get(id=usuario_id)
    cancion = get_object_or_404(Cancion, id=id, usuario=usuario)
    
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        artista = request.POST.get('artista')
        
        if titulo and artista:
            cancion.titulo = titulo
            cancion.artista = artista
            cancion.save()
            return redirect('gestion')
    
    context = {
        'cancion': cancion,
    }
    return render(request, 'editar_cancion.html', context)

# ... (el resto de las funciones se mantienen igual)
def formulario(request):
    if request.method == "POST":
        usern = request.POST.get("username")
        passw1 = request.POST.get("password1")
        passw2 = request.POST.get("password2")

        if Practica.objects.filter(username=usern).exists():
            info = {
                'infosms': "El nombre de usuario ya existe",
                'infosms2': "Por favor elige otro nombre de usuario"
            }
            return render(request, "formulario.html", info)
        
        if passw1 == passw2:
            Practica.objects.create(
                username=usern,
                password=passw2
            )
            return redirect("login")
        else:
            info = {
                'infosms': "Las contraseñas no coinciden",
                'infosms2': "Verifica tu contraseña"
            }
            return render(request, "formulario.html", info)
    
    return render(request, "formulario.html")

def login(request):
    if 'usuario_id' in request.session:
        return redirect('principal')
    
    if request.method == "POST":
        usern = request.POST.get("username")
        passw = request.POST.get("password1")
        
        try:
            usuario = Practica.objects.get(username=usern)
            
            if usuario.password == passw:
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nombre'] = usuario.username
                return redirect("principal")
            else:
                info = {
                    'infosms': "Contraseña incorrecta",
                    'infosms2': "Intenta de nuevo"
                }
        except Practica.DoesNotExist:
            info = {
                'infosms': "Usuario no encontrado",
                'infosms2': "Regístrate primero"
            }
        
        return render(request, "login.html", info)
    
    return render(request, 'login.html')

def logout(request):
    request.session.flush()
    return redirect('login')

def modificar_menu(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
        
    return HttpResponse("Esta es la página de modificación. (Pendiente de implementación)")
