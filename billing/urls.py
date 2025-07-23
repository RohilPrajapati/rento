from django.urls import path

from billing import views

urlpatterns = [
    path('', views.ElectricityBillListView.as_view(), name='bill_list'),
    path('rentee/<int:rentee_id>', views.ElectricityBillUserWiseListView.as_view(), name='bill_list_user_wise'),
    path('create/', views.ElectricityBillCreateView.as_view(), name='bill_create'),
    path('<int:pk>/edit/', views.ElectricityBillUpdateView.as_view(), name='bill_edit'),

    path('rentee/', views.RenteeListView.as_view(), name='rentee_list'),
    path('rentee/create/', views.RenteeCreateView.as_view(), name='rentee_create'),
    path('rentee/<int:pk>/edit/', views.RenteeUpdateView.as_view(), name='rentee_edit'),
    path('rentee/<int:pk>/delete/', views.RenteeDeleteView.as_view(), name='rentee_delete'),

    #     apis
    path('api/previous-reading/', views.get_previous_reading, name='get_previous_reading'),

]
