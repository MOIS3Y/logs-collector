from django.http import HttpResponse
from django.template import loader


class HttpResponseNotAllowedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        if response.status_code == 405:
            context = {}
            template = loader.get_template('405.html')
            return HttpResponse(template.render(context, request))

        return response
