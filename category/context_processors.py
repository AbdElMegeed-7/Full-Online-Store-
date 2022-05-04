from .models import Category


def menu_links(request):
    """
        Use Context_processors to make the Function Available in all the templates
    """
    links = Category.objects.all()
    return dict(links=links)
