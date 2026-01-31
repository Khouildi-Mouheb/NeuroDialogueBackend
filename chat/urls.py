from django.urls import path
from .views import chat , chat_page , createChat
urlpatterns = [
    path('chat/<int:chat_id>/', chat_page, name='chat_page'),
    path('chat/<int:chat_id>/send/', chat, name='chat'),
    path('new-chat/', createChat, name='new_chat'),
]
