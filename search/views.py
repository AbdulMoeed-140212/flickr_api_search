from search.models import Favourite
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
import flickrapi
from flickerlocation.settings import FLICKR_API_KEY, FLICKR_API_SECRET
from search.forms import AddtoFavouriteForm
from django.contrib import messages

# Create your views here.
def flickerSearchImage(kwargs):
    flickr = flickrapi.FlickrAPI(FLICKR_API_KEY, FLICKR_API_SECRET, format='parsed-json')
    return flickr.photos.search(**kwargs, per_page=2, extras="url_o,url_w")

class HomePage(TemplateView):
    template_name = "search\index.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        lat = self.request.GET.get('lat')
        lng = self.request.GET.get('lng')
        location = self.request.GET.get('location')
        page = self.request.GET.get('page', 1)
        params = ""
        if lat and lng:
            context["result"] = flickerSearchImage({"lat":lat, "lon":lng, "page":page})
            params = f"/?lat={lat}&lng={lng}"
        elif location:
            context["result"] = flickerSearchImage({"text":location, "page":page})
            params = f"/?location={location}"
        if context.get("result"):
            current_page = context["result"]["photos"]["page"]
            context["query"] = {"lat":lat, "lng": lng, "location":location}
            if current_page != 1:
                context["prev_url"] = params + f"&page={ current_page - 1 }"
            if current_page != context["result"]["photos"]["pages"]:
                context["next_url"] = params + f"&page={ current_page + 1 }"
        
        return context


def add_to_favourite(request):
    try:
        print(request.user.is_authenticated)
        if not request.user.is_authenticated:
            return redirect(reverse( "search:login"))
        else:
            if request.POST:
                form = AddtoFavouriteForm(request.POST)
                if form.is_valid():
                    fav = form.save(commit=False)
                    fav.user = request.user
                    fav.save()
                    messages.success(request, "Image added to Favourites")
                else:
                    messages.error(request, 'Failed to Add Image')
    except Exception as e:
        if "UNIQUE constraint" in e:
            messages.info(request, "Image already saved")
        else:
            messages.error(request, e)
    return redirect(reverse( "search:home_page"))


class FavouritesPage(ListView,LoginRequiredMixin):

    model = Favourite
    paginate_by =10
    template_name="search/favourite.html"

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)