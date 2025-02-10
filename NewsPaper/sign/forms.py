from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm

class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group, created = Group.objects.get_or_create(name='common')
        user.groups.add(common_group)
        
        return user