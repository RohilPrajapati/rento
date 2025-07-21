from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages


class UserProfileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'user/profile.html')
        messages.warning(request, "Please log in to access your profile.")
        return redirect('login')