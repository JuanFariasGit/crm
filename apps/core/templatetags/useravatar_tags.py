from django import template

from apps.profile.models import Profile

register = template.Library()

@register.filter('user_avatar')
def user_avatar(user):
    profile = Profile.objects.filter(user=user).first()
    if profile:
        return profile.avatar.url
    return
