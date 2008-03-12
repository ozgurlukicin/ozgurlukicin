# This is a modified version of Django's generic.pyi, hacky isn't it?

from django.template import loader, RequestContext
from django.http import Http404, HttpResponse
from django.core.paginator import ObjectPaginator, InvalidPage

def object_list(request, queryset, paginate_by=None, page=None,
        allow_empty=True, template_name=None, template_loader=loader,
        extra_context=None, context_processors=None, template_object_name='object',
        mimetype=None):
    if extra_context is None: extra_context = {}
    #queryset = queryset._clone()
    if paginate_by:
        paginator = ObjectPaginator(queryset, paginate_by)
        if not page:
            page = request.GET.get('page', 1)
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.pages
            else:
                # Page is not 'last', nor can it be converted to an int
                raise Http404
        try:
            object_list = paginator.get_page(page_number - 1)
        except InvalidPage:
            if page_number == 1 and allow_empty:
                object_list = []
            else:
                raise Http404
        c = RequestContext(request, {
            '%s_list' % template_object_name: object_list,
            'is_paginated': paginator.pages > 1,
            'results_per_page': paginate_by,
            'has_next': paginator.has_next_page(page_number - 1),
            'has_previous': paginator.has_previous_page(page_number - 1),
            'page': page_number,
            'next': page_number + 1,
            'previous': page_number - 1,
            'last_on_page': paginator.last_on_page(page_number - 1),
            'first_on_page': paginator.first_on_page(page_number - 1),
            'pages': paginator.pages,
            'hits' : paginator.hits,
            'page_range' : paginator.page_range
        }, context_processors)
    else:
        c = RequestContext(request, {
            '%s_list' % template_object_name: queryset,
            'is_paginated': False
        }, context_processors)
        if not allow_empty and len(queryset) == 0:
            raise Http404
    for key, value in extra_context.items():
        if callable(value):
            c[key] = value()
        else:
            c[key] = value
    if not template_name:
        model = queryset.model
        template_name = "%s/%s_list.html" % (model._meta.app_label, model._meta.object_name.lower())
    t = template_loader.get_template(template_name)
    return HttpResponse(t.render(c), mimetype=mimetype)
