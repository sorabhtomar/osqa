# -*- coding: utf-8 -*-
import json
import logging

from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from forum.modules import ui, decorate
from forum.settings import ONLINE_USERS
from forum.views.render import render_response

def login_required(func, request, *args, **kwargs):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('auth_signin'))
    else:
        return func(request, *args, **kwargs)

def render(template=None, tab=None, tab_title='', weight=500, tabbed=True, parent_template=None, pjax_parent=None, page_template=None):
    def decorator(func):        
        def decorated(context, request, *args, **kwargs):
            if request.user.is_authenticated():
                ONLINE_USERS[request.user] = datetime.now()

            if isinstance(context, HttpResponse):
                return context

            if tab is not None:
                context['tab'] = tab

            return render_response(context.pop('template',template), context, request, parent_template, pjax_parent, page_template)

        if tabbed and tab and tab_title:
            ui.register(ui.PAGE_TOP_TABS,
                        ui.PageTab(tab, tab_title, lambda: reverse(func.__name__), weight=weight))
            
        return decorate.result.withfn(decorated, needs_params=True)(func)

    return decorator

class CommandException(Exception):
    pass

class RefreshPageCommand(HttpResponse):
    def __init__(self):
        super(RefreshPageCommand, self).__init__(
                content=json.dumps({'commands': {'refresh_page': []}, 'success': True}),
                mimetype="application/json")

def command(func, request, *args, **kwargs):
    try:
        response = func(request, *args, **kwargs)

        if isinstance(response, HttpResponse):
            return response

        response['success'] = True
    except Exception, e:
        import traceback
        #traceback.print_exc()

        if isinstance(e, CommandException):
            response = {
            'success': False,
            'error_message': e.message
            }
        else:
            logging.exception("%s: %s" % (func.__name__, str(e)))
            response = {
            'success': False,
            'error_message': _("We're sorry, but an unknown error ocurred.<br />Please try again in a while.")
            }

    if request.is_ajax():
        return HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

