from django.db import models

# Create your models here.

class Adherent(models.Model):
    ID_ADHERENT = models.BigIntegerField(primary_key=True)
    NOM_PRENOM_RS = models.CharField(max_length=255 ,null=True)
    CODE_DIRECTION = models.CharField(max_length=255,null=True)
    def __str__(self):
        return str(self.ID_ADHERENT)
class Form_TVA(models.Model):
    ID_FORMULAIRE = models.IntegerField(primary_key=True)
    ANNEE_FORMULAIRE = models.IntegerField(null=True)
    LIB_FORMULAIRE = models.CharField(max_length=255,null=True)
    DATE_CREATION_FORM= models.DateField(auto_now_add= True,null=True)
    PUBLICATION_FORMULAIRE =models.SmallIntegerField(null=True)
    CLASS_NAME =models.CharField(max_length=255,default='')
    DATE_TRANSFERT_METIER =models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return str(self.ID_FORMULAIRE)
class TYPE_TAUX(models.Model):
    ID_TYPE_TAUX = models.BigIntegerField(primary_key=True,default=0)
    ID_FORMULAIRE = models.ForeignKey(Form_TVA,on_delete=models.CASCADE,null=True)
    TYPE_TAUX=models.CharField(max_length=255,null=True)
    LIB_TYPE_TAUX = models.CharField(max_length=100,null=True)
    TAUX_NORMAL = models.SmallIntegerField(null=True)
    TAUX_AVEC_DEDUCTION = models.SmallIntegerField(null=True)
    LIB_TYPE_TAUX_AR = models.CharField(max_length=255,null=True)

    def __str__(self):
        return str(self.ID_TYPE_TAUX)
class TYPE_DEDUCTION(models.Model):
    ID_TYPE_DEDUCTION = models.BigIntegerField(primary_key=True,default=0)
    ID_FORMULAIRE = models.ForeignKey(Form_TVA,on_delete=models.CASCADE,null=True)
    #TYP_ID_TYPE_DEDUCTION = models.ForeignKey(TYPE_DEDUCTION,on_delete=models.CASCADE)!!!
    TYPE_DEDUCTION = models.CharField(max_length=255)
    LIB_TYPE_DEDUCTION = models.CharField(max_length=100,null=True)
    ORDRE =models.IntegerField(null=True)
    LIB_TYPE_DEDUCTION_AR =models.CharField(max_length=255,null=True)
    def  __str__(self):
        return str(self.ID_TYPE_DEDUCTION)

class Rubrique(models.Model):
    ID_RUBRIQUE = models.BigIntegerField(primary_key=True)
    ID_TYPE_DEDUCTION = models.ForeignKey(TYPE_DEDUCTION,on_delete=models.CASCADE,null=True)
    ID_TYPE_TAUX = models.ForeignKey(TYPE_TAUX,on_delete=models.CASCADE,null=True)
    CODE_RUBRIQUE = models.IntegerField(default=10)
    LIB_RUBRIQUE = models.CharField(max_length=255,null=True)
    PRECISION_RUBRIQUE =models.CharField(max_length=1024,null=True)
    TAUX_RUBRIQUE =models.DecimalField(max_digits=15,decimal_places=3,null=True)
    ORDER_RUBRIQUE =models.IntegerField(null=True)
    LIB_RUBRIQUE_AR =models.CharField(max_length=500,null=True)
    def __str__(self):
        return  str(self.ID_RUBRIQUE)
class Declaration(models.Model):
    ID_DECLARATION = models.BigIntegerField(primary_key=True)
    ID_ENVOI_EDI = models.BigIntegerField(blank=True)
    ID_FORMULAIRE = models.IntegerField()
    ID_ADHERENT = models.ForeignKey(Adherent,on_delete=models.CASCADE)
    ANNEE_DECLAR = models.IntegerField() #prend des valeurs de 1 a 4
    #PERIODE_DECLAR = models.SmallIntegerField()
    #REGIME_DECLAR = models.SmallIntegerField()
    #CODE_COMP = models.IntegerField(blank=True)
    DATE_DEPOT = models.DateField()
    #FAIT_GEN = models.CharField(max_length=255)
    #RENS = models.CharField(max_length=1024)
    #MODE_DECLAR = models.SmallIntegerField()#des valeurs de 1 à 4
    CA_GLOBAL = models.DecimalField(max_digits=15,decimal_places=2)
    MNT_TAXE = models.DecimalField(max_digits=15,decimal_places=2)
    MNT_DEDUCTION = models.DecimalField(max_digits=15,decimal_places=2)
    MNT_CREDIT = models.DecimalField(max_digits=15,decimal_places=2)
    TVA_DUE = models.DecimalField(max_digits=15,decimal_places=2)
    PAIEMENT_ACCOMP = models.DecimalField(max_digits=15,decimal_places=2)
    TAXE_PAYEE = models.DecimalField(max_digits=15,decimal_places=2)
    #ETAT_DECLARATION = models.IntegerField()
    #RELEVE_DEDUCTION = models.CharField(max_length=100)
    #DATE_EFF_DEPOT = models.DateField()
    """ IS_HISTORY_ONLY = models.SmallIntegerField(default=0)
    TYPE_DECLAR = models.CharField(max_length=255)
    DELETED = models.SmallIntegerField(default=10)
    USER_MAJ = models.CharField(max_length=100)
    DATE_MAJ = models.DateTimeField(auto_now_add= True)
    DATE_TRANSFERT_METIER = models.DateField()
    MAJ = models.CharField(max_length=1)
    MAJ_T_METIER = models.CharField(max_length=1)
    RELEVE_DEDUCTION_AUTRE = models.CharField(max_length=100)
    PAIEMENT_MC_INITILIZED = models.SmallIntegerField(default=0)
    REF_PAIEMENT = models.CharField(max_length=20)
    MONTANT_VERSE =  models.DecimalField(max_digits=15,decimal_places=2)
    PRINCIPAL_VERSE = models.DecimalField(max_digits=15,decimal_places=2,default=0 )
    DROITS_COMP_TVA = models.DecimalField(max_digits=15,decimal_places=2,default=0 )
    """
    def __str__(self):
        return str(self.ID_DECLARATION)
