import django
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

def login_user(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return render(request, "accounts/login.html", {'error': "Le nom d'utilisateur ou le mot de passe est incorrect."})
        else:
            return render(request, "accounts/login.html")
    else:
        return redirect('/')

def user(request):
    if request.user.is_authenticated:
        return render(request, "accounts/user.html", context= {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        })
    else:
        return redirect('login')

def logout_user(request):
    logout(request)
    return redirect('login')

def change_pwd(request):
    if request.method == "POST":
        password1 = request.POST["password"]
        password2 = request.POST["password2"]
        if password1 == password2:
            u = User.objects.get(username=request.user.username)
            u.set_password(password2)
            u.save()
            return redirect('login')
        else:
            return render(request, "accounts/change_pwd.html", {'error': "Les mots de passes ne correspondent pas."})

    else:
        return render(request, "accounts/change_pwd.html")

def sign_up(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first-name"]
        last_name = request.POST["last-name"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if User.objects.filter(username=username).exists():
            return render(request, "accounts/sign_up.html", {'error':"Ce nom d'utilisateur est déjà pris."})
        if password1 == password2:
                user = User.objects.create_user(username, email, password2)
                user.first_name = first_name
                user.last_name = last_name
                user.is_active = False
                user.save()
                signup_url = request.build_absolute_uri(reverse('signup_request', args=[username]))
                subject = 'Demande de création de compte'
                from_email = 'contact@tao-lamoureux.com'
                to = ["contact@tao-lamoureux.com"]
                html_content = render_to_string('accounts/emails/requestSignUp.html', {
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'url': signup_url,
                })
                text_content = 'Demande de création de compte'
                email = EmailMultiAlternatives(subject, text_content, from_email, to)
                email.attach_alternative(html_content, "text/html")
                email.send()
                messages.success(request, "Votre demande de création de compte sur tao-lamoureux.com a bien été prise en compte. L'administrateur devrait accepter votre demande. À très bientôt !")
                login(request, user)
                return redirect(reverse('login'))
        
        else:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, "accounts/sign_up.html", {'error':"Les mots de passe ne correspondent pas."})
    else:
        return render(request, "accounts/sign_up.html")

def redirect_auth(request):
    if request.user.is_authenticated:
        return redirect('user')
    else:
        return redirect('login')

def signup_request(request, username):
    if request.user.is_superuser:
        try:
            user = get_object_or_404(User, username=username)
        except:
            return redirect('index')
        if user.is_active:
            return redirect('index')
        else:
            if request.method == "POST":
                if "accept" in request.POST:
                    subject = 'Confirmation de création de votre compte'
                    from_email = 'contact@tao-lamoureux.com'
                    to = [user.email]
                    html_content = render_to_string('accounts/emails/AcceptedAccount.html', {
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                    })
                    text_content = 'Acceptation de création de compte'
                    email = EmailMultiAlternatives(subject, text_content, from_email, to)
                    email.attach_alternative(html_content, "text/html")
                    try:
                        email.send()
                        user.is_active = True
                        user.save()
                    except:
                        user.delete()
                    return redirect('index')
                elif "refuse" in request.POST:
                    subject = 'Erreur de création de votre compte'
                    from_email = 'contact@tao-lamoureux.com'
                    to = [user.email]
                    html_content = render_to_string('accounts/emails/AcceptedAccount.html', {
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'refus':"refus",
                    })
                    text_content = 'Refus de création de compte'
                    email = EmailMultiAlternatives(subject, text_content, from_email, to)
                    email.attach_alternative(html_content, "text/html")
                    try:
                        email.send()
                    except:
                        pass
                    user.delete()
                    return redirect('index')
            else:
                return render(request, "accounts/signup_request.html", {'user': user})
    else:
        return redirect('index')