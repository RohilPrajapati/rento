from django.shortcuts import render, redirect, get_object_or_404
from billing.models import Rentee, ElectricityBill
from billing.forms import RenteeForm, ElectricityBillForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class RenteeListView(LoginRequiredMixin,View):
    def get(self, request):
        rentees = Rentee.objects.filter(is_deleted=False)
        print(rentees)
        return render(request, 'rentee/list.html', {'rentees': rentees})

class RenteeCreateView(LoginRequiredMixin,View):
    def get(self, request):
        form = RenteeForm()
        return render(request, 'rentee/form.html', {'form': form})

    def post(self, request):
        form = RenteeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rentee_list')
        return render(request, 'rentee/form.html', {'form': form})

class RenteeUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        rentee = get_object_or_404(Rentee, pk=pk, is_deleted=False)
        form = RenteeForm(instance=rentee)
        return render(request, 'rentee/form.html', {'form': form})

    def post(self, request, pk):
        rentee = get_object_or_404(Rentee, pk=pk, is_deleted=False)
        form = RenteeForm(request.POST, instance=rentee)
        if form.is_valid():
            form.save()
            return redirect('rentee_list')
        return render(request, 'rentee/form.html', {'form': form})

class RenteeDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        rentee = get_object_or_404(Rentee, pk=pk)
        rentee.is_deleted = True
        rentee.save()
        return redirect('rentee_list')

class ElectricityBillListView(LoginRequiredMixin, View):
    def get(self, request):
        bills = ElectricityBill.objects.select_related('rentee')
        return render(request, 'billing/list.html', {'bills': bills})


class ElectricityBillCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ElectricityBillForm()
        return render(request, 'billing/form.html', {'form': form})

    def post(self, request):
        form = ElectricityBillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bill_list')
        return render(request, 'billing/form.html', {'form': form})


class ElectricityBillUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        bill = get_object_or_404(ElectricityBill, pk=pk)
        form = ElectricityBillForm(instance=bill)
        return render(request, 'billing/form.html', {'form': form})

    def post(self, request, pk):
        bill = get_object_or_404(ElectricityBill, pk=pk)
        form = ElectricityBillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect('bill_list')
        return render(request, 'billing/form.html', {'form': form})