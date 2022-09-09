from django.contrib import admin

# Register your models here.

from .models import Adherent , Form_TVA ,TYPE_TAUX,TYPE_DEDUCTION,Rubrique,\
    Declaration,Deduction,Taxe,CA_Total,Montant_CA,Montant_Bilan,\
    Releve_Deduction ,Releve_deduction_edi,Designation


admin.site.register(Adherent)
admin.site.register(Form_TVA)
admin.site.register(TYPE_TAUX)
admin.site.register(TYPE_DEDUCTION)
admin.site.register(Rubrique)
admin.site.register(Montant_CA)
admin.site.register(Declaration)
admin.site.register(Deduction)
admin.site.register(Taxe)
admin.site.register(CA_Total)
admin.site.register(Montant_Bilan)
admin.site.register(Releve_Deduction)
admin.site.register(Releve_deduction_edi)
admin.site.register(Designation)