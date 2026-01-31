from django.db import models
from users.models import User
import uuid



class Chat(models.Model):
    title=models.CharField(
        max_length=50,
        default='title',
        )
    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        )
    created_at=models.DateTimeField(
        auto_now_add=True
        )
    updated_at=models.DateTimeField(
        auto_now=True
        )
    
    def __str__(self):
        return f'Chat {self.id} - {self.user.id}'

class Prompt(models.Model):
    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        )
    chat=models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        )
    content=models.TextField(
        max_length=5000
        )
    created_at=models.DateTimeField(
        auto_now_add=True,
        )
    
    def __str__(self):
        return f'Prompt {self.id} - {self.user}'
    

class Response(models.Model):
    prompt=models.ForeignKey(
        Prompt,
        on_delete=models.CASCADE,
        related_name='response',
        )
    chat=models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        )
    content=models.TextField()
    created_at=models.DateTimeField(
        auto_now_add=True,
        )
    
    def __str__(self):
        return f'Response {self.id} to {self.prompt.id}'
    

