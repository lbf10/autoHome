from django.conf import settings
from django.db import models
from django.utils import timezone

class Saida(models.Model):
    ON = True
    OFF = False
    UNKNOWN = None 
    STATES = (
        (ON, 'Ligado'),
        (OFF, 'Desligado'),
        (UNKNOWN, 'Desconhecido'),
    )

    name = models.CharField(max_length=64,unique=True,verbose_name="Nome")
    gpioPort = models.IntegerField(unique=True,verbose_name="Porta")
    state = models.BooleanField(verbose_name="Estado",choices=STATES,default=UNKNOWN,null=True,blank=True)
    
    def turnOn(self):
        self.state = ON
        self.save()

    def turnOff(self):
        self.state = OFF
        self.save()

    def __str__(self):
        return self.name

class Sensor(models.Model):
    name = models.CharField(max_length=64,unique=True, verbose_name="Nome")
    gpioPort = models.IntegerField(unique=True,verbose_name="Porta")
    value = models.FloatField(verbose_name = "Valor atual",blank=True)
    max_value = models.FloatField(verbose_name = "Valor de saturacao",blank=True)
    min_value = models.FloatField(verbose_name = "Valor de referencia",blank=True)

    def __str__(self):
        return self.name

class Rotina(models.Model):
    name = models.CharField(max_length=64,verbose_name='Nome')
    output = models.ForeignKey(Saida,on_delete=models.CASCADE,verbose_name='Saida controlada')
    sensor = models.ForeignKey(Sensor,default=None,on_delete=models.SET_NULL,null=True,blank=True,verbose_name='Sensor de controle')
    sensorControl = models.BooleanField(default=False,verbose_name='Controlado por sensor?')
    mon = models.BooleanField(default=False,verbose_name='Segunda-Feira')
    tue = models.BooleanField(default=False,verbose_name='Terca-Feira')
    wed = models.BooleanField(default=False,verbose_name='Quarta-Feira')
    thu = models.BooleanField(default=False,verbose_name='Quinta-Feira')
    fri = models.BooleanField(default=False,verbose_name='Sexta-Feira')
    sat = models.BooleanField(default=False,verbose_name='Sabado')
    sun = models.BooleanField(default=False,verbose_name='Domingo')
    startHour = models.TimeField(verbose_name='Inicio',null=True,blank=True)
    endHour = models.TimeField(verbose_name='Fim',null=True,blank=True)
    threshold = models.FloatField(null=True,default=0,verbose_name='Valor de ativacao',blank=True)
    
    COMPARISON_MODES = (
        ('>', 'Maior que'),
        ('<', 'Menor que'),
    )

    comparison = models.CharField(max_length=1,choices=COMPARISON_MODES,verbose_name='Modo de comparacao do sensor com valor de ativacao',blank=True)

    ACTIVATION_MODES = (
        (True, 'Ligar'),
        (False, 'Desligar'),
    )
    activation = models.BooleanField(default=True,choices=ACTIVATION_MODES,verbose_name='Acao de ativacao do sensor',blank=True)

    def __str__(self):
        return self.name
