from django.shortcuts import render
from utils.logger import print_log
from django.contrib.auth import logout
from utils.util import *
from django.http import JsonResponse


class ProductException(Exception):

    def __init__(self, request=None, message=None, custom_message=None, mode=None, page=None,
                 context=None, logoff=False, jsonresponse=False):
        self.custom_message = custom_message
        self.message = message
        self.request = request
        self.mode = mode
        self.page = page
        self.context = context
        self.logoff = logoff
        if self.message is not None:
            print_log.error(error_message=str(self.message))
        self.jsonresponse = jsonresponse
        super().__init__(self.message)

    def set_request(self, request=None):
        if request is not None:
            self.request = request

    def set_custom_message(self, custom_message=None):
        if custom_message is not None:
            self.custom_message = custom_message

    def set_message(self, message=None):
        if message is not None:
            self.message = message

    def set_mode(self, mode=None):
        if mode is not None:
            self.mode = mode

    def set_page(self, page=None):
        if page is not None:
            self.page = page

    def set_context(self, context=None):
        if context is not None:
            self.context = context

    def set_logoff(self, logoff=False):
        if not logoff:
            self.logoff = logoff

    def set_jsonresponse(self, jsonresponse=None):
        if jsonresponse is not None:
            self.jsonresponse = jsonresponse

    def handle_exception(self):
        remove_message(self.request, remove_all=True)
        if self.request is not None and self.custom_message is not None:
            messages.warning(self.request, f'{str(self.custom_message)}')
        if self.logoff and self.request is not None:
            logout(self.request)
        if self.page is not None and self.mode is not None:
            if self.mode.lower() == 'render' and self.request is not None:
                return render(self.request, self.page, self.context)
            elif self.mode.lower() == 'redirect':
                if self.context is None:
                    return redirect(self.page)
                else:
                    return redirect(self.page + ','.join([f'{key}={value}' for key, value in self.context.items()]))
            else:
                return redirect('core:homepage')
        elif self.jsonresponse:
            return JsonResponse({'error': f"'{self.message}'"})
        else:
            return redirect('core:homepage')
