from django.db.models import Sum
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from .forms import EcartForm, DesignationForm , CreditForm
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        username = request.user.get_username
        context = {"username": username}
        return render(request, 'MyApp/home.html', context)
    else:
        username = "SE CONNECTER "
        context = {"username": username}
        return render(request, 'MyApp/home.html', context)

def ecart_dd_df(request):
    if request.user.is_authenticated:
        username = request.user.get_username
        submitbutton = request.POST.get("submit")
        form = EcartForm(request.POST) #instantiation du  formulaire
        if form.is_valid():
            year = form.cleaned_data["year"]
            start = form.cleaned_data["start"]
            end = form.cleaned_data["end"]
            direction = form.cleaned_data["direction"]
            """ filtres """
            """ cette requete pour extraire le nom de client"""
            adherent = Adherent.objects.filter(CODE_DIRECTION=direction).values()#cette ligne utiliser comme filte pour les requets suivvantes 
            direction_filter = Adherent.objects.filter(CODE_DIRECTION=direction)
            declaration_filtré = Declaration.objects.filter(ANNEE_DECLAR=year, DATE_DEPOT=start,ID_ADHERENT__in=direction_filter).values()#les enregistrement des declaration qui verifient toutes les conditions
            filtre_adhent = Declaration.objects.filter(ANNEE_DECLAR=year, DATE_DEPOT=start,ID_ADHERENT__in=direction_filter).values_list('ID_ADHERENT')#les id des adhrent  qui verifient les conditions
            adherent1 = Adherent.objects.filter(ID_ADHERENT__in = filtre_adhent).values()#les adherent qui verifient tous les conditions

            if declaration_filtré == {} :
                msg = "les données saisis n'existent pas"
                context = {'msg':msg}
                return render(request, 'MyApp/ecart_dd_df.html', context)
            else:
                """ recuperer la valeur de la somme des deduction : tva_deductible """
                """" calculer combientt de declaration verifi les conditions des filtres """
                count_declaration = 0#calculer combientt de declaration verifi les conditions des filtres
                deductions_liste = []#liste qui affiche la somme de deduction de chaque declaration
                liste_declarations = []#liste affiche le detail de toute les declarations qui verifient les conditions
                """ calculer la somme des tva deductibl de chaque declaration """
                declaration_deductions = {}#le dictionaire qui va contenir les declarations et leurs somme de deduction
                declaration_releve = {}#le dictionnaire qui contient chaque declaration avec la somme de tous ses releve de deduction
                deduction_edi_list = []
                liste_resultat = {}
                for declaration in declaration_filtré:
                    count_declaration = count_declaration + 1
                    declaration_id = declaration['ID_DECLARATION']
                    #liste_declarations.append(declaration)
                    formulaires = Form_TVA.objects.filter(ID_FORMULAIRE=declaration['ID_FORMULAIRE'])
                    liste_declarations.append(formulaires)
                    typeteaux = TYPE_TAUX.objects.filter(ID_FORMULAIRE__in = formulaires)
                    liste_declarations.append(typeteaux)
                    rubrique = Rubrique.objects.filter(CODE_RUBRIQUE=10, ID_TYPE_TAUX__in=typeteaux)
                    liste_declarations.append(rubrique)
                    deduction = Deduction.objects.filter(ID_RUBRIQUE__in= rubrique).aggregate(Sum('TVA_DEDUCTIBL'))
                    somme_deduction = deduction['TVA_DEDUCTIBL__sum'] # recupperer lla valeur de la somme  car la requete deeduction est sous forme de declaration_deductionsionnaire
                    deductions_liste.append(deduction)
                    deductions_liste.append(deduction)
                    paire_deduction = {declaration_id:somme_deduction} # le paire qui contientt l'id du declaration avec la somme de c'est deduction
                    declaration_deductions.update(paire_deduction)# ajouter le paire de chaque declaration à un declaration_deductionsionaire
                    """ recueperere les releve_deduction_edi de chaque declaration """
                    deduction_edi = Releve_deduction_edi.objects.filter(ID_DECLARATION = declaration['ID_DECLARATION']).aggregate(Sum('MONTANT_TVA'))
                    somme_montant_tva = deduction_edi['MONTANT_TVA__sum']
                    deduction_edi_list.append(deduction_edi)
                    paire_releve = {declaration_id:somme_montant_tva}#le paire contient l'id du declaration avec la somme des releve de deduction
                    declaration_releve.update(paire_releve) #ajouter le paire
                    """ calcul de la difference """
                    commentaire_liste = []
                    for key in declaration_deductions :
                        for key1 in declaration_releve :
                            if key1 == key:
                                resultat = declaration_deductions[key] - declaration_releve[key1]
                                paire_resultat = {key: resultat}
                                liste_resultat.update(paire_resultat)
                                """ verifier si c'est fraud """
                                if resultat > 100:
                                    commentaire_liste.append("ANOMALIE")
                                elif resultat < 0:
                                    commentaire_liste.append("ERREUR")
                                else :
                                    commentaire_liste.append("VALIDE")
                    """  creer des liste pour simplifier l'affichage pour l'affichage """

                    deduction = []
                    for key1 in declaration_releve:
                        deduction.append(declaration_releve[key1])
                    ecart = []
                    for key in liste_resultat:
                        ecart.append(liste_resultat[key])
                    total_deduction = []
                    for key2 in declaration_deductions:
                        total_deduction.append(declaration_deductions[key2])
                context = {'submitbutton': submitbutton,'username':username,
                           'adherent1':adherent1,'declaration_filtré':declaration_filtré,'deduction':deduction,'ecart':ecart,'commentaire_liste':commentaire_liste}
                return render(request, 'MyApp/ecart_dd_df.html', context)
        context = {}
        return render(request, 'MyApp/ecart_dd_df.html', context)
    else:
         """ Envoyer l'utilisateur a la page de login """
         return redirect(to=reverse('admin:login'))

