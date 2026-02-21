import os
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from users.decorators import superuser_required
from django.shortcuts import render

FASTAPI_URL = os.getenv('FASTAPI_URL')

@superuser_required
@require_POST
def upload_document(request):

    if 'document' not in request.FILES:
        return JsonResponse({'error': 'No file provided'}, status=400)

    file = request.FILES['document']

    if not file.name.endswith('.pdf'):
        return JsonResponse({'error': 'Only PDF files are allowed'}, status=400)

    if file.size > 20 * 1024 * 1024: 
        return JsonResponse({'error': 'File too large. Max size is 20MB'}, status=400)

    docs_dir = os.path.join(settings.MEDIA_ROOT, 'docs')
    os.makedirs(docs_dir, exist_ok=True)

    save_path = os.path.join(docs_dir, file.name)

    try:
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        print(f"  [Upload] File saved: {save_path}")
    except Exception as e:
        return JsonResponse({'error': f'Failed to save file: {str(e)}'}, status=500)


    try:
        fastapi_response = requests.post(
            f"{FASTAPI_URL}index/",
            json={"pdf_path": save_path},
            timeout=300, 
        )
        fastapi_response.raise_for_status()
        data = fastapi_response.json()

        print(f"  [Upload] Indexed {data.get('chunks_indexed')} chunks")

        return JsonResponse({
            "status":         "success",
            "filename":       file.name,
            "saved_path":     save_path,
            "chunks_indexed": data.get("chunks_indexed", 0),
            "message":        f"'{file.name}' has been indexed successfully.",
        })

    except requests.Timeout:
        return JsonResponse({
            'error': 'Indexing timed out. The file was saved but may not be fully indexed.'
        }, status=504)

    except requests.ConnectionError:
        return JsonResponse({
            'error': 'Cannot connect to the model server. Make sure FastAPI is running.'
        }, status=503)

    except requests.RequestException as e:
        return JsonResponse({
            'error': f'Indexing failed: {str(e)}'
        }, status=500)
    



@superuser_required
def admin_panel(request):
    return render(request, 'users/admin/admin_panel.html')