class Deduction(models.Model):
    ID_RUBRIQUE = models.ForeignKey(Rubrique,on_delete=models.CASCADE)
    ID_DECLARATION = models.ForeignKey(Declaration,on_delete=models.CASCADE)
    TVA_FACTURES = models.DecimalField(max_digits=15 , decimal_places=2)
   # TVA_DEDUCTIBL = models.DecimalField(max_digits=15,decimal_places=2)
    TVA_DEDUCTIBL = models.FloatField()
    APPLIQUE_PRORATA = models.DecimalField(max_digits=15,decimal_places=2)
    USED = models.SmallIntegerField(default=0)
    class Meta:
        unique_together = ("ID_DECLARATION","ID_RUBRIQUE")
    def __str__(self):
        return str(self.ID_RUBRIQUE)
class Taxe(models.Model):
    ID_RUBRIQUE = models.ForeignKey(Rubrique,on_delete=models.CASCADE)
    ID_DECLARATION = models.ForeignKey(Declaration,on_delete=models.CASCADE)
    BASE_IMPOSABLE = models.DecimalField(max_digits=15 , decimal_places=2)
    TAXE_EXIGIBLE = models.DecimalField(max_digits=15 , decimal_places=2)
    USED = models.SmallIntegerField(default=0)
    class Meta:
        unique_together = ("ID_DECLARATION","ID_RUBRIQUE")

class CA_Total(models.Model):
    ID_CA_TOTAL = models.BigIntegerField(primary_key=True)
    ID_FORMULAIRE = models.ForeignKey(Form_TVA,on_delete=models.CASCADE)
    CODE_CA_TOTAL = models.IntegerField()
    LIB_CA_TOTAL = models.CharField(max_length=255)
    PRECISION_CA_TOTAL = models.CharField(max_length=1024)
    LIB_CA_TOTAL_AR  = models.CharField(max_length=255)
    def __str__(self):
        return str(self.ID_FORMULAIRE)

class Montant_CA(models.Model):
    ID_CA_TOTAL = models.ForeignKey(CA_Total,on_delete=models.CASCADE)
    ID_DECLARATION = models.ForeignKey(Declaration,on_delete=models.CASCADE)
    MNT_CA = models.DecimalField(max_digits=15,decimal_places=2)
    USED = models.SmallIntegerField(default=0)
    class Meta :
        unique_together = ("ID_CA_TOTAL","ID_DECLARATION")
    def __str__(self):
        return str(self.MNT_CA)

class Montant_Bilan(models.Model):
    ID_BILAN = models.BigIntegerField()
    ID_DECLARATION = models.ForeignKey(Declaration,on_delete=models.CASCADE)
    MNT_BILAN = models.DecimalField(max_digits=15,decimal_places=2)
    USED = models.SmallIntegerField(default=0)
    class Meta:
        unique_together = ("ID_BILAN","ID_DECLARATION")
    def __int__(self):
        return str(self.ID_BILAN)


class Releve_Deduction(models.Model):
    ID_DECLARATION = models.ForeignKey(Declaration,on_delete=models.CASCADE,primary_key=True)
    RELEVE_DEDUCTION = models.FileField()
    IS_VALID = models.SmallIntegerField()
    def __str__(self):
        return str(self.RELEVE_DEDUCTION)
class Releve_deduction_edi(models.Model):
    ID = models.BigIntegerField(primary_key=True)
    #NUM_ORDRE = models.BigIntegerField()
    #NUM_FACTURE = models.CharField(max_length=250)
    #DATE_FACTURE = models.DateField()
    #DESIGNATION_BIEN_SERVICE = models.CharField(max_length=256,default='')
    MONTANT_HT = models.FloatField()
    MONTANT_TVA = models.FloatField()
    MONTANT_TTC = models.FloatField()
    #TAUX = models.FloatField()
    #REF_MODE_PAIEMENT = models.BigIntegerField()
    #DATE_PAIEMENT = models.DateField()
    ID_DECLARATION = models.BigIntegerField()
    #NOM_FOURNISSEUR = models.CharField(max_length=250)
    #IF_FOURNISSEUR = models.CharField(max_length=8)
    #ICE_FOURNISSEUR = models.CharField(max_length=16)
    #ID_TRACE = models.BigIntegerField()
    #PRORATA = models.FloatField()
    #MONTANT_TVA_PRORATA = models.FloatField()
    #DATE_TRANSFERT_METIER = models.DateTimeField(auto_now_add=True)
    def __str__(self):
            return str(self.ID)

class Designation(models.Model):
    Designation = models.CharField(max_length=255,default='')
    ID_DESIGNATION = models.BigIntegerField(primary_key=True)
    ID_RELEVE = models.ForeignKey(Releve_deduction_edi, on_delete=models.CASCADE)
    MONTANT_HT = models.FloatField()
    MONTANT_TTC = models.FloatField()

    def __str__(self):
        return str(self.ID_DESIGNATION)