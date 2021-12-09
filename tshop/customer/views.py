from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import *

# Create your views here.
def CustomerRegisterView(request):
    if request.method == 'POST':
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your registration successfully submit . Yor are Now Login available')
            return redirect('home')
    else:
        form=CustomerRegistrationForm()
    return render(request, 'customerregistration.html', {'form':form})

