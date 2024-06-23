import subprocess
from django.shortcuts import redirect, render
from .models import Server

def AreTheServersOk_index(request):
    if request.user.is_superuser:
        queryDone = False
        context = {
            'queryDone': queryDone,
        }
        server_info = None

        if request.method == "POST":
            if "query" in request.POST:
                servers = Server.objects.all()
                queryDone = True
                context = {
                    'servers': servers,
                    'server_info': server_info,
                    'queryDone': queryDone,
                }

        return render(request, "AreTheServersOk/index.html", context)
    else:
        return redirect('/')