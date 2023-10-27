from django import template

register = template.Library()

@register.filter
def has_role(user, roles):
    role_names = user.roles.all().values_list("nombre", flat=True)
    return any(role in role_names for role in roles.split(','))
