from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ProjectForm
from .models import *
import os
from django.http import FileResponse
from django.core.files.storage import default_storage
import yt_dlp
from django.conf import settings
from datetime import date
from mcstatus import JavaServer
from mcipc.rcon.je import Biome, Client 

def get_projects_stats():
    Projects = Project.objects.all()
    numberProject =  Projects.filter(priority__gt=-1).count()
    finishedProjects = Projects.filter(priority=0).count()
    unfinishedProjects = Projects.filter(priority__gt=0).count()
    ImportantProject = None
    if Projects.filter(priority=1):
        ImportantProject = Projects.get(priority=1)
    lessImportantProject = 0
    for item in Projects:
        if item.priority > lessImportantProject:
            lessImportantProject = item.priority
    return numberProject, finishedProjects, unfinishedProjects, Projects, ImportantProject, lessImportantProject

def Espace_CT_index(request):
    if request.user.is_authenticated:
        numberProject, finishedProjects, unfinishedProjects, Projects, ImportantProject, lessImportantProject = get_projects_stats()
        return render(request, "Espace_CT/index.html", {
            "important": ImportantProject, 
            "numberProjects": numberProject, 
            "finishedProjects": finishedProjects, 
            "unfinishedProjects": unfinishedProjects,
            })
    else:
        return redirect('/auth')

def About(request):
    if request.user.is_authenticated:
        return render(request, "Espace_CT/A-propos.html")
    else:
        return redirect('/auth')

def Projects(request):
    if request.user.is_authenticated:
        errors = None
        numberProject, finishedProjects, unfinishedProjects, Projects, ImportantProject, lessImportantProject = get_projects_stats()
        if request.method == "POST":
            if "nvProject" in request.POST:
                form = ProjectForm(request.POST, request.FILES)
                if form.is_valid():
                    priorityForm = form.cleaned_data['priority']
                    if not priorityForm <= (lessImportantProject + 1):
                        errors = "Vous avez spécifié une priorité trop importante"
                        return redirect(reverse('Projects'), {"errors": errors})
                    if priorityForm < 0:
                        priorityForm = 0
                    title_form = form.cleaned_data['title']
                    if not Projects.filter(title=title_form):
                        for item in Projects:
                            if item.priority >= priorityForm and priorityForm != 0:
                                print(f"la priorité de {item} est plus grande ou égale que celle du form qui est à {priorityForm}, elle est à {item.priority}. Sa nouvelle priorité sera à {int(item.priority) + 1}")
                                item.priority += 1
                                item.save()
                        form.save()
                        return redirect(reverse('Projects'))
                else:
                    errors = form.errors
            else:
                form = ProjectForm()
            
            if "nvProjectIdea" in request.POST:
                form = ProjectForm(request.POST, request.FILES)
                if form.is_valid():
                    title_form = form.cleaned_data['title']
                    if not Projects.filter(title=title_form):
                        project = form.save(commit=False)
                        project.date = date.today()
                        project.save()
                        print(project.date)
                        return redirect(reverse('Projects'))
                else:
                    errors = form.errors
            else:
                form = ProjectForm()
        ProjectsUnFinished = Projects.filter(priority=0).order_by('-date')
        ProjectsFinished = Projects.filter(priority__gt=0).order_by('priority')
        ProjectsIdeas = Projects.filter(priority=-1).order_by('date')
        return render(request, "Espace_CT/Tous-les-projets.html", {
            "ProjectsF": ProjectsFinished,
            "ProjectsU": ProjectsUnFinished,
            "numberProjects": numberProject,
            "ProjectsIdeas": ProjectsIdeas,
            "finishedProjects": finishedProjects,
            "errors": errors,
            })
    else:
        return redirect('/auth')

