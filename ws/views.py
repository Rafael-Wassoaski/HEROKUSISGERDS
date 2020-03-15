from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import VistoriaSerializer
from django.contrib.auth import authenticate
from relatorios.models import Vistoria
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
import json, base64
from django.core.files.base import ContentFile
from django.core import serializers
from accounts.models import CustomUser
import reportlab
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from PIL import Image
from base64 import decodestring
from django.core.files.storage import default_storage
from django.conf import settings

def relatorio(request, pk):
	from reportlab.lib.units import cm
	from reportlab.lib.pagesizes import A4
	from textwrap import wrap
	from reportlab.pdfbase import pdfmetrics
	from reportlab.pdfbase.ttfonts import TTFont

	vistoria = Vistoria.objects.get(pk=pk)

	controleLinha = 28.5

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=relatorio.pdf'
	p = canvas.Canvas(response, pagesize = A4)
	#pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
	p.setFont("Helvetica", 8)
	p.drawCentredString(300, controleLinha*cm, "ESTADO DE SANTA CATARINA")
	controleLinha-= 0.5
	p.drawCentredString(300, controleLinha*cm, "SECRETARIA DE ESTADO DA DEFESA CIVIL")
	controleLinha-= 0.5
	p.drawCentredString(300, controleLinha*cm, "COORDENADORIA REGIONAL DE {}".format(vistoria.coordenadoria))
	controleLinha-= 0.5
	p.drawCentredString(300, controleLinha*cm, "RELATÓRIO CIRCUNSTANCIADO Nº{}".format(vistoria.numeroDoRelatorio))
	controleLinha-= 0.5
	controleLinha-= 0.5
	p.drawString(3*cm, controleLinha*cm, "Identificação")
	controleLinha-= 0.5
	uf = vistoria.unidadeFederativa
	municipio = vistoria.municipio
	coderec = vistoria.autor.name
	p.rect(2.96*cm, 25.4*cm, 1.95*cm,  0.5*cm)
	p.rect(4.9*cm, 25.4*cm, 6.8*cm,  0.5*cm)
	p.rect(11.7*cm, 25.4*cm, 8*cm,  0.5*cm)
	p.drawString(3*cm, controleLinha*cm, "UF: %s" % (uf))
	p.drawString(5*cm, controleLinha*cm, "Municipio: %s" % (municipio))
	p.drawString(11.85*cm, controleLinha*cm, "CODEREC: %s" % (coderec))
	controleLinha-= 0.5*2
	p.drawString(3*cm, controleLinha*cm, "Tipologia do Desastre")
	controleLinha-= 0.5
	cobrade = vistoria.cobrade
	descricao = vistoria.descricaoCobrade
	data = vistoria.dataHoraDesastre.split(";")[0];
	hora = vistoria.dataHoraDesastre.split(";")[1];

	p.rect(2.96*cm, (controleLinha-0.2)*cm, 3.7*cm,  0.5*cm)
	p.rect(6.66*cm, (controleLinha-0.2)*cm, 6*cm,  0.5*cm)
	p.rect(12.66*cm, (controleLinha-0.2)*cm, 2.7*cm,  0.5*cm)
	p.rect(15.36*cm, (controleLinha-0.2)*cm, 4.35*cm,  0.5*cm)
	p.drawString(3*cm, controleLinha*cm, "COBRADE: %s" % (cobrade))
	p.drawString(6.7*cm, controleLinha*cm, "Descricao: %s" % (descricao))
	p.drawString(12.7*cm, controleLinha*cm, "Data: %s" % (data))
	p.drawString(15.4*cm, controleLinha*cm, "Hora: %s" % (hora))
	controleLinha-= 0.5*4
	p.drawString(3.1*cm, controleLinha*cm, "Descricao: ")
	controleLinha-= 0.5
	text = p.beginText(3.1*cm,controleLinha*cm)
	descricaoDesastre = []
	descricaoDes = vistoria.descricaoDesastre
			
	descricaoDesastre = descricaoDes.split("\n")
	for line in descricaoDesastre:
		text.textLine(line)
	p.drawText(text)
	#(controleLinha-(len(descricaoDesastre)*0.35))*cm
	controleLinha-= 0.5*len(descricaoDesastre)
	p.rect(2.96*cm, controleLinha*cm , 16.75*cm, 3.5*cm)
	controleLinha-= 0.5*2
	p.drawString(3.1*cm, controleLinha*cm, "Avaliacao de Danos e Prejuizos")
	controleLinha-= 0.5*2

	p.drawString(3.1*cm, (controleLinha+0.4)*cm, "Danos Humanos:")

	controleLinha -=0.5

	sim = ""
	nao = "x"

	if vistoria.quantiadeObitos > 0:
		sim = "X"
		nao = ""

	p.drawString(3.1*cm, controleLinha*cm, "Óbitos relacionados ao desastre")
	p.drawString(11.1*cm, controleLinha*cm, "Sim: {}".format(sim))
	p.drawString(13.1*cm, controleLinha*cm, "Não: {}".format(nao))
	p.drawString(15.1*cm, controleLinha*cm, "Quantidade: {}".format(vistoria.quantiadeObitos))

	p.rect(2.96*cm, (controleLinha-0.15)*cm, 8.04*cm, 0.5*cm)
	p.rect(11*cm, (controleLinha-0.15)*cm, 2*cm, 0.5*cm)
	p.rect(13*cm, (controleLinha-0.15)*cm, 2*cm, 0.5*cm)
	p.rect(15*cm, (controleLinha-0.15)*cm, 4.71*cm, 0.5*cm)

	controleLinha-=0.5*2

	sim = ""
	nao = "X"

	if vistoria.quantiadePopuIsolada > 0:
		sim = "X"
		nao = ""

	p.drawString(3.1*cm, controleLinha*cm, "População isolada pelo desastre")
	p.drawString(11.1*cm, controleLinha*cm, "Sim: {}".format(sim))
	p.drawString(13.1*cm, controleLinha*cm, "Não: {}".format(nao))
	p.drawString(15.1*cm, controleLinha*cm, "Quantidade: {}".format(vistoria.quantiadePopuIsolada))

	p.rect(2.96*cm, (controleLinha-0.15)*cm, 8.04*cm, 0.5*cm)
	p.rect(11*cm, (controleLinha-0.15)*cm, 2*cm, 0.5*cm)
	p.rect(13*cm, (controleLinha-0.15)*cm, 2*cm, 0.5*cm)
	p.rect(15*cm, (controleLinha-0.15)*cm, 4.71*cm, 0.5*cm)

	controleLinha-=0.5*2

	sim = ""
	nao = "X"

	if vistoria.quantidadeDesalojados > 0:
		sim = "X"
		nao = ""

	p.drawString(3.1*cm, controleLinha*cm, "Desalojados/desabrigados")
	p.drawString(11.1*cm, controleLinha*cm, "Sim: {}".format(sim))
	p.drawString(13.1*cm, controleLinha*cm, "Não: {}".format(nao))
	p.drawString(15.1*cm, controleLinha*cm, "Quantidade: {}".format(vistoria.quantidadeDesalojados))

	p.rect(2.96*cm, (controleLinha-0.15)*cm, 8.04*cm, 0.5*cm)
	p.rect(11*cm, (controleLinha-0.15)*cm, 2*cm, 0.5*cm)
	p.rect(13*cm, (controleLinha-0.15)*cm, 2*cm, 0.5*cm)
	p.rect(15*cm, (controleLinha-0.15)*cm, 4.71*cm, 0.5*cm)

	controleLinha-=0.5*2
	afetados = vistoria.populacaoAfetada
	porcentagem = vistoria.porcentagemPopulacaoAfetada
	p.drawString(3.1*cm, controleLinha*cm, "Estimativa da população afetada: {} pessoas, equivalente a {}{} do total de habitantes.".format(afetados, porcentagem, "%"))
	p.rect(2.96*cm, (controleLinha-0.15)*cm, 16.75*cm, 0.5*cm)

	controleLinha-= 0.5
	p.line(2.96*cm, controleLinha*cm, 19.74*cm, controleLinha*cm)
	controleLinha-= 0.5
	p.drawString(3.1*cm, controleLinha*cm, "Danos Materiais:")
	controleLinha-= 0.5*2

	sim = ""
	nao = "X"

	if vistoria.habitacoesAtingidas > 0:
		sim = "X"
		nao = ""
	
	p.drawString(3.1*cm, controleLinha*cm, "Interdição ou destruição de unidades habitacionais")
	p.drawString(11.1*cm, controleLinha*cm, "Sim: {}".format(sim))
	p.drawString(13.1*cm, controleLinha*cm, "Não: {}".format(nao))
	p.drawString(15.1*cm, controleLinha*cm, "Quantidade: {}".format(vistoria.habitacoesAtingidas))

	p.rect(2.96*cm, (controleLinha-0.15)*cm, 8.04*cm, 0.5*cm)
	p.rect(11*cm, (controleLinha-0.15)*cm, 2*cm, 0.5*cm)
	p.rect(13*cm, (controleLinha-0.15)*cm, 2*cm, 0.5*cm)
	p.rect(15*cm, (controleLinha-0.15)*cm, 4.71*cm, 0.5*cm)

	controleLinha-= 0.5*2

	sim = ""
	nao = "X"

	if vistoria.interrupcaoDeServi != "Não afetada":
		sim = "X"
		nao = ""

	p.drawString(3*cm, controleLinha*cm, "Interrupção dos serviços essenciais devido a danificação ou destruição de instalações públicas")
	controleLinha-= 0.5
	p.drawString(3*cm, controleLinha*cm, "prestadores dos serviços (energia, água, ensino, saúde, etc...) ")
	controleLinha-= 0.5
	p.drawString(3*cm, controleLinha*cm, "[{}] SIM [{}] NÃO - Quais: {}".format(sim, nao, vistoria.interrupcaoDeServi))
	controleLinha -= 0.5
	p.rect(2.96*cm, (controleLinha-4)*cm, 16.75*cm, 12.8*cm)

	p.line(3*cm, 3.5*cm, 18.5*cm, 3.5*cm)
	p.drawCentredString(11*cm, 3*cm, "SECRETARIA DE ESTADO DA DEFESA CIVIL")
	p.drawCentredString(11*cm, 2.5*cm, "Rua Ivo Silveira, 2320 - Capoeiras | CEP 88.085-001 | Florianopolis - SC")
	p.drawCentredString(11*cm, 2*cm, "www.defesacivil.sc.gov.br")
	p.showPage()
	
	#fim da pg 1
	controleLinha = 25.5
	p.setFont("Helvetica", 8)

	sim = ""
	nao = "X"

	if vistoria.infraPublica != "Não afetada":
		sim = "X"
		nao = ""

	p.drawString(3.1*cm, controleLinha*cm, "Danificação ou destruição de obras de infraestrutura pública (vias afetadas, pontes, drenagem, etc...)")
	controleLinha-= 0.5
	p.drawString(3.1*cm, controleLinha*cm, "[{}] SIM [{}] NÃO - Quais: {}".format(sim, nao, vistoria.infraPublica))
	controleLinha-=3
	p.rect(2.96*cm, controleLinha*cm, 16.75*cm, 5*cm)

	controleLinha-= 0.5

	sim = ""
	nao = "X"

	if vistoria.economiaPrivada != "Não afetada":
		sim = "X"
		nao = ""

	p.drawString(3.1*cm, controleLinha*cm, "Danos e Prejuízos Econômicos Privados (agricultura, pecuária, indústria, comércio e serviços)")
	controleLinha-= 0.5
	p.drawString(3.1*cm, controleLinha*cm, "[{}] SIM [{}] NÃO - Quais: {}".format(sim, nao, vistoria.economiaPrivada))
	controleLinha-=4
	p.rect(2.96*cm, controleLinha*cm, 16.75*cm, 5*cm)

	controleLinha-= 0.5

	p.drawString(3.1*cm, controleLinha*cm, "Danos Ambientais:")

	controleLinha-= 1

	sim = ""
	nao = "X"

	if vistoria.ambiente != "Não afetada":
		sim = "X"
		nao = ""

	p.drawString(3.1*cm, controleLinha*cm, "Poluição ou contaminação da água, do ar e do solo, diminuição ou exaurimento hídrico e incêndios em APAs ou APPs.")
	controleLinha-= 0.5
	p.drawString(3.1*cm, controleLinha*cm, "[{}] SIM [{}] NÃO - Quais: {}".format(sim, nao, vistoria.ambiente))
	controleLinha-=4
	p.rect(2.96*cm, controleLinha*cm, 16.75*cm, 5*cm)

	controleLinha-= 1

	p.drawString(3.1*cm, controleLinha*cm, "Ações de Socorro, Assistência e Reabilitação realizada pelo município:")

	controleLinha -= 1

	sim = ""
	nao = "X"

	if vistoria.iah != "Não fornecidas":
		sim = "X"
		nao = ""


	p.drawString(3.1*cm, controleLinha*cm, "Fornecimento de IAH:")
	controleLinha-= 0.5
	p.drawString(3.1*cm, controleLinha*cm, "[{}] SIM [{}] NÃO - Quais: {}".format(sim, nao, vistoria.iah))
	controleLinha-=2
	p.rect(2.96*cm, controleLinha*cm, 16.75*cm, 3*cm)

	controleLinha -= 0.5

	sim = ""
	nao = "X"

	if vistoria.desobistrucaoVias > 0:
		sim = "X"
		nao = ""

	p.drawString(3.1*cm, controleLinha*cm, "Desobstrução de vias:")
	controleLinha-= 0.5
	p.drawString(3.1*cm, controleLinha*cm, "[{}] SIM [{}] NÃO - Desobstruído {}{} das vias.".format(sim, nao, vistoria.desobistrucaoVias, "%"))
	controleLinha-=2
	p.rect(2.96*cm, controleLinha*cm, 16.75*cm, 3*cm)

	controleLinha -= 0.5

	sim = ""
	nao = "X"

	if vistoria.desobistrucaoVias != "Não afetada":
		sim = "X"
		nao = ""

	p.drawString(3.1*cm, controleLinha*cm, "Restabelecimento dos serviços essenciais:")
	controleLinha-= 0.5
	p.drawString(3.1*cm, controleLinha*cm, "[{}] SIM [{}] NÃO - Quais: {}.".format(sim, nao, vistoria.desobistrucaoVias))
	controleLinha-=2
	p.rect(2.96*cm, controleLinha*cm, 16.75*cm, 3*cm)

	p.rect(2.96*cm, controleLinha*cm, 16.75*cm, 26.5*cm)

	p.showPage()

	#fim da pg 2

	controleLinha = 28.5
	p.setFont("Helvetica", 8)

	p.drawCentredString(300, controleLinha*cm, "ESTADO DE SANTA CATARINA")
	controleLinha-= 0.5
	p.drawCentredString(300, controleLinha*cm, "SECRETARIA DE ESTADO DA DEFESA CIVIL")
	controleLinha-= 0.5
	p.drawCentredString(300, controleLinha*cm, "COORDENADORIA REGIONAL DE DEFESA CIVIL")
	controleLinha-= 1


	p.drawString(3.1*cm, controleLinha*cm, "Conclusões:")
	controleLinha-= 0.5
	p.drawString(3.1*cm, controleLinha*cm, "Classificação do Desastre")
	p.rect(2.96*cm, (controleLinha-0.15)*cm, 9*cm, 0.5*cm)
	p.rect(11.96*cm, (controleLinha-0.15)*cm, 7.75*cm, 0.5*cm)
	p.drawString(12.1*cm, controleLinha*cm, "Recomendação à homologação")
	controleLinha-= 0.5

	classificacao1 = ""
	classificacao2 = ""
	classificacao3 = ""
	classificacao4 = ""

	if vistoria.classificacao == 0:
		classificacao1 = "X"
	if vistoria.classificacao == 1:
		classificacao2 = "X"
	if vistoria.classificacao == 2:
		classificacao3 = "X"
	if vistoria.classificacao == 3:
		classificacao4 = "X"	



	sim = ""
	nao = ""
	if vistoria.homologacao:
		sim = "X"
	else:
		nao = "X"
	
	p.drawString(3.1*cm, controleLinha*cm, "[{}] Não atende aos critérios de classificação".format(classificacao1))
	p.drawString(12.1*cm, (controleLinha-0.25)*cm, "[{}] Deferimento".format(sim))
	p.rect(2.96*cm, (controleLinha-0.15)*cm, 9*cm, 0.5*cm)
	p.rect(11.96*cm, (controleLinha-0.65)*cm, 7.75*cm, 1*cm)


	controleLinha-=0.5
	p.drawString(3.1*cm, controleLinha*cm, "[{}] Desastre de Nível I – Situação de Emergência".format(classificacao2))
	p.rect(2.96*cm, (controleLinha-0.15)*cm, 9*cm, 0.5*cm)	

	controleLinha-=0.5
	p.drawString(3.1*cm, controleLinha*cm, "[{}] Desastre de Nível II – Situação de Emergência".format(classificacao3))
	p.drawString(12.1*cm, (controleLinha-0.25)*cm, "[{}] Indeferimento".format(nao))
	p.rect(2.96*cm, (controleLinha-0.15)*cm, 9*cm, 0.5*cm)
	p.rect(11.96*cm, (controleLinha-0.65)*cm, 7.75*cm, 1*cm)


	controleLinha-=0.5
	p.drawString(3.1*cm, controleLinha*cm, "[{}] Desastre de Nível III – Estado de Calamidade Pública".format(classificacao4))
	p.rect(2.96*cm, (controleLinha-0.15)*cm, 9*cm, 0.5*cm)	

	controleLinha-=1.5
	p.drawString(3.1*cm, controleLinha*cm, "Informações gerais")
	controleLinha-=0.5

	controleComeco = controleLinha
	
	text = p.beginText(3.5*cm,controleLinha*cm)
	descricaoDesastre = vistoria.infosGerais.split("\n")
	for line in descricaoDesastre:
		text.textLine(line)
	p.drawText(text)

	controleLinha-= 0.5*len(descricaoDesastre)
	p.rect(2.96*cm, controleLinha*cm , 16.75*cm, (controleComeco - controleLinha + 1)*cm)

	controleLinha -=0.5
	p.drawString(3.1*cm, controleLinha*cm , "{}/SC, {}".format(vistoria.municipio, vistoria.dataHoraRegistrado.split()))

	controleLinha -=0.5*4

	p.line(6*cm, controleLinha*cm, 16*cm, controleLinha*cm)
	controleLinha -=0.5
	p.drawString(8.5*cm, controleLinha*cm, "Assinatura do Coordenador Regional")


	p.line(3*cm, 3.5*cm, 18.5*cm, 3.5*cm)
	p.drawCentredString(11*cm, 3*cm, "SECRETARIA DE ESTADO DA DEFESA CIVIL")
	p.drawCentredString(11*cm, 2.5*cm, "Rua Ivo Silveira, 2320 - Capoeiras | CEP 88.085-001 | Florianopolis - SC")
	p.drawCentredString(11*cm, 2*cm, "www.defesacivil.sc.gov.br")

	p.showPage()

	

	p.save()
	return response




