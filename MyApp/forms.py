from django import forms
""" FORMULAIRE DE CALCUL D'ECART """
class EcartForm(forms.Form):
    year= forms.IntegerField()
    start = forms.DateField()
    end = forms.DateField()
    direction = forms.CharField()
""" FORMULAIRE DE L'ACTIVITE CONTRIBUABLE  """
class  DesignationForm(forms.Form):
    client_name = forms.CharField(max_length=255)
    client_id = forms.IntegerField()
    direction = forms.CharField()
""" FORMULAIRE POUR COMPARER LES CREDITS """
class CreditForm(forms.Form):
    client_name = forms.CharField(max_length=255)
    client_id  = forms.IntegerField()
    annee_depot = forms.IntegerField()