def activite_contribuable (request) :
    if request.user.is_authenticated:
        submitbutton = request.POST.get("submit")
        myform = DesignationForm(request.POST)
        if myform.is_valid():
            client_name = myform.cleaned_data["client_name"]
            client_id = myform.cleaned_data["client_id"]
            direction = myform.cleaned_data["direction"]
            """FILTRES"""
            """recuperer l'id du client a partir de son nom"""
            ID_CLIENT = Adherent.objects.filter(NOM_PRENOM_RS = client_name).filter(ID_ADHERENT=client_id).filter(CODE_DIRECTION=direction)
            """recupperer l'id de declaration a partir du id adherent"""
            ID_DECLARATION  = Declaration.objects.filter(ID_ADHERENT__in=ID_CLIENT).values_list('ID_DECLARATION')
            """recupperer la liste des releves qui appartient à l'utlisateur demandé"""
            """ cette requete pour pouvoir recuperer lesreleve id dans le template"""
            RELEVE1 = Releve_deduction_edi.objects.filter(ID_DECLARATION__in=ID_DECLARATION).values()
            """ cette requete utilise comme filtre pour la requete suivante """
            RELEVE = Releve_deduction_edi.objects.filter(ID_DECLARATION__in = ID_DECLARATION).values_list('ID')
            """ cette requete pour recuperere les designations """
            designation = Designation.objects.filter(ID_RELEVE__in = RELEVE).values()
            liste_designation  = [] # la liste qui contient les nom des designations
            liste_id_designation = [] #contient les id des designations pour pouvoir recupperer les liens qui mene aux factures de designation
            liste_id_releve = [] # l'id des releve
            liste = []
            for d in designation:
                liste_designation.append(d.get('Designation'))
                liste_id_designation.append(d.get('ID_DESIGNATION'))
            for r in RELEVE1 :
                liste_id_releve.append(r['ID'])
            context = {"submitbutton":submitbutton, "client_name": client_name,
                       "ID_DECLARATION":ID_DECLARATION,"RELEVE":RELEVE,
                       "RELEVE1":RELEVE1,"designation":designation,
                       'liste_designation':liste_designation,'liste_id_designation':liste_id_designation
                        ,'liste_id_releve':liste_id_releve,'liste':liste,'ID_CLIENT':ID_CLIENT}
            return render(request,"MyApp/activite_contribuable.html",context)
        context = {}
        return render(request,'MyApp/activite_contribuable.html',context)
    else:
        """si l'user n'est pas connecté il va l'envoyer à la page de connexion """
        return redirect(to=reverse('admin:login'))

def comparaison_credit(request):
    if request.user.is_authenticated:
        submitbutton = request.POST.get("submit")
        myform = CreditForm(request.POST)
        if myform.is_valid():
            annee_depot = myform.cleaned_data["annee_depot"]
            nom_client = myform.cleaned_data["client_name"]
            id_client = myform.cleaned_data["client_id"]
            clients =  Adherent.objects.filter(ID_ADHERENT = id_client).filter(NOM_PRENOM_RS=nom_client)
            declarations = Declaration.objects.filter(ID_ADHERENT__in = clients).filter(ANNEE_DECLAR = annee_depot).values()
            credit_declare = [] #liste contient des paires chaque paire est sous forme de  id de declaration avec la valeur de  son  credit
            for d in declarations :
                paire = {d['ID_DECLARATION']:d['MNT_CREDIT']}
                credit_declare.append(paire)

            context = {"submitbutton":submitbutton,'declarations':declarations,'clients':clients,'credit_declare':credit_declare}
            return render(request,"MyApp/comparaison_credit.html",context)
        context = {}
        return render(request, "MyApp/comparaison_credit.html", context)
    else:
        """si l'user n'est pas connecté il va l'envoyer à la page de connexion """
        return redirect(to=reverse('admin:login'))


