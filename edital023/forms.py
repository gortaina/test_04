from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, CharField, PasswordInput, DateField, TimeField, ChoiceField
from django.core.exceptions import ValidationError
from django_select2.forms import ModelSelect2Widget
from edital023.models import Cidadao, Agendamento, LocalVacinacao


class EsqueciForm(ModelForm):
    class Meta:
        model = Cidadao
        fields = ["email"]


# class LocalVacinacaoWidget(s2forms.ModelSelect2Widget):
#     search_fields = [
#         "nom_estab__icontains",
#     ]

class AgendamentoForm(ModelForm):
    data = DateField()
    hora = TimeField()
    onde = ChoiceField(
        label="Local de vacinação",
        widget=ModelSelect2Widget(
            model=LocalVacinacao,
            search_fields=['nom_estab__icontains'],
        )
    )
    class Meta:
        model = Agendamento
        # TODO HU#5.CA#02
        fields = ["data", "hora", "onde", "porque"]


class AcessarForm(ModelForm):
    # # HU#4.CA#01
    senha = CharField(
        label=_("Senha"),
        widget=PasswordInput(),
    )
    class Meta:
        model = Cidadao
        fields = ["email", "senha"]


class CidadaoCreationForm(ModelForm):
    # HU#3.CA#01
    error_messages = {
        'password_mismatch': _('As duas senhas têm que ser iguais'),
    }
    password = CharField(
        label=_("Senha"),
        widget=PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    confirmPassword = CharField(
        label=_("Confirmar senha"),
        widget=PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    class Meta:
        model = Cidadao
        fields = ["nome", "nascimento", "email"]
        # field_classes = {'username': UsernameField}

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self._meta.model.USERNAME_FIELD in self.fields:
    #         self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    def confirm_password_clean(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return confirm_password

    # def _post_clean(self):
    #     super()._post_clean()
    #     password = self.cleaned_data.get('confirmPassword')
    #     if password:
    #         try:
    #             password_validation.validate_password(password, self.instance)
    #         except ValidationError as error:
    #             self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
