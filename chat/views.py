from django.shortcuts import render , redirect , get_object_or_404
from .models import Prompt , Response , Chat
from users.models import User
from django.http import JsonResponse
import requests
from django.views.decorators.http import require_POST




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
        # Call the FastAPI endpoint /chat_final
        response = requests.get(
            'http://127.0.0.1:8001/chat_final',
            params={"text": user_input},
            timeout=500,
        )
        response.raise_for_status()

        # Get clean model output
        model_output = response.json().get("response", "")

        # Save model output to DB
        response_obj = Response(
            prompt=prompt,
            content=model_output,
            chat=chat
        )
        response_obj.save()

    except requests.RequestException as e:
        return JsonResponse({'error': f'cannot reach the model: {e}'}, status=500)

    # Return the model output as JSON
    return JsonResponse({"response": model_output})


def chat_page(request , chat_id):
    chat=get_object_or_404(
        Chat,
        id=chat_id,
    )
    prompts=Prompt.objects.filter(
        chat=chat
        ).prefetch_related(
                'response'
            )
    conversation=[]
    for prompt in prompts:
        conversation.append({
                'prompt':prompt,
                'response':prompt.response.first()
            })
    context={
        'chat':chat,
        'conversation':conversation,
        }
    return render(request, 
                  "users/chat.html",
                  context)


def createChat(request):
    chat = Chat.objects.create(user=request.user)
    return redirect('chat_page', chat_id=chat.id)







