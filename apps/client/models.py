# coding=utf-8
import datetime
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from apps.city.models import City, Surface
from core.files import upload_to
from core.models import User

__author__ = 'alexy'


class Client(models.Model):
    class Meta:
        verbose_name = u'Клиент'
        verbose_name_plural = u'Клиенты'
        app_label = 'client'

    def __unicode__(self):
        return self.legal_name

    user = models.OneToOneField(to=User, verbose_name=u'Пользователь')
    city = models.ForeignKey(to=City, verbose_name=u'Город')
    legal_name = models.CharField(max_length=256, blank=True, null=True, verbose_name=u'Юридическое название')
    actual_name = models.CharField(max_length=256, blank=True, null=True, verbose_name=u'Фактичексое название')
    inn = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'ИНН')
    kpp = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'КПП')

    ogrn = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'ОГРН')
    bank = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'Банк')
    bik = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'БИК')
    account = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'Расчётный счёт')
    account_cor = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'Кор. счёт')
    signer_post_dec = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'должность подписанта')
    signer_name_dec = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'имя подписанта')
    signer_doc_dec = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'действует на основании')

    legal_address = models.TextField(verbose_name=u'Физический адрес', blank=True, null=True)
    leader = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'Руководитель')
    leader_function = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'Должность руководителя')
    work_basis = models.CharField(max_length=256, blank=True, null=True, verbose_name=u'Основание для работы')


class ClientSurface(models.Model):
    class Meta:
        verbose_name = u'Рекламная поверхность'
        verbose_name_plural = u'Рекламные поверхности'
        app_label = 'client'
        ordering = ['-date', ]

    def __unicode__(self):
        return u'%s %s ' % (self.surface.street.name, self.surface.house_number)

    client = models.ForeignKey(to=Client, verbose_name=u'Клиент')
    surface = models.ForeignKey(to=Surface, verbose_name=u'Рекламная поверхность')
    date = models.DateField(verbose_name=u'Дата заказа', default=datetime.date.today())
    date_end = models.DateField(verbose_name=u'Дата заказа', blank=True, null=True)


class ClientMaket(models.Model):
    class Meta:
        verbose_name = u'Макет'
        verbose_name_plural = u'Макеты'
        app_label = 'client'
        ordering = ['-date']

    def __unicode__(self):
        return self.name

    client = models.ForeignKey(to=Client, verbose_name=u'Клиент')
    name = models.CharField(max_length=256, verbose_name=u'Название')
    file = models.FileField(verbose_name=u'Файл макета', upload_to=upload_to)
    date = models.DateField(verbose_name=u'Дата размещения макета')
