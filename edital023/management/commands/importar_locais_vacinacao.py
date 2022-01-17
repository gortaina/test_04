import csv, os
from os.path import dirname
from django.core.management.base import BaseCommand
from edital023.models import Municipio, LocalVacinacao, GrupoAtendimento


EDITAL023_DIR = dirname(dirname(dirname(__file__)))
FIXTURES_DIR = f"{EDITAL023_DIR}/fixtures"
FIXTURES_FILE = f"{FIXTURES_DIR}/ubs.csv"
UFS = {
    '11': 'RO',
    '12': 'AC',
    '13': 'AM',
    '14': 'RR',
    '15': 'PA',
    '16': 'AP',
    '17': 'TO',
    '21': 'MA',
    '22': 'PI',
    '23': 'CE',
    '24': 'RN',
    '25': 'PB',
    '26': 'PE',
    '27': 'AL',
    '28': 'SE',
    '29': 'BA',
    '31': 'MG',
    '32': 'ES',
    '33': 'RJ',
    '35': 'SP',
    '41': 'PR',
    '42': 'SC',
    '43': 'RS',
    '50': 'MS',
    '51': 'MT',
    '52': 'GO',
    '53': 'DF',
}


class Command(BaseCommand):
    help = 'Importa Municipios e LocalVacinacao de edital023/fixture/ubs.csv'

    def handle(self, *args, **options):

        print(f"Lendo {FIXTURES_FILE}...")
        print(f"Municipio...")
        municipios_lidos = {}
        with open(FIXTURES_FILE) as csvfile:
            for row in csv.DictReader(csvfile, delimiter=',', quotechar='"'):
                # Municipio.objects.get_or_create(codigo=row.pop("codigo"), defaults=row)
                municipios_lidos[row['cod_munic']] = {'cidade': row['dsc_cidade'], 'id': None}

        for cod_munic, dados in municipios_lidos.items():
            id, created = Municipio.objects.get_or_create(cod_munic=cod_munic, defaults={"uf": UFS[cod_munic[:2]], "dsc_cidade": dados['cidade']})
            municipios_lidos[cod_munic]['id'] = id

        print("OK", len(municipios_lidos), '.')

        print("LocalVacinacao... ", end='', flush=True)
        i = 0
        with open(FIXTURES_FILE) as csvfile:
            LocalVacinacao.objects.all().delete()
            for row in csv.DictReader(csvfile, delimiter=',', quotechar='"'):
                i += 1
                if i % 1000 == 0:
                    print(i, end=" ", flush=True)
                LocalVacinacao.objects.create(
                    cod_cnes=row['cod_cnes'],
                    **{
                        "vlr_latitude": row['vlr_latitude'],
                        "vlr_longitude": row['vlr_longitude'],
                        "municipio": municipios_lidos[row['cod_munic']]['id'],
                        "nom_estab": row['nom_estab'],
                        "dsc_endereco": row['dsc_endereco'],
                        "dsc_bairro": row['dsc_bairro'],
                        "dsc_telefone": row['dsc_telefone'],
                        "dsc_estrut_fisic_ambiencia": row['dsc_estrut_fisic_ambiencia'],
                        "dsc_adap_defic_fisic_idosos": row['dsc_adap_defic_fisic_idosos'],
                        "dsc_equipamentos": row['dsc_equipamentos'],
                        "dsc_medicamentos": row['dsc_medicamentos'],
                    }
                )
                # LocalVacinacao.objects.get_or_create(
                #     cod_cnes=row['cod_cnes'],
                #     defaults={
                #         "vlr_latitude": row['vlr_latitude'],
                #         "vlr_longitude": row['vlr_longitude'],
                #         "municipio": municipios_lidos[row['cod_munic']]['id'],
                #         "nom_estab": row['nom_estab'],
                #         "dsc_endereco": row['dsc_endereco'],
                #         "dsc_bairro": row['dsc_bairro'],
                #         "dsc_telefone": row['dsc_telefone'],
                #         "dsc_estrut_fisic_ambiencia": row['dsc_estrut_fisic_ambiencia'],
                #         "dsc_adap_defic_fisic_idosos": row['dsc_adap_defic_fisic_idosos'],
                #         "dsc_equipamentos": row['dsc_equipamentos'],
                #         "dsc_medicamentos": row['dsc_medicamentos'],
                #     }
                # )
                # UF.objects.get_or_create(sigla=row.pop("sigla"), defaults=row)
                # ufs = {u.codigo: u.pk for u in UF.objects.all()}
        print("OK", i, '.')

        print("GrupoAtendimento... ", end='', flush=True)
        GrupoAtendimento.objects.all().delete()
        GrupoAtendimento.objects.create(nome="Maiores de 65", idade_minima=65)
        GrupoAtendimento.objects.create(nome="Entre 40 e 64", idade_minima=40)
        GrupoAtendimento.objects.create(nome="Entre 18 e 40", idade_minima=18)
        GrupoAtendimento.objects.create(nome="Até 17", idade_minima=0)
        print("OK", 4, '.')
