from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from toktok.redirect_mixins import RedirectMixin
from toktok.apps.storemanagerapp import models as store_manager_models

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class IsStoreManagerMixin(RedirectMixin):
    def test_func(self):
        return store_manager_models.StoreManagerBasicDetail.objects.filter(manager=self.request.user).exists()


