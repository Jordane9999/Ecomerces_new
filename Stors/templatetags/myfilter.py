from django  import template 

# Enregistrer dans la library des filtre
register = template.Library()

# Premier filtre
@register.simple_tag(name="multiplication")
def multiplication(a, b, *args, **kwargs):
    return a * b
