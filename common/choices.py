from django.utils.translation import gettext_lazy as _

class ModelChoices:
    AVANCE = 'avance'
    PAID = 'paid'
    DETTE = 'dette'
    DEPENSE = 'depense'
    CREDIT = 'credit'
    

    KYC_STATUS = (
        (AVANCE, _('Avance')),
        (PAID, _('Paid')),
        (DETTE, _('Dette')),
        (DEPENSE, _('Depense')),
        (CREDIT, _('Credit'))
    )
    
    IMMEUBLE = 'immeuble'
    MEUBLE = 'meuble'
    BUREAUTIQUE = 'bureautique'
    INFORMATIQUE = 'informatique'
    ENGINS_ROULANT = 'engins_roulant'
    
    
    
    CATEGORIES_PATRIMOINES = (
        (IMMEUBLE, _('Immeuble')),
        (MEUBLE, _('Meuble')),
        (BUREAUTIQUE, _('Bureautique')),
        (INFORMATIQUE, _('Informatique')),
        (ENGINS_ROULANT, _('Engins Roulant'))
    )
    
    NEUF = 'neuf'
    BON = 'bon'
    MAUVAIS = 'mauvais'
    DECLASSE = 'declasse'
    
    STATUS_PATRIMOINES = (
        (NEUF, _('Neuf')),
        (BON, _('Bon')),
        (MAUVAIS, _('Mauvais')),
        (DECLASSE, _("Declassé"))
    )
    
    US = 'US'
    CDF = 'CDF'
    BIF = 'BIF'
    
    DEVISE_STATUS = (
        (US, _('US')),
        (CDF, _('CDF')),
        (BIF, _('BIF'))
    )
    
    # Convenience references for units for plan recurrence billing
    # ----------------------------------------------------------------------------
    ONCE = '0'
    SECOND = '1'
    MINUTE = '2'
    HOUR = '3'
    DAY = '4'
    WEEK = '5'
    MONTH = '6'
    YEAR = '7'
    RECURRENCE_UNIT_CHOICES = (
        (MONTH, 'month'),
        (YEAR, 'year'),
    )