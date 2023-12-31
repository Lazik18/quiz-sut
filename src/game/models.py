from django.db import models
from django.conf import settings
from quiz.models import Module
import uuid
import random
import string

# Create your models here.

def generate_code(length=5, attempts=10):
    characters = string.ascii_uppercase + string.digits
    for i in range(attempts):
        code = ''.join(random.choices(characters, k=length))
        if not Lobby.objects.filter(code=code).exists():
            return code
    raise Exception(f"Could not generate a unique code within the attempts ({attempts}) limit.")



class Lobby(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    secret = models.UUIDField(default = uuid.uuid4, blank=False, null=False)
    is_open = models.BooleanField(default=True, null=False)
    in_play = models.BooleanField(default=False, null=False)
    
    uuid = models.UUIDField(default = uuid.uuid4, blank=False, null=False)
    code = models.CharField(max_length=5, default=generate_code, unique=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def generate_code(self):
        self.code = generate_code()


    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code()
        super(Lobby, self).save(*args, **kwargs)

    def __str__(self):
        return self.code


class LobbyPlayer(models.Model):
    player_id = models.UUIDField(default=uuid.uuid4, blank=False, null=False)
    name = models.CharField(max_length=30, default="unkown_user")
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, related_name="players")

    word_index = models.IntegerField(default=0, blank=False, null=False)
    points = models.IntegerField(default=0, blank=False, null=False)

    # Возможно стоит записывать IP и/или последний момент выхода из лобби, чтобы отчищать


class LobbySettings(models.Model):
    lobby = models.OneToOneField("Lobby", on_delete=models.CASCADE, related_name="settings")
    penalty_time_ms = models.IntegerField(default=0)
    repeat_qustion = models.BooleanField(default=False)
    think_time_ms = models.IntegerField(default=3000)
    finish_first = models.BooleanField(default=False)

    def __str__(self):
        return f"{str(self.lobby)}"
