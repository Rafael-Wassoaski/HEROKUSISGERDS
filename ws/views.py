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

def relatorio(request):
	from reportlab.lib.units import cm
	from reportlab.lib.pagesizes import A4
	from textwrap import wrap
	from reportlab.pdfbase import pdfmetrics
	from reportlab.pdfbase.ttfonts import TTFont

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=relatorio.pdf'
	p = canvas.Canvas(response, pagesize = A4)
	#pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
	#p.setFont("Arial", 8)
	p.drawString(6.8*cm, 28.5*cm, "ESTADO DE SANTA CATARINA")
	p.drawString(6.8*cm, 28*cm, "SECRETARIA DE ESTADO DA DEFESA CIVIL")
	p.drawString(6.8*cm, 27.5*cm, "COORDENADORIA REGIONAL DE DEFESA CIVIL")
	p.drawCentredString(11*cm, 25.5*cm, "RELATÓRIO CIRCUNSTANCIADO Nº           ")
	p.line(6.7*cm, 25*cm, 15.5*cm, 25*cm)
	p.drawString(4*cm, 24*cm, "Identificação")
	uf = "a"
	municipio = "b"
	coderec = "c"
	p.drawString(4*cm, 23.5*cm, "UF: %s Municipio: %s CODEREC: %s" % (uf,municipio,coderec))
	p.drawString(4*cm, 23*cm, "Tipologia do Desastre")
	cobrade = "a"
	descricao = "b"
	data = "c"
	hora = "c"
	p.drawString(4*cm, 22.5*cm, "COBRADE: %s Descricao: %s Data: %s Hora: %s" % (cobrade,descricao,data, hora))
	descricao = "ajsndjasjdnasjdashjhfsdhbfhjasdhjfsdbfsdhjfbhjasdbhjfbhsdbfhjsdbhjfbhasdbfhbsdhbfhjasdhjfsdfhjbasdfhjsdbhjfbhjsdbfhbsdhfbhsdbfhjsdbfhsdfbsdhjfbsdhjfbsdhjfbsdhbcsbvhbbbbbbbbbbbbbb"
	p.drawString(4*cm, 22*cm, "Descricao: ")
	wraped_text = '\n'.join(wrap(descricao, 20)) 
	p.drawString(6*cm, 22*cm, wraped_text)
	p.drawString(4*cm, 21.5*cm, "Avaliacao de Danos e Prejuizos")
	p.drawString(4*cm, 21*cm, "DANOS HUMANOS                                                                                                        SIM  NAO  QUANTIDADE")
	p.drawString(4*cm, 20.5*cm, "Desalojados")
	p.drawString(4*cm, 20*cm, "Desabrigados")
	p.drawString(4*cm, 19.5*cm, "Desaparecidos")
	p.drawString(4*cm, 19*cm, "Feridos")
	p.drawString(4*cm, 18.5*cm, "Enfermos")
	p.drawString(4*cm, 18*cm, "Mortos")
	p.drawString(4*cm, 17.5*cm, "Isolados")
	p.drawString(4*cm, 17*cm, "Atingidos")
	p.drawString(4*cm, 16.5*cm, "Afetados")
	p.drawString(4*cm, 15*cm, "Observacoes")
	p.line(4*cm, 14.5*cm, 18*cm, 14.5*cm)
	p.line(4*cm, 14*cm, 18*cm, 14*cm)
	p.line(4*cm, 13.5*cm, 18*cm, 13.5*cm)

	p.drawString(4*cm, 13*cm, "DANOS MATERIAIS                                                                                                        SIM  NAO  QUANTIDADE")
	p.drawString(4*cm, 12.5*cm, "Unidades Habitacionais Atingidas")
	p.drawString(4*cm, 12*cm, "Unidades Habitacionais Danificadas")
	p.drawString(4*cm, 11.5*cm, "Unidades Habitacionais Interditadas")
	p.drawString(4*cm, 11*cm, "Unidades Habitacionais Destruidas")
	p.drawString(4*cm, 10.5*cm, "Instalacoes Publicas de Saude Atingidas/Danificadas/Destruidas")
	p.drawString(4*cm, 10*cm, "Instalacoes Publicas de Ensino Atingidas/Danificadas/Destruidas")
	p.drawString(4*cm, 9.5*cm, "Instalacoes Publicas de uso Comunitario Atingidas/Danificadas/Destruidas")
	p.drawString(4*cm, 9*cm, "Obras de Infraestrutura Publica Danificada/Destruida")
	p.drawString(4*cm, 8.5*cm, "Interrupcao de Servicos Essenciais")
	p.drawString(4*cm, 7*cm, "Observacoes")
	p.line(4*cm, 6.5*cm, 18*cm, 6.5*cm)
	p.line(4*cm, 6*cm, 18*cm, 6*cm)
	p.line(4*cm, 5.5*cm, 18*cm, 5.5*cm)

	p.line(4*cm, 4.5*cm, 18*cm, 4.5*cm)
	p.drawCentredString(11*cm, 4*cm, "SECRETARIA DE ESTADO DA DEFESA CIVIL")
	p.drawCentredString(11*cm, 3.5*cm, "Rua Ivo Silveira, 2320 - Capoeiras | CEP 88.085-001 | Florianopolis - SC")
	p.drawCentredString(11*cm, 3*cm, "www.defesacivil.sc.gov.br")
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
			nomeArq = '{}{}.jpg'.format(vistoria.id, vistoria.cobrad)
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
