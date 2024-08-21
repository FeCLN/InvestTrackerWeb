from django.shortcuts import render

def home(request):
    context = {
        'current_page': 'home',  
    }
    return render(request, 'home.html', context)


