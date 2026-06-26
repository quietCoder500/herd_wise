#
# Initial code credits to Kevin Renskers
# https://www.loopwerk.io/articles/2025/alpine-ajax-django/
#

from django.template.response import TemplateResponse as BaseTemplateResponse
from django.http import HttpRequest


def is_alpine(request: HttpRequest) -> bool:
    return "X-Alpine-Request" in request.headers


class AlpineTemplateResponse(BaseTemplateResponse):
    def get_ajax_template(self, request: HttpRequest, template: str) -> str:
        if is_alpine(request):
            # Use the target ID from the request as the partial name.
            # This allows one view to serve multiple, distinct partials.
            partial = request.headers.get("X-Alpine-Target")
            if not partial:
                raise ValueError("No 'X-Alpine-Target' in an 'X-Alpine-Request'")
            return f"{template}#{partial}"

        return template

    def __init__(self, request: HttpRequest, template: str, *args, **kwargs):
        template_name = self.get_ajax_template(request, template)
        super().__init__(request, template_name, *args, **kwargs)
