from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'npm' : '2406453530',
        'name': 'Muhammad Adra Prakoso',
        'class': 'PBP KKI'
    }

    return render(request, "main.html", context)