def edit_project(request, item_title):
    if request.user.is_superuser:
        numberProject, finishedProjects, unfinishedProjects, Projects, ImportantProject, lessImportantProject = get_projects_stats()
        project_to_edit = Projects.get(title=item_title)
        if request.method == "POST":
            old_image = project_to_edit.images
            form = ProjectForm(request.POST, request.FILES, instance=project_to_edit)
            if form.is_valid():
                priorityForm = form.cleaned_data['priority']
                if not priorityForm <= lessImportantProject:
                    errors = "Vous avez spécifié une priorité trop importante"
                    return redirect(reverse('Projects'), {"errors": errors})
                if priorityForm < -1:
                    priorityForm = 0
                title_form = form.cleaned_data['title']
                description_form = form.cleaned_data['description']
                url_placeholder_form = form.cleaned_data['url_placeholder']
                url_form = form.cleaned_data['url']
                old_priority = Projects.get(title=title_form).priority
                date = form.cleaned_data['date']
                image_form = form.cleaned_data['images']
                if image_form != old_image:
                    print(f"/Users/comptepourjeux/Documents/Code/Projets_codes/chiroo.fr/chiroo/src/media/{old_image}")
                    try:
                        default_storage.delete(str(f"/Users/comptepourjeux/Documents/Code/Projets_codes/chiroo.fr/chiroo/src/media/{old_image}"))
                    except:
                        print("the delete did not work")
                else:
                    print(project_to_edit.images)
                    print(image_form)
                if date:
                    print(date)
                    project_to_edit.date = date
                    project_to_edit.save()
                else:
                    print("date = none")
                    project_to_edit.save(update_fields=['title', 'priority', 'description', 'url_placeholder', 'url'])
                Projects = Projects.order_by('-priority')
                print("-----------")
                print(f"item édité : {title_form}")
                print(f"priorité : {priorityForm}")
                for item in Projects:
                    if item != project_to_edit and item.priority != 0 and item.priority != -1 and old_priority != priorityForm and not Projects.filter(priority=priorityForm).count == 0:
                        print("-----------")
                        print(f"nous somme sur {item.title}")
                        print(f"sa priorité : {item.priority}")
                        print(f"dif item priority et old_priority {item.priority - old_priority}")
                        print(f"old priorité : {old_priority}")
                        if priorityForm == 0:
                            print("le projet édité est finit")
                            if item.priority >= old_priority:
                                item.priority -=1
                        elif old_priority == 0 or old_priority == -1:
                            print("le projet édité n'est plus finit")
                            if item.priority >= priorityForm:
                                item.priority += 1
                            elif item.priority < priorityForm:
                                print("projet à une priorité en dessous de celui qui vient d'arriver")
                                item.priority -= 1
                                print("Priorité décrémenté")
                            print(f"Sa nouvelle priorité est de {item.priority}")
                        elif item.priority > priorityForm:
                            print(f"Sa priorité est supérieur à celle du projet renseigné dans le form")
                            if old_priority > item.priority:
                                item.priority += 1 
                            print(f"Sa nouvelle priorité est de {item.priority}")
                        elif item.priority < priorityForm:
                            print(f"Sa priorité est inférieur à celle du projet renseigné dans le form")
                            if item.priority == 1:
                                pass
                            elif old_priority < item.priority:
                                item.priority -= 1
                                print("Priorité décrémenté")
                            print(f"Sa nouvelle priorité est de {item.priority}")
                        elif item.priority == priorityForm:
                            print(f"Sa priorité est égale à celle renseigné dans le form.")
                            if old_priority > priorityForm:
                                item.priority += 1
                                print("Priorité incrémenté")
                            elif old_priority < priorityForm:
                                item.priority -= 1
                                print("Priorité décrémenté")
                            print(f"Sa nouvelle priorité est de {item.priority}")
                        item.save()
                project_to_edit.title = title_form
                project_to_edit.priority = priorityForm
                project_to_edit.description = description_form
                project_to_edit.url_placeholder = url_placeholder_form
                project_to_edit.url = url_form
                project_to_edit.images = image_form
                if date:
                    print(date)
                    project_to_edit.date = date
                    project_to_edit.save()
                else:
                    print("date = none")
                    project_to_edit.save(update_fields=['title', 'priority', 'description', 'url_placeholder', 'url', 'images'])
                return redirect(reverse('Projects'))
            else:
                errors = form.errors
                print(f"was not valid, {errors.as_text()}")
        else:
            form = ProjectForm(instance=project_to_edit)

        return render(request, "Espace_CT/edit_project.html", {
            "form": form,
            "Project": project_to_edit,
        })
    else:
        return redirect('/auth')

