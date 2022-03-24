from django import forms

from apps.adjuster.models import Adjuster
from apps.city.models import City

__author__ = 'alexy'


class AdjusterAddForm(forms.ModelForm):
    class Meta:
        model = Adjuster
        exclude = ['user']
        widgets = {
            'city': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AdjusterAddForm, self).__init__(*args, **kwargs)
        if self.request.user:
            user = self.request.user
            if user.type == 6:
                self.fields['city'].queryset = user.superviser.city.all()
            elif user.type == 2:
                self.fields['city'].queryset = City.objects.filter(moderator=user)
            elif user.type == 5:
                self.fields['city'].queryset = City.objects.filter(moderator=user.manager.moderator)


class AdjusterUpdateForm(forms.ModelForm):
    class Meta:
        model = Adjuster
        exclude = []
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control hide'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AdjusterUpdateForm, self).__init__(*args, **kwargs)
        if self.request.user:
            user = self.request.user
            if user.type == 6:
                self.fields['city'].queryset = user.superviser.city.all()
            elif self.request.user.type == 2:
                self.fields['city'].queryset = City.objects.filter(moderator=user)
            elif self.request.user.type == 5:
                self.fields['city'].queryset = City.objects.filter(moderator=user.manager.moderator)


class AdjusterPaymentForm(forms.ModelForm):
    class Meta:
        model = Adjuster
        fields = ('cost_mounting', 'cost_change', 'cost_repair', 'cost_dismantling', 'cost_view')
        widgets = {
            'cost_mounting': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost_change': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost_repair': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost_dismantling': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost_view': forms.NumberInput(attrs={'class': 'form-control'}),
        }
