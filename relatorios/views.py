from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from random import *
from django.contrib import messages

from django.core.mail import send_mail, BadHeaderError

from .models import Vistoria

class simpleVistoria:
	"""docstring for simpleVistoria"""
	def __init__(self, autor):
		self.autor = autor
		self.cobrad = 0
		self.municipios = "Nao informado"
		self.descricao = "Nao informado"
		self.descDesastre = "Nao informado"
		self.data = "Nao informado"
		self.hora = "Nao informado"
		self.endereco = "Nao informado"
		self.dataDesastre = "Nao informado"

		self.danos_humanos_desalojados = 0
		self.danos_humanos_desabrigados = 0
		self.danos_humanos_desaparecidos = 0
		self.danos_humanos_feridos = 0
		self.danos_humanos_enfermos = 0
		self.danos_humanos_mortos = 0
		self.danos_humanos_isolados = 0
		self.danos_humanos_atingidos = 0
		self.danos_humanos_afetados = 0 

		self.danos_humanos_desalojados_bool = False
		self.danos_humanos_desabrigados_bool = False
		self.danos_humanos_desaparecidos_bool = False
		self.danos_humanos_feridos_bool = False
		self.danos_humanos_enfermos_bool = False
		self.danos_humanos_mortos_bool = False
		self.danos_humanos_isolados_bool = False
		self.danos_humanos_atingidos_bool = False
		self.danos_humanos_afetados_bool = False
		self.danos_humanos_observacoes = "Nao informado"

		self. unidades_habitacionais_atingidas =  0
		self. unidades_habitacionais_danificads = 0
		self. unidades_habitacionais_interditadas = 0
		self. unidades_habitacionais_destruidas = 0
		self. instalacoes_publicas_saude_atingidas = 0
		self. instalacoes_publicas_ensino_atingidas = 0
		self. instalacoes_comunitarias_atingidas = 0
		self. obras_atingidas = 0
		self. interrupcoes_servicos_essenciais = 0

		self. unidades_habitacionais_atingidas_bool = False
		self. unidades_habitacionais_danificads_bool = False
		self. unidades_habitacionais_interditadas_bool = False
		self. unidades_habitacionais_destruidas_bool = False
		self. instalacoes_publicas_saude_atingidas_bool = False
		self. instalacoes_publicas_ensino_atingidas_bool = False
		self. instalacoes_comunitarias_atingidas_bool = False
		self. obras_atingidas_bool = False
		self. interrupcoes_servicos_essenciais_bool = False
		self.danos_materiais_observacoes = "Nao informado"

		self.contaminacao_solo = 0
		self.contaminacao_agua = 0
		self.contaminacao_ar = 0

		self.contaminacao_solo_bool = False
		self.contaminacao_agua_bool = False
		self.contaminacao_ar_bool = False
		self.danos_ambientais_observacoes = "Nao informado"

		self.danos_agricultura = 0
		self.danos_pecuaria = 0
		self.danos_industria = 0
		self.danos_comercio = 0
		self.danos_prestacao_de_servicos = 0

		self.danos_agricultura_bool = False
		self.danos_pecuaria_bool = False
		self.danos_industria_bool = False
		self.danos_comercio_bool = False
		self.danos_prestacao_de_servicos_bool = False
		self.danos_economicos_observacoes = "Nao informado"

		self.iah_bool = False

		self.iah_cestas_de_alimentos = 0
		self.iah_agua_potavel = 0
		self.iah_colchoes = 0
		self.iah_kit_higiene_pessoal = 0
		self.iah_kit_limpeza = 0
		self.iah_telhas = 0
		self.iah_lona_plastica = 0
		self.iah_outros = 0


		self.iah_cestas_de_alimentos_bool = False
		self.iah_agua_potavel_bool = False
		self.iah_colchoes_bool = False
		self.iah_kit_higiene_pessoal_bool = False
		self.iah_kit_limpeza_bool = False
		self.iah_telhas_bool = False
		self.iah_lona_plastica_bool = False
		self.iah_outros_bool = False

		self.iah_fornecidos_outros_observacoes = "Nao informado"
		self.iah_vias_publicas_totalmente_desobistruidas = False
		self.iah_reestabelecimento_servicos_essenciais = False

		self.deferido = False

