from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

class UserProfileView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, 'user/profile.html')
