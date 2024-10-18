from django.contrib.auth.views import PasswordContextMixin, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from unfold.sites import UnfoldAdminSite
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from unfold.widgets import INPUT_CLASSES

class UnfoldViewMixin(PasswordContextMixin):
    def get_context_data(self, **kwargs):
        unfold_context = UnfoldAdminSite().each_context(self.request)
        # only use a subset
        extra_context = {
            'form_classes': unfold_context.get('form_classes'),
            'site_logo': unfold_context.get('site_logo'),
            'site_icon': unfold_context.get('site_icon'),
            'site_symbol': unfold_context.get('site_symbol'),
            'site_favicons': unfold_context.get('site_favicons'),
            'colors': unfold_context.get('colors'),
            'styles': unfold_context.get('styles'),
            'theme': unfold_context.get('theme'),
        }
        return super().get_context_data(
            **kwargs,
            **extra_context,
        )

class UnfoldPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs["class"] = " ".join(INPUT_CLASSES)
class UnfoldPasswordResetView(UnfoldViewMixin, PasswordResetView):
    form_class = UnfoldPasswordResetForm

class UnfoldPasswordResetDoneView(UnfoldViewMixin, PasswordResetDoneView):
    pass

class UnfoldSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["new_password1"].widget.attrs["class"] = " ".join(INPUT_CLASSES)
        self.fields["new_password2"].widget.attrs["class"] = " ".join(INPUT_CLASSES)
class UnfoldPasswordResetCompleteView(UnfoldViewMixin, PasswordResetCompleteView):
    form_class = UnfoldSetPasswordForm

class UnfoldPasswordResetConfirmView(UnfoldViewMixin, PasswordResetConfirmView):
    pass