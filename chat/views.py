from django.shortcuts import render, redirect, get_object_or_404
from .models import Prompt, Response, Chat
from django.http import JsonResponse
import requests
import os
import logging
from django.conf import settings

FASTAPI_URL = os.getenv('FASTAPI_URL')






logger = logging.getLogger(__name__)

def chat(request, chat_id):
    """
    Handle chat message and get AI response
    """
    print("DJANGO CHAT VIEW HIT")
    
    chat = get_object_or_404(Chat, id=chat_id)
    
    # ✅ FIX 1: Get user input from POST, not GET
    if request.method == 'POST':
        user_input = request.POST.get('text', '') or request.body.decode('utf-8')
        # If using JSON body:
        import json
        try:
            body = json.loads(request.body)
            user_input = body.get('text', '')
        except:
            user_input = request.POST.get('text', '')
    else:
        # Fallback to GET (if needed for testing)
        user_input = request.GET.get('text', '')
    
    if not user_input:
        return JsonResponse({'error': 'no input provided'}, status=400)
    
    # Save prompt to DB
    prompt = Prompt(user=request.user, content=user_input, chat=chat)
    prompt.save()
    
    try:
        # ✅ FIX 2: Use POST request with JSON body
        response = requests.post(  # ← Changed from GET to POST
            settings.FASTAPI_URL,  # ← Use settings.FASTAPI_URL
            json={"text": user_input},  # ← Send as JSON body, not params
            headers={"Content-Type": "application/json"},  # ← Add header
            timeout=60,
        )
        
        response.raise_for_status()
        
        # ✅ FIX 3: Parse response correctly
        data = response.json()
        
        # FastAPI returns: {"status": "success", "data": "...", "error": null}
        model_output = data.get("data", "") or data.get("response", "")
        
        if not model_output:
            logger.error(f"No response from FastAPI: {data}")
            model_output = "I apologize, but I couldn't generate a response."
        
        # Save model output to DB
        response_obj = Response(
            prompt=prompt,
            content=model_output,
            chat=chat
        )
        response_obj.save()
        
        return JsonResponse({
            "response": model_output,
            "status": data.get("status", "success"),
            "analysis": data.get("analysis", {})
        })
        
    except requests.Timeout:
        logger.error("FastAPI request timeout")
        return JsonResponse({
            'error': 'The AI is thinking too hard. Please try again.'
        }, status=504)
    
    except requests.ConnectionError:
        logger.error(f"Cannot connect to FastAPI at {settings.FASTAPI_URL}")
        return JsonResponse({
            'error': 'AI service is not available. Make sure FastAPI is running on http://localhost:8000'
        }, status=503)
    
    except requests.RequestException as e:
        logger.error(f"FastAPI request error: {str(e)}")
        return JsonResponse({
            'error': f'AI service unavailable: {str(e)}'
        }, status=503)
    
    except Exception as e:
        logger.error(f"Unexpected error in chat view: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': 'An unexpected error occurred'
        }, status=500)


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