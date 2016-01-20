# coding=utf-8
import datetime

import xlwt
from datetime import date
from annoying.decorators import ajax_request
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from apps.city.models import City, Surface
from apps.client.forms import ClientUpdateForm, ClientAddForm, ClientSurfaceAddForm, ClientMaketForm, ClientOrderForm, \
    ClientJournalForm
from core.forms import UserAddForm, UserUpdateForm
from .models import Client, ClientSurface, ClientMaket, ClientOrder, ClientOrderSurface, ClientJournal

__author__ = 'alexy'


def client_add(request):
    context = {}
    if request.method == "POST":
        user_form = UserAddForm(request.POST)
        client_form = ClientAddForm(request.POST, request=request)
        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save(commit=False)
            user.type = 3
            user.save()
            client = client_form.save(commit=False)
            client.user = user
            client.save()
            return HttpResponseRedirect(reverse('client:change', args=(client.id,)))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        user_form = UserAddForm()
        client_form = ClientAddForm(request=request)
    context.update({
        'user_form': user_form,
        'client_form': client_form
    })
    return render(request, 'client/client_add.html', context)


class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.type == 1:
            qs = Client.objects.all()
        elif self.request.user.type == 2:
            qs = Client.objects.filter(city__moderator=user_id)
        else:
            qs = None
        queryset = qs
        if self.request.GET.get('email'):
            queryset = qs.filter(user__email=self.request.GET.get('email'))
        elif self.request.GET.get('legal_name'):
            queryset = qs.filter(legal_name=self.request.GET.get('legal_name'))
        else:
            if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
                queryset = qs.filter(city__id=int(self.request.GET.get('city')))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        user_id = self.request.user.id
        if self.request.user.type == 1:
            city_qs = City.objects.all()
        elif self.request.user.type == 2:
            city_qs = City.objects.filter(moderator=user_id)
        else:
            city_qs = None
        context.update({
            'city_list': city_qs
        })
        if self.request.GET.get('city'):
            context.update({
                'city_id': int(self.request.GET.get('city'))
            })
        return context


def client_update(request, pk):
    context = {}
    client = Client.objects.get(pk=int(pk))
    user = client.user
    success_msg = u''
    error_msg = u''
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password2:
            if password1 == password2:
                user.set_password(password1)
                success_msg = u'Пароль успешно изменён!'
            else:
                error_msg = u'Пароль и подтверждение пароля не совпадают!'
        user_form = UserUpdateForm(request.POST, instance=user)
        client_form = ClientUpdateForm(request.POST, request=request, instance=client)
        if user_form.is_valid() and client_form.is_valid():
            user_form.save()
            client_form.save()
            success_msg += u' Изменения успешно сохранены'
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        user_form = UserUpdateForm(instance=user)
        client_form = ClientUpdateForm(request=request, instance=client)

    context.update({
        'success': success_msg,
        'error': error_msg,
        'user_form': user_form,
        'client_form': client_form,
        'object': client,
        'client': client,
    })
    return render(request, 'client/client_update.html', context)


def client_maket(request, pk):
    context = {}
    client = Client.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    client_maket_form = ClientMaketForm(
        initial={
            'client': client
        }
    )

    context.update({
        'success': success_msg,
        'error': error_msg,
        'client_maket_form': client_maket_form,
        'object': client,
        'client': client,
    })
    return render(request, 'client/client_maket.html', context)


def client_maket_update(request, pk):
    context = {}
    maket = ClientMaket.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    if request.method == 'POST':
        form = ClientMaketForm(request.POST, request.FILES, instance=maket)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('client:maket', args=(maket.client.id,)))
    else:
        form = ClientMaketForm(instance=maket, initial={
            'file': maket.file
        })
    context.update({
        'success': success_msg,
        'error': error_msg,
        'client_maket_form': form,
        'object': maket,
        'client': maket.client
    })
    return render(request, 'client/client_maket_update.html', context)


