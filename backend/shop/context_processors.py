from .models import Category

def categories(request):
    """
    A context processor that returns a list of top level categories.

    Categories are fetched from the database and are available as a variable
    named 'categories' in every template.
    """
    categories = Category.objects.filter(parent=None)
    return {'categories': categories}