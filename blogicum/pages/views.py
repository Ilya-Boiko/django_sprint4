from django.shortcuts import render
from django.views.generic import TemplateView


def about(request):
    return render(request, 'pages/about.html')


def rules(request):
    return render(request, 'pages/rules.html')


def custom_403_view(request, exception):
    return render(request, 'pages/403csrf.html', status=403)


def custom_404_view(request, exception):
    return render(request, 'pages/404.html', status=404)


def custom_500_view(request):
    return render(request, 'pages/500.html', status=500)


class AboutView(TemplateView):
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    template_name = 'pages/rules.html'
