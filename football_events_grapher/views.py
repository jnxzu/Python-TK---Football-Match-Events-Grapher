from django.http import HttpResponse
from django.template import loader


def landing(request):
    template = loader.get_template('landing.html')
    return HttpResponse(template.render({}, request))


def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render({}, request))
