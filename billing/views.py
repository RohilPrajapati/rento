from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.http import require_GET

from billing.forms import RenteeForm, ElectricityBillForm
from billing.models import Rentee, ElectricityBill
from billing.utils import get_previous_month_and_year
from elec_proj.mixins import PaginationMixin
import nepali_datetime
from elec_proj.constants import DATE_MONTH_CHOICES


# Create your views here.
class RenteeListView(LoginRequiredMixin, PaginationMixin, View):
    paginate_by = 10  # override default if needed

    def get(self, request):
        query = request.GET.get('q', '')
        rentees = Rentee.objects.filter(is_deleted=False).order_by('full_name')

        if query:
            rentees = rentees.filter(full_name__icontains=query)

        page_obj = self.paginate_queryset(rentees, request)

        context = {
            'rentees': page_obj,
            'search_query': query,
        }
        return render(request, 'rentee/list.html', context)


class RenteeCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = RenteeForm()
        return render(request, 'rentee/form.html', {'form': form})

    def post(self, request):
        form = RenteeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Added Rentee Successfully")
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
            messages.success(request, "Updated Rentee Successfully")
            return redirect('rentee_list')
        return render(request, 'rentee/form.html', {'form': form})


class RenteeDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        rentee = get_object_or_404(Rentee, pk=pk)
        rentee.is_deleted = True
        rentee.save()
        messages.success(request, "Remove Rentee Successfully")
        return redirect('rentee_list')


class BaseElectricityBillListView(LoginRequiredMixin, PaginationMixin, View):
    rentee_filter = None  # To be overridden in child class if needed

    def get_filter_params(self, request):
        query = request.GET.get('q', '').strip()
        query_month = request.GET.get('q_month')
        query_year = request.GET.get('q_year')

        filter_params = {}

        if query:
            filter_params['rentee__full_name__icontains'] = query
        if query_month:
            filter_params['billing_month'] = query_month
        if query_year:
            filter_params['billing_year'] = query_year

        return filter_params, query, query_month, query_year

    def get_queryset(self, filter_params):
        qs = ElectricityBill.objects.select_related('rentee')
        if self.rentee_filter:
            qs = qs.filter(rentee=self.rentee_filter)
        return qs.filter(**filter_params)

    def get_context_data(self, request, page_obj, query, q_month, q_year, **kwargs):
        context = {
            'bills': page_obj,
            'search_query': query,
            'q_month': str(q_month) if q_month is not None else '',
            'q_year': str(q_year) if q_year is not None else '',
            'DATE_MONTH_CHOICES': DATE_MONTH_CHOICES,
        }
        context.update(kwargs)
        return context

    def get(self, request, *args, **kwargs):
        filter_params, query, q_month, q_year = self.get_filter_params(request)
        queryset = self.get_queryset(filter_params)
        page_obj = self.paginate_queryset(queryset, request)
        context = self.get_context_data(
            request, page_obj, query, q_month, q_year, **kwargs
        )
        return render(request, self.template_name, context)

class ElectricityBillListView(BaseElectricityBillListView):
    template_name = 'billing/list.html'

class ElectricityBillUserWiseListView(BaseElectricityBillListView):
    template_name = 'billing/user_wise_list.html'

    def dispatch(self, request, *args, **kwargs):
        self.rentee = get_object_or_404(Rentee, pk=kwargs['rentee_id'])
        self.rentee_filter = self.rentee
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, request, page_obj, query, q_month, q_year, **kwargs):
        context = super().get_context_data(
            request, page_obj, query, q_month, q_year, **kwargs
        )
        context['rentee'] = self.rentee
        return context


@login_required
@require_GET
def get_previous_reading(request):
    rentee_id = request.GET.get('rentee_id')
    billing_month = request.GET.get('billing_month')  # expect number as string, e.g. "1" for January
    billing_year = request.GET.get('billing_year')  # e.g. "2025"

    if not (rentee_id and billing_month):
        return JsonResponse({'previous_reading': None})

    # Parse month and year
    try:
        month = int(billing_month)
        year = int(billing_year)
    except ValueError:
        return JsonResponse({'previous_reading': None})

    # Calculate previous month and year
    prev_month, prev_year = get_previous_month_and_year(month, year)

    try:
        prev_bill = ElectricityBill.objects.get(rentee_id=rentee_id, billing_month=prev_month, billing_year=prev_year)
        previous_reading = prev_bill.current_reading
    except ElectricityBill.DoesNotExist:
        previous_reading = None

    return JsonResponse({'previous_reading': previous_reading})


class ElectricityBillCreateView(LoginRequiredMixin, View):
    def get(self, request):
        rentee_id = request.GET.get('rentee_id')
        initial_data = {}

        if rentee_id:
            initial_data['rentee'] = get_object_or_404(Rentee, pk=rentee_id)
        form = ElectricityBillForm(initial=initial_data)
        return render(request, 'billing/form.html', {'form': form})

    def post(self, request):
        form = ElectricityBillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Added Bill Successfully")
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
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
            messages.success(request, "Updated Bill Successfully")
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('bill_list')
        return render(request, 'billing/form.html', {'form': form})

class ElectricityBillDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        bill = get_object_or_404(ElectricityBill, pk=pk)
        bill.delete()
        messages.success(request, "Bill deleted successfully.")
        next_url = request.POST.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('bill_list')


class HomePageView(View):
    def get(self, request):
        today = nepali_datetime.date.today()
        current_month = today.month
        current_year = today.year

        total_rentees = Rentee.objects.filter(is_deleted=False).count()

        monthly_bill_count = ElectricityBill.objects.filter(
            billing_month=int(current_month),
            billing_year=int(current_year)
        ).count()

        pending_bill_count = ElectricityBill.objects.filter(
            bill_status='pending'
        ).count()
        summary = {
            'total_rentees': total_rentees,
            'monthly_bill_count': monthly_bill_count,
            'pending_bill_count': pending_bill_count,
        }
        return render(request, 'home.html', context=summary)
