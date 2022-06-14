from django.shortcuts import render

def homepage(request):
    u = request.POST.get('usr','default')
    p = request.POST.get('pass','default')

    print(u)
    print(p)

    return render(request, 'homepage.html')