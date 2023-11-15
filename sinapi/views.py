from django.views.generic import TemplateView
from django.shortcuts import render

class ReactAppView(TemplateView):
    template_name = "mainapp.html"  # Your Django template that includes React build files



def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')