def remove_project(request, item_title):
    numberProject, finishedProjects, unfinishedProjects, Projects, ImportantProject, lessImportantProject = get_projects_stats()
    if request.method == "POST" and request.user.is_authenticated:
        project_to_remove = Projects.get(title=item_title)
        print(project_to_remove)
        priority_project_to_remove = project_to_remove.priority
        if priority_project_to_remove >= 1:
            for item in Projects: 
                if item.priority >= priority_project_to_remove:
                    item.priority -= 1
                    item.save()
        image_project_to_remove = project_to_remove.images
        print(f"/Users/comptepourjeux/Documents/Code/Projets_codes/chiroo.fr/chiroo/src/media/{image_project_to_remove}")
        try:
            default_storage.delete(str(f"/Users/comptepourjeux/Documents/Code/Projets_codes/chiroo.fr/chiroo/src/media/{image_project_to_remove}"))
        except:
            print("the delete did not work")
        project_to_remove.delete()
        return redirect('Projects')

def counter(request):
    if request.user.is_authenticated:
        return render(request, "Espace_CT/compteur.html")
    else:
        return redirect('/auth')

def IMC(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            age = request.POST.get("age")
            taille = request.POST.get("taille")
            poids = request.POST.get("poids")
        else:
            return render(request, "Espace_CT/projet-calculer-IMC.html")
    else:
        return redirect('/auth')

def ytVideoImporter(request):
    if request.user.is_authenticated:
        context = {}
        if request.method == "POST":
            if "search" in request.POST:
                link = request.POST.get("link")
                try:
                    ydl_opts = {
                        'quiet': True,
                        'skip_download': True,
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info_dict = ydl.extract_info(link, download=False)
                    video_author = info_dict.get("uploader")
                    context = {
                        "video": info_dict,
                        "link": link,
                        "author": video_author,
                    }
                except Exception as e:
                    print(f"An error has occurred: {e}")
                    context = {
                        "error": "Problème de lien ou de connexion"
                    }
            elif "import" in request.POST:
                SAVE_PATH = os.path.join(settings.MEDIA_ROOT, 'videos_yt_imports')
                link = request.POST.get("link")
                try:
                    ydl_opts = {
                        'outtmpl': os.path.join(SAVE_PATH, '%(title)s.%(ext)s'),
                    }
                    if request.POST.get("options[]") == "video":
                        ydl_opts['format'] = 'bestvideo+bestaudio/best'
                    elif request.POST.get("options[]") == "audio":
                        ydl_opts['format'] = 'bestaudio/best'
                        ydl_opts['postprocessors'] = [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '256',
                        }]
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info_dict = ydl.extract_info(link, download=False)
                        filename = ydl.prepare_filename(info_dict)
                        # Correctly rename the file if it's audio
                        if request.POST.get("options[]") == "audio":
                            filename = filename.replace(".webm", ".mp3").replace(".m4a", ".mp3")
                        download = ydl.download([link])
                        download_filename = os.path.basename(filename)
                        file_path = os.path.join(SAVE_PATH, download_filename)
                    
                    # Ensure we open the correct file type
                    response = FileResponse(open(file_path, 'rb'), as_attachment=True)
                    return response

                except Exception as e:
                    print(f"An error has occurred: {e}")
                    context = {
                        "error": "Erreur lors du téléchargement"
                    }
        
        return render(request, "Espace_CT/yt_import.html", context)
    else:
        return redirect('/auth')

def minecraftServer(request):
    if request.user.is_superuser:
        MCServers = MinecraftServer.objects.all()
        if request.method == "POST":
            if "shutdown" in request.POST:
                ServerName = request.POST.get("ServerName")
                server = MCServers.get(name=ServerName)
                ipServer = server.ip
                portServer = server.rcon_port
                ipPortServer = str(ipServer) + ":" + str(portServer)
                print(ipPortServer)
                print(server.password)
                with Client(ipServer, int(portServer), passwd=server.password) as client:
                    client.stop()
        for server in MCServers:
            server_ip_port = str(server.ip) + ":" + str(server.server_port)
            MCserver = JavaServer.lookup(server_ip_port)
            try:
                server.status = MCserver.status()
                server.on = True
                server.status.latency = round(server.status.latency, 2)
            except:
                server.status = False
                server.on = False
        context = {
            "servers": MCServers
        }
        return render(request, "Espace_CT/minecraft-server.html", context)
    else:
        return redirect('/')