@login_required
def deferir(request, pk):
	print('ola')
	vistoria = Vistoria.objects.get(pk=pk)
	vistoria.deferido  = True
	vistoria.save()
	return vistoriadetalhes(request, pk)

@login_required
def indeferir(request, pk):
        vistoria = Vistoria.objects.get(pk=pk)
        vistoria.deferido  = False
        vistoria.save()
        return vistoriadetalhes(request, pk)	

@login_required
def vistoria_pdf(request, pk):
	vistoria = Vistoria.objects.get(pk = pk)
	vistoriaSimples = simpleVistoria(vistoria.autor)
	vistoriaSimples.cobrade = vistoria.cobrade
	vistoriaSimples.municipios = vistoria.municipios
	vistoriaSimples.descricao = vistoria.descricao
	dataHora = vistoria.dataDesastre.split(';')
	vistoriaSimples.data = dataHora[0]
	vistoriaSimples.hora = dataHora[1]
	vistoriaSimples.descDesastre = vistoria.descricaoDesastre
	vistoriaSimples.endereco = vistoria.endereco
	vistoriaSimples.dataDesastre = vistoria.dataDesastre

	#danos humanos

	if(vistoria.danos_humanos_desalojados > 0):
		vistoriaSimples.danos_humanos_desalojados = vistoria.danos_humanos_desalojados
		vistoriaSimples.danos_humanos_desalojados_bool = True

	if(vistoria.danos_humanos_desabrigados > 0):
		vistoriaSimples.danos_humanos_desabrigados = vistoria.danos_humanos_desabrigados
		vistoriaSimples.danos_humanos_desabrigados_bool = True

	if(vistoria.danos_humanos_desaparecidos > 0):
		vistoriaSimples.danos_humanos_desaparecidos = vistoria.danos_humanos_desaparecidos
		vistoriaSimples.danos_humanos_desaparecidos_bool = True

	if(vistoria.danos_humanos_feridos > 0):
		vistoriaSimples.danos_humanos_feridos = vistoria.danos_humanos_feridos
		vistoriaSimples.danos_humanos_feridos_bool = True

	if(vistoria.danos_humanos_enfermos > 0):
		vistoriaSimples.danos_humanos_enfermos = vistoria.danos_humanos_enfermos
		vistoriaSimples.danos_humanos_enfermos_bool = True

	if(vistoria.danos_humanos_mortos > 0):
		vistoriaSimples.danos_humanos_mortos = vistoria.danos_humanos_mortos
		vistoriaSimples.danos_humanos_mortos_bool = True

	if(vistoria.danos_humanos_isolados > 0):
		vistoriaSimples.danos_humanos_isolados = vistoria.danos_humanos_isolados
		vistoriaSimples.danos_humanos_isolados_bool = True

	if(vistoria.danos_humanos_atingidos > 0):
		vistoriaSimples.danos_humanos_atingidos = vistoria.danos_humanos_atingidos
		vistoriaSimples.danos_humanos_atingidos_bool = True

	if(vistoria.danos_humanos_afetados > 0):
		vistoriaSimples.danos_humanos_afetados = vistoria.danos_humanos_afetados
		vistoriaSimples.danos_humanos_afetados_bool = True

	vistoriaSimples.danos_humanos_observacoes = vistoria.danos_humanos_observacoes


	#danos materiais

	if(vistoria.unidades_habitacionais_atingidas > 0):
		vistoriaSimples.unidades_habitacionais_atingidas = vistoria.unidades_habitacionais_atingidas
		vistoriaSimples.unidades_habitacionais_atingidas_bool = True

	if(vistoria.unidades_habitacionais_danificads > 0):
		vistoriaSimples.unidades_habitacionais_danificads = vistoria.unidades_habitacionais_danificads
		vistoriaSimples.unidades_habitacionais_danificads_bool = True

	if(vistoria.unidades_habitacionais_interditadas > 0):
		vistoriaSimples.unidades_habitacionais_interditadas = vistoria.unidades_habitacionais_interditadas
		vistoriaSimples.unidades_habitacionais_interditadas_bool = True

	if(vistoria.unidades_habitacionais_destruidas > 0):
		vistoriaSimples.unidades_habitacionais_destruidas = vistoria.unidades_habitacionais_destruidas
		vistoriaSimples.unidades_habitacionais_destruidas_bool_bool = True

	if(vistoria.instalacoes_publicas_saude_atingidas > 0):
		vistoriaSimples.instalacoes_publicas_saude_atingidas = vistoria.instalacoes_publicas_saude_atingidas
		vistoriaSimples.instalacoes_publicas_saude_atingidas_bool = True

	if(vistoria.instalacoes_publicas_ensino_atingidas > 0):
		vistoriaSimples.instalacoes_publicas_ensino_atingidas = vistoria.instalacoes_publicas_ensino_atingidas
		vistoriaSimples.instalacoes_publicas_ensino_atingidas_bool = True

	if(vistoria.instalacoes_comunitarias_atingidas > 0):
		vistoriaSimples.instalacoes_comunitarias_atingidas = vistoria.instalacoes_comunitarias_atingidas
		vistoriaSimples.instalacoes_comunitarias_atingidas_bool = True

	if(vistoria.obras_atingidas > 0):
		vistoriaSimples.obras_atingidas = vistoria.obras_atingidas
		vistoriaSimples.obras_atingidas_bool = True

	if(vistoria.interrupcoes_servicos_essenciais > 0):
		vistoriaSimples.interrupcoes_servicos_essenciais = vistoria.interrupcoes_servicos_essenciais
		vistoriaSimples.interrupcoes_servicos_essenciais_bool = True

	vistoriaSimples.danos_materiais_observacoes = vistoria.danos_materiais_observacoes

	#danos ambientais

	if(vistoria.contaminacao_solo > 0):
		vistoriaSimples.contaminacao_solo = vistoria.contaminacao_solo
		vistoriaSimples.contaminacao_solo_bool = True

	if(vistoria.contaminacao_agua > 0):
		vistoriaSimples.contaminacao_agua = vistoria.contaminacao_agua
		vistoriaSimples.contaminacao_agua_bool = True

	if(vistoria.contaminacao_ar > 0):
		vistoriaSimples.contaminacao_ar = vistoria.contaminacao_ar
		vistoriaSimples.contaminacao_ar_bool = True

	vistoriaSimples.danos_ambientais_observacoes = vistoria.danos_ambientais_observacoes

	#danos economicos

	if(vistoria.danos_agricultura > 0):
		vistoriaSimples.danos_agricultura = vistoria.danos_agricultura
		vistoriaSimples.danos_agricultura_bool = True

	if(vistoria.danos_pecuaria > 0):
		vistoriaSimples.danos_pecuaria = vistoria.danos_pecuaria
		vistoriaSimples.danos_pecuaria_bool = True

	if(vistoria.danos_industria > 0):
		vistoriaSimples.danos_industria = vistoria.danos_industria
		vistoriaSimples.danos_industria_bool = True

	if(vistoria.danos_comercio > 0):
		vistoriaSimples.danos_comercio = vistoria.danos_comercio
		vistoriaSimples.danos_comercio_bool = True

	if(vistoria.danos_prestacao_de_servicos > 0):
		vistoriaSimples.danos_prestacao_de_servicos = vistoria.danos_prestacao_de_servicos
		vistoriaSimples.danos_prestacao_de_servicos_bool = True

	vistoriaSimples.danos_economicos_observacoes = vistoria.danos_economicos_observacoes

	#iah

	if(vistoria.iah_cestas_de_alimentos > 0):
		vistoriaSimples.iah_cestas_de_alimentos = vistoria.iah_cestas_de_alimentos
		vistoriaSimples.iah_cestas_de_alimentos_bool = True
		vistoriaSimples.iah_bool = True

	if(vistoria.iah_agua_potavel > 0):
		vistoriaSimples.iah_agua_potavel = vistoria.iah_agua_potavel
		vistoriaSimples.iah_agua_potavel_bool = True
		vistoriaSimples.iah_bool = True

	if(vistoria.iah_colchoes > 0):
		vistoriaSimples.iah_colchoes = vistoria.iah_colchoes
		vistoriaSimples.iah_colchoes_bool = True
		vistoriaSimples.iah_bool = True

	if(vistoria.iah_kit_higiene_pessoal > 0):
		vistoriaSimples.iah_kit_higiene_pessoal = vistoria.iah_kit_higiene_pessoal
		vistoriaSimples.iah_kit_higiene_pessoal_bool = True
		vistoriaSimples.iah_bool = True

	if(vistoria.iah_kit_limpeza > 0):
		vistoriaSimples.iah_kit_limpeza = vistoria.iah_kit_limpeza
		vistoriaSimples.iah_kit_limpeza_bool = True
		vistoriaSimples.iah_bool = True

	if(vistoria.iah_telhas > 0):
		vistoriaSimples.iah_telhas = vistoria.iah_telhas
		vistoriaSimples.iah_telhas_bool = True
		vistoriaSimples.iah_bool = True

	if(vistoria.iah_lona_plastica > 0):
		vistoriaSimples.iah_lona_plastica = vistoria.iah_lona_plastica
		vistoriaSimples.iah_lona_plastica_bool = True
		vistoriaSimples.iah_bool = True

	if(vistoria.iah_outros > 0):
		vistoriaSimples.iah_outros = vistoria.iah_outros
		vistoriaSimples.iah_outros_bool = True
		vistoriaSimples.iah_bool = True

	vistoriaSimples.iah_fornecidos_outros_observacoes = vistoria.iah_fornecidos_outros_observacoes
	vistoriaSimples.iah_vias_publicas_totalmente_desobistruidas = vistoria.iah_vias_publicas_totalmente_desobistruidas
	if(vistoria.iah_vias_publicas_totalmente_desobistruidas):
		vistoriaSimples.iah_vias_publicas_totalmente_desobistruidas = True
	if(vistoria.iah_reestabelecimento_servicos_essenciais):
		vistoriaSimples.iah_reestabelecimento_servicos_essenciais = True

	print(vistoriaSimples.iah_vias_publicas_totalmente_desobistruidas)
	vistoriaSimples.deferido = vistoria.deferido

	return render(request, 'relatorios/relatorio.html', {'vistoria': vistoriaSimples})
	


@login_required
def todasvistorias(request):
	vistorias = Vistoria.objects.filter(data__lte=timezone.now()).order_by('-data')
	return render(request, 'relatorios/vistorias.html', {'vistorias':vistorias})

@login_required
def minhasvistorias(request):
	if request.user.is_superuser:
		 vistorias = Vistoria.objects.filter(data__lte=timezone.now()).order_by('-data')
	else:
		vistorias = Vistoria.objects.filter(autor=request.user, data__lte=timezone.now()).order_by('-data')
	return render(request, 'relatorios/minhas_vistorias.html', {'vistorias':vistorias})

def ajuda(request):
	return render(request, '../templates/ajuda/Ajuda.html', {})

@login_required
def vistoriadetalhes(request, pk):
	vistoria = get_object_or_404(Vistoria, pk=pk)
	if request.user == vistoria.autor:
		can_edit = True
	else:
		can_edit = False
	if request.user.is_superuser:
		can_validate = True
	else:
		can_validate = False
	return render(request, 'relatorios/vistoria_detalhes.html', {'vistoria':vistoria, 'can_edit':can_edit, 'can_validate':can_validate})
