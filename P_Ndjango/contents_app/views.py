from django.shortcuts import render, redirect
from django.http import JsonResponse
from google.cloud import vision
from google.cloud.vision_v1 import types
from django.contrib import messages
from . import receipe_search

# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')

def search(request):
    return render(request, 'search.html')

def material_search(request):
    if request.method == 'POST' :
        image = request.FILES['image'] # FILES를 따로 한 이유가 있나
        content = image.read()
        image = types.Image(content=content)
        text = receipe_search.tempFunction(image) # receipt_image to text

        return redirect('material_search.html', {'temptext':text})

    return render(request, 'material_search.html')

# 이미지 검색
from googletrans import Translator

def img_search(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        client = vision.ImageAnnotatorClient()

        content = image.read()
        image = types.Image(content=content)
        # 이미지 객체를 텍스트로 변환
        response = client.object_localization(image=image)
        objects = response.localized_object_annotations

        if objects:
            detected_objects = [obj.name for obj in objects]
            unique_detected_objects = list(set(detected_objects))
            
            # 구글 번역 API 한국어로 번역 일일 사용량 제한있음
            translator = Translator()
            translated_objects = [translator.translate(obj, src='en', dest='ko').text for obj in unique_detected_objects]
            
            # '음식' 및 '패키지 상품' 필터링
            filtered_objects = [obj for obj in translated_objects if obj not in ['음식', '패키지 상품', '채소']]
            
            return render(request, 'img_search.html', {'translated_objects': filtered_objects})
        else:
            messages.warning(request, '재료를 찾을 수 없습니다.')
            return render(request, 'img_search.html')
    else:
        return render(request, 'img_search.html')

def board(request):
    return render(request, 'board.html')

def search_result(request):
    return render(request, 'search_result.html')

def mypage(request):
    return render(request, 'my_page.html')

def profile_edit(request):
    return render(request, 'profile_edit.html')

def post(request) :
    return render(request, 'post.html')

def write_post(request) :
    return render(request, 'write_post.html')