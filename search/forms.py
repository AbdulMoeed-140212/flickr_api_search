from search.models import Favourite
from django.forms import ModelForm

class AddtoFavouriteForm(ModelForm):
    
    class Meta:
        model=Favourite
        fields=["image_id","url_m","url_original"]