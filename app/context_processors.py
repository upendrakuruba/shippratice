from category.models import *
from store.models import *
def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)

