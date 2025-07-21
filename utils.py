# context_processors.py
from home.models import SocialLinks

def templates_data(request):
    links = SocialLinks.objects.all()
    
    return{
        'links':links,
    }
     