def client_order(request, pk):
    context = {}
    client = Client.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    if request.method == 'POST':
        form = ClientOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return HttpResponseRedirect(reverse('client:order-update', args=(order.id,)))
    else:
        form = ClientOrderForm(initial={
            'client': client
        })
    context.update({
        'success': success_msg,
        'error': error_msg,
        'client_order_form': form,
        'object': client,
        'client': client
    })
    return render(request, 'client/client_order.html', context)


def client_order_update(request, pk):
    context = {}
    order = ClientOrder.objects.get(pk=int(pk))
    client = order.client
    area_list = client.city.area_set.all()
    success_msg = u''
    error_msg = u''

    if request.method == 'POST':
        form = ClientOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
    else:
        form = ClientOrderForm(instance=order)
    context.update({
        'success': success_msg,
        'error': error_msg,
        'order_form': form,
        'object': order,
        'client': client,
        'area_list': area_list
    })
    return render(request, 'client/client_order_update.html', context)


def client_order_export(request, pk):
    order = ClientOrder.objects.get(pk=int(pk))
    client = order.client
    font0 = xlwt.Font()
    font0.name = 'Calibri'
    font0.height = 220

    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN

    style0 = xlwt.XFStyle()
    style0.font = font0

    style1 = xlwt.XFStyle()
    style1.font = font0
    style1.borders = borders

    wb = xlwt.Workbook()
    ws = wb.add_sheet(u'Заказанные рекламные поверхости')
    ws.write(0, 0, u'Клиент:', style0)
    ws.write(0, 1, u'%s' % client.legal_name, style0)
    ws.write(1, 0, u'Город:', style0)
    ws.write(1, 1, u'%s' % client.city.name, style0)
    ws.write(2, 0, u'Начало размещения:', style0)
    ws.write(2, 1, u'%s' % order.date_start, style0)
    ws.write(3, 0, u'Конец размещения:', style0)
    ws.write(3, 1, u'%s' % order.date_end, style0)

    ws.write(5, 0, u'Город', style1)
    ws.write(5, 1, u'Район', style1)
    ws.write(5, 2, u'Улица', style1)
    ws.write(5, 3, u'Номер дома', style1)
    ws.write(5, 4, u'Количество стендов', style1)

    i = 6
    porch_total = 0
    for item in order.clientordersurface_set.all():
        ws.write(i, 0, item.surface.city.name, style1)
        ws.write(i, 1, item.surface.street.area.name, style1)
        ws.write(i, 2, item.surface.street.name, style1)
        ws.write(i, 3, item.surface.house_number, style1)
        ws.write(i, 4, item.surface.porch_count(), style1)
        i += 1
        porch_total += item.surface.porch_count()
    ws.write(i + 1, 0, u'Кол-во домов: %d' % order.clientordersurface_set.all().count(), style0)
    ws.write(i + 2, 0, u'Кол-во стендов: %d' % porch_total, style0)

    ws.col(0).width = 10000
    ws.col(1).width = 10000
    ws.col(2).width = 10000
    ws.col(3).width = 4500
    ws.col(4).width = 10000
    for count in range(i):
        ws.row(count).height = 300

    fname = 'order_#%d.xls' % order.id
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    wb.save(response)
    return response


def client_journal(request, pk):
    context = {}
    client = Client.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    if request.method == 'POST':
        form = ClientJournalForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('client:journal', args=(client.id,)))
    else:
        form = ClientJournalForm(initial={
            'client': client
        })
    form.fields['clientorder'].queryset = client.clientorder_set.all()
    context.update({
        'success': success_msg,
        'error': error_msg,
        'clientjournal_form': form,
        'object': client,
        'client': client
    })
    return render(request, 'client/client_journal.html', context)


