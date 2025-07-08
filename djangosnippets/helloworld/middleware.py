from django.shortcuts import redirect
from django.contrib import messages

class RejectNotManager:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if path.startswith('/manager') and request.path != '/manager/signup/':
            user = request.user

            if not user.is_authenticated:
                messages.warning(request, 'ログインしてください。')
                return redirect('login')

            if not getattr(user, 'is_manager', False):
                messages.error(request, 'このページのアクセス権限がありません。')
                return redirect('top')

        return self.get_response(request)
