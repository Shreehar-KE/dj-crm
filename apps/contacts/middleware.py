from django.contrib import messages
from django.http import HttpResponse
import json


class HtmxMessageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        messages_to_show = []
        for message in messages.get_messages(request):
            if "htmx-toast" in message.tags:
                messages_to_show.append(
                    {"message": message.message, "level": message.level_tag})
        if messages_to_show:
            response.headers["HX-Trigger"] = f"htmx:messages {json.dumps(messages_to_show)}"
        return response
