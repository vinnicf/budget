from django.views.generic import TemplateView

class ReactAppView(TemplateView):
    template_name = "mainapp.html"  # Your Django template that includes React build files