def client_journal_export(request, pk):
    journal = ClientJournal.objects.get(pk=int(pk))
    client = journal.client
    order = journal.clientorder
    moderator = client.city.moderator
    current_year = date.today().year
    cost = journal.cost if journal.cost else 0
    add_cost = journal.add_cost if journal.add_cost else 0
    discount = journal.discount if journal.discount else 0
    if moderator.company:
        company_name = moderator.company
    else:
        company_name = u'Не указано'
    if moderator.leader:
        company_leader = moderator.leader
    else:
        company_leader = u'Не указано'
    if moderator.leader_function:
        company_leader_function = moderator.leader_function
    else:
        company_leader_function = u'Не указано'
    if moderator.work_basis:
        company_basis = moderator.work_basis
    else:
        company_basis = u'Не указано'
    first_msg = u"%s, в лице %s %s, действующего на основании %s,\n именуемое в дальнейшем Рекламораспространитель." % (company_name, company_leader_function, company_leader, company_basis)
    second_msg = u', именуемое в дальнейшем Рекламодатель, пришли в соглашение о нижеследующем:\nРекламораспространитель обязуется разместить рекламные публикации Рекламодателя\n на следующих условиях:'

    font0 = xlwt.Font()
    font0.name = 'Calibri'
    font0.height = 160

    font1 = xlwt.Font()
    font1.name = 'Calibri'
    font1.height = 160
    font1.bold = True

    font2 = xlwt.Font()
    font2.name = 'Calibri'
    font2.height = 240
    font2.bold = True

    alignment_right = xlwt.Alignment()
    alignment_right.horz = xlwt.Alignment.HORZ_RIGHT
    alignment_right.vert = xlwt.Alignment.VERT_TOP
    alignment_center = xlwt.Alignment()
    alignment_center.horz = xlwt.Alignment.HORZ_CENTER
    alignment_center.vert = xlwt.Alignment.VERT_TOP

    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN

    borders_bottom = xlwt.Borders()
    borders_bottom.bottom = xlwt.Borders.THIN

    style0 = xlwt.XFStyle()
    style0.font = font0
    style0.alignment = alignment_right

    style1 = xlwt.XFStyle()
    style1.font = font1
    style1.alignment = alignment_center

    style2 = xlwt.XFStyle()
    style2.font = font0

    style3 = xlwt.XFStyle()
    style3.font = font2
    style3.alignment = alignment_center

    style4 = xlwt.XFStyle()
    style4.font = font1
    style4.alignment = alignment_center
    style4.borders = borders

    style5 = xlwt.XFStyle()
    style5.font = font1
    style5.borders = borders_bottom

    wb = xlwt.Workbook()
    ws = wb.add_sheet(u'Лист 1')
    ws.write_merge(0, 0, 0, 8,
                   u'К договору на изготовление и размещение рекламы № _____ от "___" _____%sг.' % str(current_year),
                   style0)
    ws.write_merge(2, 2, 0, 8, u'Заказ на размещение рекламы', style1)
    ws.write_merge(4, 4, 0, 8, first_msg, style2)
    ws.write_merge(5, 5, 0, 8, client.legal_name, style3)
    ws.write_merge(6, 6, 0, 8, second_msg, style2)
    ws.write_merge(8, 8, 0, 8, u'1. Издания, выходящие под брендом: %s' % company_name, style2)
    ws.write_merge(10, 10, 0, 8, u'2. Медиа план:', style2)

    ws.write(11, 0, u'Город', style4)
    ws.write(11, 1, u'Район', style4)
    ws.write(11, 2, u'Улица', style4)
    ws.write(11, 3, u'Номер дома', style4)
    ws.write(11, 4, u'Кол-во стендов', style4)
    ws.write(11, 5, u'Цена за стенд, руб', style4)
    ws.write(11, 6, u'Наценка, %', style4)
    ws.write(11, 7, u'Скидка, %', style4)
    ws.write(11, 8, u'Итого, руб', style4)

    i = 12
    porch_total = 0
    total_count = 0
    for item in order.clientordersurface_set.all():
        count = ((cost*(1+add_cost*0.01))*(1+discount*0.01)) * item.surface.porch_count()
        ws.write(i, 0, item.surface.city.name, style4)
        ws.write(i, 1, item.surface.street.area.name, style4)
        ws.write(i, 2, item.surface.street.name, style4)
        ws.write(i, 3, item.surface.house_number, style4)
        ws.write(i, 4, item.surface.porch_count(), style4)
        ws.write(i, 5, cost, style4)
        ws.write(i, 6, add_cost, style4)
        ws.write(i, 7, discount, style4)
        ws.write(i, 8, count, style4)
        i += 1
        porch_total += item.surface.porch_count()
        total_count += count
    ws.write(i+1, 0, u'Итого', style2)
    ws.write(i+1, 8, u"%s, руб." % total_count, style2)
    ws.write_merge(i+2, i+2, 0, 1, u'Ответственный менеджер', style5)
    ws.write_merge(i+5, i+5, 0, 1, u'Руководитель отдела', style5)
    ws.write_merge(i+8, i+8, 0, 1, u'Бухгалтерия', style5)

    ws.col(0).width = 6000
    ws.col(1).width = 6000
    ws.col(2).width = 6000
    ws.col(3).width = 4500
    ws.col(4).width = 4500
    ws.col(5).width = 6000
    ws.col(6).width = 4000
    ws.col(7).width = 4000
    ws.col(8).width = 4000
    for count in range(i+8):
        ws.row(count).height = 300
    ws.row(4).height = 1000
    ws.row(5).height = 400
    ws.row(6).height = 1000

    fname = 'journal_#%d_client_#%d_order_#%d.xls' % (journal.id, client.id, order.id)
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    wb.save(response)
    return response


