from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Practica

# Vistas existentes (sin cambios)
def saludo(request):
    return HttpResponse("Hola Inmundo")

def pestana(request):
    return HttpResponse("ñ")

def cachorro(request):
    return HttpResponse("sin H")

def primeravista(request):
    return render(request, '1-vista.html')

def segundavista(request):
    return render(request, '2-vista.html')

# miapp/views.py - Función formulario ACTUALIZADA
def formulario(request):
    if request.method == "POST":
        usern = request.POST.get("username", "").strip()
        passw1 = request.POST.get("password1", "").strip()
        passw2 = request.POST.get("password2", "").strip()
        image_url = request.POST.get("image_url", "").strip()  # NUEVO CAMPO
        
        # Validaciones básicas
        if not all([usern, passw1, passw2, image_url]):  # Ahora image_url es requerido
            info = {
                'infosms': "Todos los campos son obligatorios",
                'infosms2': "Incluye una URL de imagen"
            }
            return render(request, "formulario.html", info)
        
        # Validar formato de URL
        if not image_url.startswith(('http://', 'https://')):
            info = {
                'infosms': "URL de imagen inválida",
                'infosms2': "Debe comenzar con http:// o https://"
            }
            return render(request, "formulario.html", info)
        
        # Validar si usuario ya existe
        if Practica.objects.filter(username=usern).exists():
            info = {
                'infosms': "El nombre de usuario ya existe",
                'infosms2': "Por favor elige otro nombre de usuario"
            }
            return render(request, "formulario.html", info)
        
        # Validar contraseñas
        if passw1 != passw2:
            info = {
                'infosms': "Las contraseñas no coinciden",
                'infosms2': "Verifica tu contraseña"
            }
            return render(request, "formulario.html", info)
        
        # Validar longitud mínima de contraseña
        if len(passw1) < 6:
            info = {
                'infosms': "Contraseña muy corta",
                'infosms2': "La contraseña debe tener al menos 6 caracteres"
            }
            return render(request, "formulario.html", info)
        
        try:
            # Crear usuario CON image_url (Punto 3)
            usuario = Practica.objects.create(
                username=usern,
                password=passw2,
                image_url=image_url  # AHORA SÍ incluimos la imagen
            )
            
            # Redirigir al login automáticamente
            return redirect("login")
            
        except Exception as e:
            info = {
                'infosms': "Error al crear usuario",
                'infosms2': str(e)
            }
            return render(request, "formulario.html", info)
    
    return render(request, "formulario.html")

# Vista de login (MODIFICADA para autenticación real)
def login(request):
    if request.method == "POST":
        usern = request.POST.get("username")
        passw = request.POST.get("password1")  # Cambiado de password2 a password1
        
        try:
            # Buscar usuario en la base de datos
            usuario = Practica.objects.get(username=usern)
            
            # Verificar contraseña (en producción usaría hash)
            if usuario.password == passw:
                # Guardar usuario en sesión
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nombre'] = usuario.username
                return redirect("usuarios_registrados")  # Redirigir a vista de usuarios
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

# NUEVA VISTA: Ver todos los usuarios registrados
def usuarios_registrados(request):
    # Verificar si el usuario ha iniciado sesión
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    # Obtener todos los usuarios
    usuarios = Practica.objects.all()
    
    # Información del usuario actual
    usuario_actual = {
        'id': request.session.get('usuario_id'),
        'nombre': request.session.get('usuario_nombre')
    }
    
    return render(request, 'usuarios.html', {
        'usuarios': usuarios,
        'usuario_actual': usuario_actual
    })

# NUEVA VISTA: Eliminar usuario
def eliminar_usuario(request, id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    usuario = get_object_or_404(Practica, id=id)
    usuario.delete()
    
    return redirect('usuarios_registrados')

# miapp/views.py - Función actualizar_usuario MEJORADA
def actualizar_usuario(request, id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    usuario = get_object_or_404(Practica, id=id)
    
    if request.method == "POST":
        # Obtener datos del formulario
        nuevo_username = request.POST.get("username", "").strip()
        nueva_password = request.POST.get("password", "").strip()
        nueva_image_url = request.POST.get("image_url", "").strip()
        
        # Validar campos obligatorios
        if not nuevo_username or not nueva_image_url:
            return render(request, 'actualizar_usuario.html', {
                'usuario': usuario,
                'infosms': "Campos incompletos",
                'infosms2': "Usuario e imagen son obligatorios"
            })
        
        # Validar formato de URL
        if not nueva_image_url.startswith(('http://', 'https://')):
            return render(request, 'actualizar_usuario.html', {
                'usuario': usuario,
                'infosms': "URL de imagen inválida",
                'infosms2': "Debe comenzar con http:// o https://"
            })
        
        # Validar si el nuevo username ya existe (excepto para el mismo usuario)
        if Practica.objects.filter(username=nuevo_username).exclude(id=id).exists():
            return render(request, 'actualizar_usuario.html', {
                'usuario': usuario,
                'infosms': "Nombre de usuario no disponible",
                'infosms2': "Elige otro nombre de usuario"
            })
        
        # Actualizar datos
        usuario.username = nuevo_username
        if nueva_password:  # Solo actualizar si se proporcionó nueva contraseña
            usuario.password = nueva_password
        usuario.image_url = nueva_image_url
        usuario.save()
        
        # Actualizar sesión si el usuario actualizó su propio perfil
        if request.session.get('usuario_id') == id:
            request.session['usuario_nombre'] = nuevo_username
        
        return redirect('usuarios_registrados')
    
    return render(request, 'actualizar_usuario.html', {'usuario': usuario})

# NUEVA VISTA: Logout
def logout(request):
    request.session.flush()
    return redirect('login')