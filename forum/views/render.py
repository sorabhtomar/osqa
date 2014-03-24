"""Replacements for django render_to_string and render_to_response to include support for endless pagination and PJAX"""

from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response

def render_response(template, context=None, request=None, parent_template=None, pjax_parent=None, page_template=None):
    if context is None:
        context = {}
    context['parent_template'] = _resolve_parent(request, parent_template, pjax_parent)
    render_template = _resolve_template(context, request, template, page_template)

    return render_to_response(render_template, context, context_instance=RequestContext(request))

def render_string(template, request=None, context=None):
    parent_template = _resolve_parent(request)
    render_context = context
    if render_context is None:
      render_context = {'parent_template': parent_template}
    render_template = _resolve_template(context, request, template)

    return render_to_string(render_template, render_context, RequestContext(request))

def _resolve_parent(request, parent_template=None, pjax_parent=None):
    resolved_parent = None

    # Allow parent templates to be configured in the context
    resolved_parent = parent_template or 'base_content.html'

    # PJAX. Provide pjaxtend style template extension. Assume pjax.html is parent template for PJAX
    # requests unless a parent is specified
    if _isPjax(request):
        if pjax_parent:
            resolved_parent = pjax_parent
        else:
            resolved_parent = 'base_pjax.html' if parent_template == 'base.html' else 'base_content_pjax.html'

    return resolved_parent


def _resolve_template(context, request, template, page_template=None):
    """Endless pagination. If a pagination template is configured add it to the context here and
    check if it should be rendered directly"""
    resolved_template = template
    if context:
        resolved_template = context.pop('template', template)

    if page_template:
        context['page_template'] = page_template

    if request:
        if request.is_ajax() and not _isPjax(request) and page_template is not None:
            resolved_template = page_template

    return resolved_template

def _isPjax(request):
    return request and request.META.get('HTTP_X_PJAX', False)
