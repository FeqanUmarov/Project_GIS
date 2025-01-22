from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.http import JsonResponse
import json
from shapely.geometry import shape
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        
       
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "İstifadəçi adı və ya şifrə yalnışdır.")
    
    return redirect("index")


@login_required
def home(request):
    return render(request, 'home.html',{'user': request.user})


def get_user_geojson(request):
   
    if request.user.is_authenticated:
        user = request.user.username

 
        geojson_file_path = os.path.join(settings.BASE_DIR, 'static', 'geojson', 'torpaq.geojson')


        try:
            with open(geojson_file_path, 'r', encoding='utf-8') as f:
                geojson_data = json.load(f)  
        except FileNotFoundError:
            return JsonResponse({"error": "Geojson datası tapılmadı"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "GeoJSON məlumatı xətalıdır!"}, status=400)


        if user == "feqanumarov":
            return JsonResponse(geojson_data)

        
        filtered_features = []
        for feature in geojson_data.get("features", []):
    
            if feature.get("properties", {}).get("user") == user:
                filtered_features.append(feature)

 
        if not filtered_features:
            return JsonResponse({"error": "Bu istifadəçiyə aid geojson datası tapılmadı"}, status=404)

     
        return JsonResponse({
            "type": "FeatureCollection",
            "features": filtered_features
        })
    else:
        return JsonResponse({"error": "İstifadəçi giriş etmədi!"}, status=401)


@login_required
def my_profile(request):
    user = request.user
    return render(request, 'my_profile.html', {
        'user': user
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, "Profil məlumatları yeniləndi")
        return redirect('myprofile') 

    return render(request, 'edit_profile.html')



@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('user_login')
    return redirect('/')



@csrf_exempt
def save_geojson(request):
   
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Post request-dən gələn məlumatları alırıq
            filename = data.get('filename', 'torpaq.geojson')
            new_geojson = data.get('data')  # Yeni poliqonlar
            original_object_id = data.get('original_object_id')  # Silinecek poligonun OBJECTID-i

            # geojson tam yolunu alırıq
            full_path = os.path.join(settings.BASE_DIR, "static", "geojson", filename)

            # Movcud geosjon məlumatını yeniden yazırıq
            with open(full_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)

            existing_features = existing_data.get('features', [])

        
            if original_object_id is not None:
                existing_features = [
                    feat for feat in existing_features
                    if feat['properties'].get('OBJECTID') != original_object_id
                ]

   
            new_features = new_geojson.get('features', [])
            for i, feature in enumerate(new_features):
               
                feature['properties']['OBJECTID'] = original_object_id + 100 + i

            existing_features.extend(new_features)

           
            existing_data['features'] = existing_features

    
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)

            return JsonResponse({'status': 'ok'}, status=200)

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)


    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)

