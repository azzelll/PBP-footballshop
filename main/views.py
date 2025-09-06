from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'app_name' : 'PROSCORE',
        'name': 'Made Shandy Krisnanda',
        'class': 'PBP C'
    }

    return render(request, "main.html", context)