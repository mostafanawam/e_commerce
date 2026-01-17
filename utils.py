# context_processors.py
from home.models import SocialLinks
from settings.models import Settings

def templates_data(request):
    links = SocialLinks.objects.all()
    settings=Settings.objects.get()
    
    return{
        'links':links,
        'settings':settings,
    }
     


