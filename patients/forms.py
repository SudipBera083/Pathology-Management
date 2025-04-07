from django import forms
from .models import Patient, DiagnosticTest, FactorsInDiagnosticTest, DefaultFactorValues

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'phone', 'referred_doctor', 'tests', 'age', 'age_unit']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'referred_doctor': forms.TextInput(attrs={'class': 'form-control'}),
            'tests': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'age_unit': forms.Select(attrs={'class': 'form-control'}),
        }

class DiagnosticTestForm(forms.ModelForm):
    class Meta:
        model = DiagnosticTest
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class FactorsInDiagnosticTestForm(forms.ModelForm):
    class Meta:
        model = FactorsInDiagnosticTest
        fields = ['test_name', 'factors']
        widgets = {
            'test_name': forms.Select(attrs={'class': 'form-control'}),
            'factors': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DefaultFactorValuesForm(forms.ModelForm):
    class Meta:
        model = DefaultFactorValues
        fields = ['test_name', 'factor_name', 'min_age', 'min_age_unit', 'max_age', 'max_age_unit', 'min_value', 'max_value', 'unit']
        widgets = {
            'test_name': forms.Select(attrs={'class': 'form-control'}),
            'factor_name': forms.Select(attrs={'class': 'form-control'}),
            'min_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_age_unit': forms.Select(attrs={'class': 'form-control'}),
            'max_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_age_unit': forms.Select(attrs={'class': 'form-control'}),
            'min_value': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_value': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
        }
