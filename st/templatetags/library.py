import os
import Image
from django.template import Library
from oi.settings import MEDIA_ROOT, MEDIA_URL

register = Library()

def thumbnail(file, size='200x200'):
    # defining the size
    x, y = [int(x) for x in size.split('x')]
    # defining the filename and the miniature filename
    basename, format = file.rsplit('.', 1)
    miniature = basename + '_' + size + '.' +  format
    miniature_filename = os.path.join(MEDIA_ROOT, miniature)
    miniature_url = os.path.join(MEDIA_URL, miniature)
    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename):
        print '>>> debug: resizing the image to the format %s!' % size
        filename = os.path.join(MEDIA_ROOT, file)
        image = Image.open(filename)
        image.thumbnail([x, y]) # generate a 200x200 thumbnail
        image.save(miniature_filename, image.format)
    return miniature_url

register.filter(thumbnail)

def paginator(context, adjacent_pages=2):
    """
    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.
    """
    page_numbers = [n for n in \
                    range(context["page"] - adjacent_pages, context["page"] + adjacent_pages + 1) \
                    if n > 0 and n <= context["paginator"].pages]
    return {
        "hits": context["paginator"].hits,
        "page": context["page"],
        "pages": context["pages"],
        "page_numbers": page_numbers,
        "next": context["page"]+1,
        "previous": context["page"]-1,
        "has_next": context["paginator"].has_next_page(context["page"]),
        "has_previous": context["paginator"].has_previous_page(context["page"]-1),
        "show_first": 1 not in page_numbers,
        "show_last": context["pages"] not in page_numbers,
    }

register.inclusion_tag("paginator.html", takes_context=True)(paginator)
