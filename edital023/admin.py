from django.contrib.admin import ModelAdmin, register 
from django.contrib.auth.admin import UserAdmin
from edital023.models import Municipio, LocalVacinacao, GrupoAtendimento, Agendamento
from edital023.models import Cidadao


@register(Municipio)
class MunicipioAdmin(ModelAdmin):
    icon_name = "location_city"
    list_display = ["cod_munic", "dsc_cidade"]


@register(LocalVacinacao)
class LocalVacinacaoAdmin(ModelAdmin):
    # HU#1.CA#01
    icon_name = "local_hospital"
    list_display = ["nom_estab", "dsc_endereco", "dsc_bairro", "municipio"]
    search_fields = ["nom_estab", "dsc_endereco", "dsc_bairro"]
    list_filter = ["municipio", "dsc_estrut_fisic_ambiencia", "dsc_adap_defic_fisic_idosos", "dsc_equipamentos", "dsc_medicamentos"]
    list_select_related = ('municipio',)


@register(GrupoAtendimento)
class GrupoAtendimentoAdmin(ModelAdmin):
    # HU#2.CA#01
    icon_name = "wc"
    list_display = ["nome", "idade_minima"]


@register(Cidadao)
class CidadaoAdmin(ModelAdmin):
    icon_name = "face"
    list_display = ["nome", "nascimento"]
    date_hierarchy = "nascimento"


@register(Agendamento)
class AgendamentoAdmin(ModelAdmin):
    icon_name = "event"
    list_display = ["quem", "quando", "onde", "porque"]
    date_hierarchy = "quando"
