
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('edit-patient/<int:pk>/',views.edit_patient, name='edit_patient'),
    path('delete-patient/<int:pk>/', views.delete_patient, name='delete_patient'),
    path('add-test/', views.add_test, name='add_test'),
    path('add-factor/', views.add_factor, name='add_factor'),
    path("factor/edit/<int:factor_id>/", views.edit_factor, name="edit_factor"),
    path("factor/delete/<int:factor_id>/", views.delete_factor, name="delete_factor"),
    path('add-default-value/', views.add_default_value, name='add_default_value'),
    path('receipt/<int:patient_id>/', views.download_receipt, name='download_receipt'),

    path("set-default-values/<int:factor_id>/", views.set_default_values, name="set_default_values"),
    path('edit-default-value/<int:value_id>/', views.edit_default_value, name='edit_default_value'),
    path('delete-default-value/<int:value_id>/', views.delete_default_value, name='delete_default_value'),
    # path('generate-report/<int:patient_id>/', views.generate_report, name='generate_report'),
    # path('patient/generate-report/<int:patient_id>/<int:test_id>/', views.generate_report, name='generate_report'),
    # path("select-test/<int:patient_id>/", views.select_test, name="select_test"),
    # path("generate-report/<int:patient_id>/", views.generate_report, name="generate_report"),
    path('patient/save-test-report/<int:patient_id>/', views.save_test_report, name='save_test_report'),
    path('takeResponse/<int:patient_id>/', views.takeResponse, name="takeResponse"),
    path("select_test/<int:patient_id>/", views.select_test, name="select_test"),
    path('generate_report/<int:report_id>/', views.generate_diagnostic_report, name='generate_report'),
    path('generate_custom_report/<int:report_id>/', views.generate_custom_report, name='generate_custom_report'),








]