# Create your views here.
@csrf_exempt
def loginmobile(request):
	if request.method == 'POST':
		name = request.POST['name']
		password = request.POST['password']
		user=authenticate(username=name, password=password)

		data = None
		if user is not None:
			data = {
				"id": user.id,
				"status": 200
			}
		else:
			data = {
				"status": 404
			}
		return JsonResponse(data)



@api_view(['POST', 'GET'])
@permission_classes((permissions.AllowAny,))	
def cadastrovistoria(request):

	if request.method == 'GET':
		vistorias = Vistoria.objects.all()
		serializer = VistoriaSerializer(vistorias, many=True)
		jason = json.dumps(serializer.data)
		print(jason)

		return JsonResponse(jason, safe=False)

	if request.method == 'POST':
		data = json.loads(request.body.decode('UTF-8'))
		user = CustomUser.objects.get(id = data.get('autor'))
		serializer = VistoriaSerializer(data=data)
		if serializer.is_valid():
			vistoria = serializer.save()
			print(vistoria)
			imagem = base64.b64decode(vistoria.foto)
			nomeArq = '{}{}.jpg'.format(vistoria.id, vistoria.cobrade)
			#path = default_storage.save(settings.MEDIA_ROOT+'/'+nomeArq)
			with open(settings.MEDIA_ROOT+nomeArq, 'wb') as file:
				file.write(imagem)
				 #path = default_storage.save(settings.MEDIA_ROOT+'/'+nomeArq, file)
			with open(settings.MEDIA_ROOT+nomeArq, 'rb') as file:
				vistoria.fotoCompilada.save(nomeArq, file ,save = True)
				vistoria.save()
			data = {
				"status": 200
			}
			
			
			
			return JsonResponse(data)
		return JsonResponse(serializer.errors, status=400)
