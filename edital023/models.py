import hashlib
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.db.models import Model
from django.db.models import CharField, PositiveSmallIntegerField, DateField, EmailField, DateTimeField
from django.db.models import ForeignKey, CASCADE

class Municipio(Model):
    cod_munic = CharField("Código", max_length=6, primary_key=True)
    dsc_cidade = CharField("Nome", max_length=250)
    uf = CharField("UF", max_length=2, choices=[
        ('RO', 'RO'), ('AC', 'AC'), ('AM', 'AM'), ('RR', 'RR'), ('PA', 'PA'), ('AP', 'AP'), ('TO', 'TO'),
        ('MA', 'MA'), ('PI', 'PI'), ('CE', 'CE'), ('RN', 'RN'), ('PB', 'PB'), ('PE', 'PE'), ('AL', 'AL'), ('SE', 'SE'), ('BA', 'BA'),
        ('MG', 'MG'), ('ES', 'ES'), ('RJ', 'RJ'), ('SP', 'SP'),
        ('PR', 'PR'), ('SC', 'SC'), ('RS', 'RS'),
        ('MS', 'MS'), ('MT', 'MT'), ('GO', 'GO'), ('DF', 'DF')
    ])

    class Meta:
        verbose_name = "Município"
        verbose_name_plural = "Municípios"

    def __str__(self):
        return f"{self.dsc_cidade} ({self.cod_munic})"


class LocalVacinacao(Model):
    # HU#1.CA#01
    vlr_latitude = CharField("Latitude", max_length=20)
    vlr_longitude = CharField("Longitude", max_length=20)
    municipio = ForeignKey(Municipio, verbose_name="Município", on_delete=CASCADE)
    cod_cnes = CharField("CNES", max_length=7)
    nom_estab = CharField("Nome", max_length=250)
    dsc_endereco = CharField("Logradouro", max_length=250)
    dsc_bairro = CharField("Bairro", max_length=250)
    dsc_telefone = CharField("Telefone", max_length=250, null=True, blank=True)
    dsc_estrut_fisic_ambiencia = CharField("Estutura física ambiencia?", max_length=250)
    dsc_adap_defic_fisic_idosos = CharField("Adaptado para deficiêntes físicos ou idosos?", max_length=250)
    dsc_equipamentos = CharField("Equipamentos", max_length=250)
    dsc_medicamentos = CharField("Medicamentos", max_length=250)

    class Meta:
        verbose_name = "Local de vacinação"
        verbose_name_plural = "Locais de vacinação"

    def __str__(self):
        return self.nom_estab


class GrupoAtendimento(Model):
    # HU#2.CA#01
    nome = CharField("Nome", max_length=250)
    idade_minima = PositiveSmallIntegerField("Idade mímina")

    class Meta:
        verbose_name = "Grupo atendimento"
        verbose_name_plural = "Grupos de atendimento"

    def __str__(self):
        return self.nome


class Cidadao(Model):
    # HU#3
    nome = CharField("Nome completo", max_length=250)
    nascimento = DateField("Data de nascimento")
    email = EmailField("Email")
    senha = CharField('Senha', max_length=128)

    class Meta:
        verbose_name = "Cidadão"
        verbose_name_plural = "Cidadãos"

    def __str__(self):
        return self.nome

    def set_password(self, clean_password):
        self.senha = make_password(clean_password)

    @property
    def is_authenticated(self):
        return True

    @property
    def has_agendamento(self):
        return Agendamento.objects.filter(quem=self).exists()

    @property
    def agendamento(self):
        return Agendamento.objects.filter(quem=self).first()


class CidadaoAnonimo(object):
    def __init__(self):
        super().__init__()
        self.nome = "Anonimo"
        self.nascimento = None
        self.email = None
        self.senha = None

    @property
    def is_authenticated(self):
        return False

    @property
    def has_agendamento(self):
        return False


def autenticar(request, email, raw_senha):
    cidadao = Cidadao.objects.filter(email=email).first()
    if cidadao and check_password(raw_senha, cidadao.senha):
        request.session['cidadao_pk'] = cidadao.pk
        return True
    return False


class Agendamento(Model):
    # HU#5
    quem = ForeignKey(Cidadao, verbose_name="Cidadão", on_delete=CASCADE)
    quando = DateTimeField("Para quando")
    onde = ForeignKey(LocalVacinacao, verbose_name="Local de vacinação", on_delete=CASCADE)
    porque = ForeignKey(GrupoAtendimento, verbose_name="Grupo de atendimento", on_delete=CASCADE)
    comprovante = CharField("Comprovante", max_length=250)

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"

    def __str__(self):
        return f"{self.quem.pk}.{self.quando}.{self.onde.pk}.{self.porque.pk}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.comprovate = hashlib.sha256(f"{settings.SITE_URL}{self.quem.pk}.{self.quando}.{self.onde.pk}.{self.porque.pk}".encode('utf-8'))
        super().save(force_insert, force_update, using, update_fields)

    @property
    def is_authenticated(self):
        return True
