from django.db import models

class Server(models.Model):
    name = models.CharField(max_length=100)
    ip = models.CharField(max_length=300)
    username = models.CharField(max_length=200, default='root')
    #ssh-keygen -t rsa -b 4096 -C "your_email@example.com" pour ne pas avoir à utiliser le mdp
    #ssh-copy-id user@server_address faire ca pour chaque servers
    
    def __str__(self):
        return self.name
