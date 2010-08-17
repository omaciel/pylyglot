# vim: ts=4 sw=4 expandtab ai
# -*- encoding: utf-8 -*-

"""

From Django Snippets: http://djangosnippets.org/snippets/2058/
This is the local_settings.py trick extended to Django templates.

Sometimes you need to insert some arbitrary code in the HTML of the production site for external service integration like uservoice, typekit, google analytics... You don't want to put this code into source control because some other sites using the same source code may not need it.

So, add this template tag to your collection and do:

{% try_to_include 'head.html' %}
And leave head.html out of source control. Then when you need to include some code on your production site, just add the head.html template with the desired code to include.

I usually have one included template in the header for extra <head> tags, and one in the footer for extra javascript.

Node that the included template is rendered against the current context. If the template doesn't exist, an empty string is returned.
"""

from django import template

register = template.Library()


class IncludeNode(template.Node):
    def __init__(self, template_name):
        self.template_name = template_name

    def render(self, context):
        try:
            # Loading the template and rendering it
            included_template = template.loader.get_template(
                    self.template_name).render(context)
        except template.TemplateDoesNotExist:
            included_template = ''
        return included_template


@register.tag
def try_to_include(parser, token):
    """Usage: {% try_to_include "head.html" %}

    This will fail silently if the template doesn't exist. If it does, it will
    be rendered with the current context."""
    try:
        tag_name, template_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, \
            "%r tag requires a single argument" % token.contents.split()[0]

    return IncludeNode(template_name[1:-1])
