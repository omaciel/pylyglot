# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai
#
# This file is part of Pylyglot.
#
# Pylyglot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pylyglot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pylyglot.  If not, see <http://www.gnu.org/licenses/>.

from SimpleXMLRPCServer import SimpleXMLRPCDispatcher

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from core.models import Language, Package, Translation

try:
    rpc_dispatcher = SimpleXMLRPCDispatcher(allow_none=False, encoding=None)
except Exception, e:
    rpc_dispatcher = SimpleXMLRPCDispatcher()

@csrf_exempt
def rpc_service(request):
    if request.method == 'POST':
        response = HttpResponse(mimetype='text/xml')
        response.write(rpc_dispatcher._marshaled_dispatch(request.raw_post_data))
    else:
        methods = []

        for method in rpc_dispatcher.system_listMethods():
            method_help = rpc_dispatcher.system_methodHelp(method)

            methods.append({
                'name': method,
                'help': method_help
            })

        return render_to_response('rpc_service/rpc.html', {'methods': methods},
                                  context_instance=RequestContext(request))

    response['Content-length'] = str(len(response.content))
    return response

def get_status():
    """ Returns a "key -> value" structure with Pylyglot stats.

    Keys:
        total_packages -- Number of registered packages.
        total_languages -- Number of registered languages.
        total_translations - Number of registered translations.

    """
    return {
        'total_packages': Package.objects.count(),
        'total_languages': Language.objects.count(),
        'total_translations': Translation.objects.count()
    }

def get_languages():
    """ Returns a "key->value" structure with both short and long names of the
    registered languages.

    Keys:
        long_name -- Full name (e.g., Brazilian Portuguese, English, French)
        short_name -- Abbreviated name (e.g., pt_BR, en, fr)

    """
    languages = []
    for language in Language.objects.all():
        languages.append({
            'long_name': language.long_name or '',
            'short_name': language.short_name,
        })

    return languages

def get_translation(language, term):
    """
    Arguments:
        language -- Translated term language.
        term -- Term to translate.

    Keys of the structure returned:
        original -- The original untranslated message.
        translation -- Translated term.
        packages -- Packages that contain the original message.

    """
    result = []

    translations = Translation.objects.filter(
            sentence__msgid__icontains=term,
            language__short_name=language,
            obsolete=False,
            ).values(
                    'sentence__msgid',
                    'msgstr',
                    'sentence__length',
                    ).order_by(
                            'sentence__length',
                            'sentence__msgid',
                            'msgstr'
                            ).distinct()

    for translation in translations:
        # I don't like this but for now it's ok
        packages = Translation.objects.filter(
                language__short_name=language,
                sentence__msgid=translation['sentence__msgid']
                ).order_by(
                        'package__name'
                        )
        result.append({
            'original': translation['sentence__msgid'],
            'translation': translation['msgstr'],
            'packages': [x.package.name for x in packages],
        })

    return result

rpc_dispatcher.register_function(get_translation)
rpc_dispatcher.register_function(get_languages)
rpc_dispatcher.register_function(get_status)
