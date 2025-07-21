from django.urls import path
from billing.views import (
    RenteeListView, RenteeCreateView, RenteeUpdateView, RenteeDeleteView,
    ElectricityBillListView,ElectricityBillCreateView, ElectricityBillUpdateView
)

urlpatterns = [
    path('', ElectricityBillListView.as_view(), name='bill_list'),
    path('create/', ElectricityBillCreateView.as_view(), name='bill_create'),
    path('<int:pk>/edit/', ElectricityBillUpdateView.as_view(), name='bill_edit'),

    path('rentee/', RenteeListView.as_view(), name='rentee_list'),
    path('rentee/create/', RenteeCreateView.as_view(), name='rentee_create'),
    path('rentee/<int:pk>/edit/', RenteeUpdateView.as_view(), name='rentee_edit'),
    path('rentee/<int:pk>/delete/', RenteeDeleteView.as_view(), name='rentee_delete'),

]
