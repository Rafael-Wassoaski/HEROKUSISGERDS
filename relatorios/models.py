from django.conf import settings
from django.db import models
from django.utils import timezone


class Vistoria(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'autor_id',  on_delete=models.CASCADE)
    foto = models.TextField(default = 'none')
    fotoCompilada = models.ImageField( null = True, blank = True)
    #tem como fazer com choice
    cobrad = models.CharField(max_length=200)
    municipios = models.TextField()
    #tem como fazer com choice

    descricao = models.TextField()
    data = models.DateTimeField(default=timezone.now)
    endereco = models.TextField()
    dataDesastre = models.TextField()
    descricaoDesastre = models.CharField(max_length=500)
    #latitude e longitude com FloatField ou DecimalField?
    #Danos humanos:

    danos_humanos_desalojados = models.IntegerField(default=0, blank=True)
    danos_humanos_desabrigados = models.IntegerField(default=0, blank=True)
    danos_humanos_desaparecidos = models.IntegerField(default=0, blank=True)
    danos_humanos_feridos = models.IntegerField(default=0, blank=True)
    danos_humanos_enfermos = models.IntegerField(default=0, blank=True)
    danos_humanos_mortos = models.IntegerField(default=0, blank=True)
    danos_humanos_isolados = models.IntegerField(default=0, blank=True)
    danos_humanos_atingidos = models.IntegerField(default=0, blank=True)
    danos_humanos_afetados = models.IntegerField(default=0, blank=True)

    danos_humanos_observacoes = models.TextField(default="Sem Observações", blank=True)

    #Danos materiais:

    unidades_habitacionais_atingidas = models.IntegerField(default=0, blank=True)
    unidades_habitacionais_danificads = models.IntegerField(default=0, blank=True)
    unidades_habitacionais_interditadas = models.IntegerField(default=0, blank=True)
    unidades_habitacionais_destruidas = models.IntegerField(default=0, blank=True)
    instalacoes_publicas_saude_atingidas = models.IntegerField(default=0, blank=True)
    instalacoes_publicas_ensino_atingidas = models.IntegerField(default=0, blank=True)
    instalacoes_comunitarias_atingidas = models.IntegerField(default=0, blank=True)
    obras_atingidas = models.IntegerField(default=0, blank=True)
    interrupcoes_servicos_essenciais = models.IntegerField(default=0, blank=True)

    danos_materiais_observacoes = models.TextField(default="Sem Observações", blank=True)

    #Danos ambientais:

    contaminacao_solo = models.IntegerField(default=0, blank=True)
    contaminacao_agua = models.IntegerField(default=0, blank=True)
    contaminacao_ar = models.IntegerField(default=0, blank=True)

    danos_ambientais_observacoes = models.TextField(default="Sem Observações", blank=True)

    #Danos econômicos:

    danos_agricultura = models.IntegerField(default=0, blank=True)
    danos_pecuaria = models.IntegerField(default=0, blank=True)
    danos_industria = models.IntegerField(default=0, blank=True)
    danos_comercio = models.IntegerField(default=0, blank=True)
    danos_prestacao_de_servicos = models.IntegerField(default=0, blank=True)

    danos_economicos_observacoes = models.TextField(default="Sem Observações", blank=True)

    #IAH

    iah_cestas_de_alimentos = models.IntegerField(default=0, blank=True)
    iah_agua_potavel = models.IntegerField(default=0, blank=True)
    iah_colchoes = models.IntegerField(default=0, blank=True)
    iah_kit_higiene_pessoal = models.IntegerField(default=0, blank=True)
    iah_kit_limpeza = models.IntegerField(default=0, blank=True)
    iah_telhas = models.IntegerField(default=0, blank=True)
    iah_lona_plastica = models.IntegerField(default=0, blank=True)
    iah_outros = models.IntegerField(default=0, blank=True)

    iah_fornecidos_outros_observacoes = models.TextField(default="Sem Observações", blank=True)
    iah_vias_publicas_totalmente_desobistruidas = models.BooleanField(default=False)
    iah_reestabelecimento_servicos_essenciais = models.BooleanField(default=False)

    #Status

    deferido = models.BooleanField(default=False, blank=True)

    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)

    def publish(self):
        self.save()
