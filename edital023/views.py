from django.shortcuts import render, redirect, get_object_or_404
from edital023.forms import CidadaoCreationForm, AcessarForm, EsqueciForm, AgendamentoForm
from django.contrib import messages
from edital023.models import autenticar
from edital023.decorators import cidadao_is_anonymous, cidadao_is_authenticated


def home(request):

    return render(request, 'edital023/home.html')


def sair(request):
    request.session['cidadao_pk'] =  None
    messages.add_message(request, messages.SUCCESS, f'Você saiu com sucesso.')
    return redirect('home')


@cidadao_is_anonymous
def esqueci(request):
    if request.method == 'POST':
        form = EsqueciForm(request.POST)
        if form.is_valid():
            email  = form.cleaned_data.get('email')
            messages.add_message(
                request, messages.SUCCESS, 
                f'Isto não é um requisito, ou seja, não foi implementado. Caso contrário seria enviado um email para {email}.'
            )
        form = EsqueciForm()
    else:
        form = EsqueciForm()
    return render(request, 'edital023/esqueci.html', {'form': form})


@cidadao_is_anonymous
def acessar(request):
    # HU#4.CA#01
    if request.method == 'POST':
        form = AcessarForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            raw_senha = form.cleaned_data.get('senha')
            if autenticar(request, email, raw_senha):
                return redirect('home')
            else:
                messages.add_message(request, messages.ERROR, f'Usuário e senha não conferem.')

    form = AcessarForm()
    return render(request, 'edital023/acessar.html', {'form': form})


@cidadao_is_anonymous
def cadastro(request):
    if request.method == 'POST':
        form = CidadaoCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_senha = form.cleaned_data.get('password')
            autenticar(request, email, raw_senha)
            # HU#3.CA#03
            messages.add_message(
                request, messages.SUCCESS, 
                f'Cadastro realizado com sucesso. Você já pode agendar sua vacinação clicando em agendar.'
            )
            return redirect('home')
        else:
            # TODO HU#3.CA#02
            pass
    form = CidadaoCreationForm()
    return render(request, 'edital023/cadastro.html', {'form': form})


@cidadao_is_authenticated
def agendar(request):
    if request.method == 'POST':
        from edital023.models import Agendamento, LocalVacinacao, GrupoAtendimento
        form = AgendamentoForm(request.POST)
        # HU#5.CA#01
        # HU#6.CA#01
        # HU#6.CA#02
        agendamento = Agendamento()
        agendamento.onde = LocalVacinacao.objects.get(pk=form.data['onde'])
        agendamento.quando = form.data['data'] + ' ' + form.data['hora']
        agendamento.quem = request.cidadao
        agendamento.porque = GrupoAtendimento.objects.get(pk=form.data['porque'])
        agendamento.save()
        messages.add_message(
            request, messages.SUCCESS, 
            f'Agendamento salvo com sucesso. Você não poderá fazer novo agendamento. Aproveite para imprimir e guardar seu comprovante.'
        )
        return redirect('comprovante')
        # return render(request, 'edital023/comprovante.html', {'instance': agendamento})
    else:
        form = AgendamentoForm()
    return render(request, 'edital023/agendar.html', {'form': form})


@cidadao_is_authenticated
def comprovante(request):
    print(request.cidadao.agendamento)
    return render(request, 'edital023/comprovante.html')
