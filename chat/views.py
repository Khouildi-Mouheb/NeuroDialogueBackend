from django.shortcuts import render, redirect, get_object_or_404
from .models import Prompt, Response, Chat
from django.http import JsonResponse
import requests
import os


FASTAPI_URL = os.getenv('FASTAPI_URL')

def chat(request, chat_id):
    print("DJANGO CHAT VIEW HIT")
    chat = get_object_or_404(Chat, id=chat_id)

    # Get user input
    user_input = request.GET.get('text', '')
    if not user_input:
        return JsonResponse({'error': 'no input provided'}, status=400)

    # Save prompt to DB
    prompt = Prompt(user=request.user, content=user_input, chat=chat)
    prompt.save()

    try:
        # ✅ CHANGED - Call deployed FastAPI instead of localhost
        response = requests.get(
            f'{FASTAPI_URL}/chat_final',  # ← Now uses deployed URL
            params={"text": user_input},
            timeout=60,  # ← Reduced from 500 for cloud
        )
        response.raise_for_status()

        # Get clean model output
        data = response.json()
        model_output = data.get("response", "")

        # Save model output to DB
        response_obj = Response(
            prompt=prompt,
            content=model_output,
            chat=chat
        )
        response_obj.save()

        return JsonResponse({
            "response": model_output,
            "analysis": data.get("analysis", {})  # ← Emotion analysis included
        })

    except requests.Timeout:
        return JsonResponse({
            'error': 'The AI is thinking too hard. Please try again.'
        }, status=504)
    
    except requests.RequestException as e:
        return JsonResponse({
            'error': f'AI service unavailable: {str(e)}'
        }, status=503)


def chat_page(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    prompts = Prompt.objects.filter(
        chat=chat
    ).prefetch_related('response')
    
    conversation = []
    for prompt in prompts:
        conversation.append({
            'prompt': prompt,
            'response': prompt.response.first()
        })
    
    context = {
        'chat': chat,
        'conversation': conversation,
    }
    return render(request, "users/chat.html", context)


def createChat(request):
    chat = Chat.objects.create(user=request.user)
    return redirect('chat_page', chat_id=chat.id)