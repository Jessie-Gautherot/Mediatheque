from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def admin_home(request):
    return render(request, "administration/administration_home.html")

def login_admin(request):
    # Formulaire vide par défaut
    form = AuthenticationForm(request=request, data=None)
    return render(request, 'registration/login.html', {'form': form})