# @ajax_request
def add_client_surface(request):
    print 'STEP 1'
    if request.method == 'POST':
        print 'STEP 2 - POST'
        # print request.POST
        # client = Client.objects.get(pk=int(request.POST.get('cos_client')))
        # print 'client %s' % int(request.POST.get('cos_client'))
        print 'client %s' % int(request.POST.get('cos_order'))
        order = ClientOrder.objects.get(pk=int(request.POST.get('cos_order')))
        surfaces = request.POST.getlist('chk_group[]')
        for item in surfaces:
            surface = Surface.objects.get(pk=int(item))
            surface.free = False
            surface.save()
            print surface
            c_surface = ClientOrderSurface(
                clientorder=order,
                surface=surface
            )
            c_surface.save()
        return HttpResponseRedirect(reverse('client:order-update', args=(int(request.POST.get('cos_order')),)))
    else:
        print 'STEP FAIL'
        return HttpResponseRedirect(reverse('client:order', args=(int(request.POST.get('cos_order')),)))


def client_maket_add(request):
    if request.method == 'POST':
        form = ClientMaketForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def client_excel_export(request, pk):
    client = Client.objects.get(id=int(pk))
    font0 = xlwt.Font()
    font0.name = 'Calibri'
    font0.height = 220

    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN

    style0 = xlwt.XFStyle()
    style0.font = font0

    style1 = xlwt.XFStyle()
    style1.font = font0
    style1.borders = borders

    wb = xlwt.Workbook()
    ws = wb.add_sheet(u'Рекламные поверхости')
    ws.write(0, 0, u'Клиент:', style0)
    ws.write(0, 1, u'%s' % client.legal_name, style0)
    ws.write(1, 0, u'Город:', style0)
    ws.write(1, 1, u'%s' % client.city.name, style0)

    ws.write(3, 0, u'Город', style1)
    ws.write(3, 1, u'Район', style1)
    ws.write(3, 2, u'Улица', style1)
    ws.write(3, 3, u'Номер дома', style1)
    ws.write(3, 4, u'Дата размещения', style1)
    ws.write(3, 5, u'Дата окончания размещения', style1)

    i = 4
    if client.clientsurface_set.all():
        for item in client.clientsurface_set.all():
            ws.write(i, 0, item.surface.city.name, style1)
            ws.write(i, 1, item.surface.street.area.name, style1)
            ws.write(i, 2, item.surface.street.name, style1)
            ws.write(i, 3, item.surface.house_number, style1)
            ws.write(i, 4, str(item.date_start), style1)
            ws.write(i, 5, str(item.date_end), style1)
            i += 1

    ws.col(0).width = 6666
    ws.col(1).width = 6666
    ws.col(2).width = 10000
    ws.col(3).width = 4500
    ws.col(4).width = 10000
    ws.col(5).width = 10000
    for count in range(i):
        ws.row(count).height = 300

    fname = 'client_#%d_address_list.xls' % client.id
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    wb.save(response)
    return response
