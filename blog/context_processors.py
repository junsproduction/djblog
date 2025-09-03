from .models import Category

def blog_context(request):
    """
    Global context processor for blog-related data
    """
    try:
        categories = Category.objects.all()
        return {
            'categories': categories,
        }
    except Exception as e:
        # Return empty context on error
        return {
            'categories': [],
        }
