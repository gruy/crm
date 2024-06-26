# coding=utf-8
from annoying.decorators import ajax_request
from datetime import datetime

from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from apps.adjuster.models import Adjuster, AdjusterTaskSurface, SurfacePhoto
from apps.city.models import Area, City, Street, Surface, ManagementCompany
from apps.client.models import Client, ClientOrder, ClientOrderSurface, ClientSurfaceBind
from core.models import User

__author__ = 'alexy'


@ajax_request
def get_simple_city_map(request):
    """
    Функция получения информации для карты главной страницы сайта
    Получение полного списка городов с координатами и количеством поверхностей.
    """
    qs = City.objects.all()
    city_list = []
    for city in qs:
        city_list.append({
            'name': city.name,
            'coord_x': float(city.coord_x),
            'coord_y': float(city.coord_y),
            'surface_count': int(city.surface_count())
        })
    return {
        'city_list': city_list
    }


@ajax_request
def get_city_area(request):
    """
    получение списка районов данного города.
    Опционально - список монтажников данного города и УК
    """
    if request.GET.get('city'):
        area_list = []
        adjuster_list = []
        client_list = []
        clientorder_list = []
        management_list = []
        r_city = request.GET.get('city')
        area_qs = Area.objects.filter(city=int(r_city))
        adjuster_qs = Adjuster.objects.filter(city=int(r_city))
        client_qs = Client.objects.filter(city=int(r_city))
        today = datetime.today()
        clientorder_qs = Client.objects.filter(
            clientorder__clientordersurface__surface__city_id=int(r_city),
            clientorder__date_end__gte=today
        ).distinct()
        management_qs = ManagementCompany.objects.filter(city_id=int(r_city)).order_by('name')
        for i in area_qs:
            area_list.append({
                'id': i.id,
                'name': i.name
            })
        for i in adjuster_qs:
            adjuster_list.append(
                {
                    'id': i.id,
                    'name': i.user.get_full_name()
                }
            )
        for i in client_qs:
            client_list.append(
                {
                    'id': i.id,
                    'name': i.legal_name
                }
            )
        for i in clientorder_qs:
            clientorder_list.append(
                {
                    'id': i.id,
                    'name': i.legal_name
                }
            )
        for i in management_qs:
            management_list.append(
                {
                    'id': i.id,
                    'name': i.name
                }
            )
        return {
            'area_list': area_list,
            'adjuster_list': adjuster_list,
            'client_list': client_list,
            'clientorder_list': clientorder_list,
            'management_list': management_list
        }
    else:
        return {
            'error': True
        }


@ajax_request
def simple_get_area_streets(request):
    if request.GET.get('area'):
        street_list = []
        area_pk = int(request.GET.get('area'))

        street_qs = Street.objects.filter(area=area_pk)
        for street in street_qs:
            # if surface.id not in client_surfaces:
            street_list.append({
                'id': street.id,
                'name': street.name,
            })
        return {
            'street_list': street_list
        }
    else:
        return {
            'error': u'Что то пошло не так!'
        }


def _surface_list(surfaces):
    return [
        {
            'id': surface.id,
            'city': surface.city.name,
            'street': surface.street.name,
            'number': surface.house_number,
            'porch_count': surface.porch_count(),
            'coord_x': surface.coord_x,
            'coord_y': surface.coord_y,
            'floors': surface.floors or '-',
            'apart_count': surface.apart_count or '-',
            'management': surface.management.name if surface.management else '-',
        }
        for surface in surfaces
    ]


@ajax_request
def get_area_surfaces(request):
    area_id = request.GET.get('area_id')
    client_id = request.GET.get('client_id')
    surface_list = []
    qs = (
        Surface.objects.select_related('management')
        .filter(street__area=area_id)
        .exclude(clientsurfacebind__client__id=client_id)
        .extra(select={'house_number_int': 'CAST(house_number AS INTEGER)'})
        .order_by('street__area', 'street__name', 'house_number_int')
    )
    return {
        'surface_list': _surface_list(qs)
    }


@ajax_request
def get_free_area_surface(request):
    if request.GET.get('area') and request.GET.get('order'):
        surface_list = []
        streets_list = []
        area_pk = int(request.GET.get('area'))
        street_id = int(request.GET.get('street_id', 0))
        order = ClientOrder.objects.get(pk=int(request.GET.get('order')))
        surface_qs = Surface.objects.select_related('management').filter(
            street__area=area_pk,
        ).exclude(
            (
                Q(clientordersurface__clientorder__date_start__gte=order.date_start)
                | Q(clientordersurface__clientorder__date_end__gte=order.date_start)
            )
            & Q(clientordersurface__clientorder__date_start__lte=order.date_end)
        )
        if street_id:
            surface_qs = surface_qs.filter(street_id=street_id)
        else:
            streets_list = [
                {'id': s.id, 'name': s.name} for s in Street.objects.filter(area=area_pk).order_by('name')
            ]
        # фильтруем поверхности по зоне покрытия клиента
        if order.client.has_limit_surfaces:
            surfaces = ClientSurfaceBind.objects.filter(client=order.client).values_list('surface', flat=True)
            surface_qs = surface_qs.filter(id__in=surfaces)

        surface_qs = surface_qs.extra(select={'house_number_int': 'CAST(house_number AS INTEGER)'})
        surface_qs = surface_qs.order_by('street__name', 'house_number_int')

        return {
            'surface_list': _surface_list(surface_qs),
            'streets_list': streets_list,
        }
    else:
        return {
            'error': u'Что то пошло не так!'
        }


@ajax_request
def surface_ajax(request):
    street_list = []
    if request.GET.get('city'):
        if int(request.GET.get('city')) == 0:
            user = User.objects.get(id=int(request.user.id))
            if user.type == 1:
                city = City.objects.all()
                street_qs = Street.objects.all()
            else:
                city = user.city_set.all()
                street_qs = Street.objects.filter(city__moderator=user)
        else:
            city = City.objects.get(id=int(request.GET.get('city')))
            street_qs = city.street_set.all()
        for i in street_qs:
            street_list.append(
                {
                    'id': i.id,
                    'name': i.__unicode__()
                }
            )
        return {
            # 'city': city.name,
            'street_list': street_list
        }


@ajax_request
def get_city_adjusters(request):
    adjuster_list = []
    if request.GET.get('city'):
        a_qs = Adjuster.objects.filter(city=int(request.GET.get('city')))
        for i in a_qs:
            adjuster_list.append(
                {
                    'id': i.id,
                    'name': i.user.get_full_name()
                }
            )
        return {
            'success': True,
            'adjuster_list': adjuster_list
        }
    else:
        return {
            'error': True
        }


@ajax_request
def get_area_surface_list(request):
    """
    Функция отображает список поверхностей для постановки задачи.
    Воказываются только целые и не полностью повреждённые поверхности.
    """
    if request.GET.get('area'):
        surface_list = []
        r_area = request.GET.get('area')
        r_date = request.GET.get('date')
        r_type = request.GET.get('type')
        at_surface_list_id = []
        if r_date:
            date = datetime.strptime(r_date, '%d.%m.%Y')
            at_surface = AdjusterTaskSurface.objects.filter(
                surface__street__area=int(r_area),
                adjustertask__date=date
            )
            at_surface_list_id = [int(i.surface.id) for i in at_surface]
        one_porch = False
        if r_type:
            if int(r_type) == 3:
                one_porch = True
        surface_qs = Surface.objects.filter(street__area=int(r_area), full_broken=False)
        for surface in surface_qs:
            broken_porch = []
            intact_porch = []
            if int(surface.id) not in at_surface_list_id:
                for porch in surface.porch_set.all():
                    if porch.is_broken:
                        broken_porch.append(porch.number)
                    else:
                        intact_porch.append(porch.number)
                    if one_porch:
                        surface_list.append({
                            'id': surface.id,
                            'porch_id': porch.id,
                            'city': surface.city.name,
                            'area': surface.street.area.name,
                            'street': surface.street.name,
                            'number': surface.house_number,
                            'porch': '-',
                            'intact_porch': intact_porch,
                            'broken_porch': broken_porch
                        })
                        broken_porch = []
                        intact_porch = []
                if not one_porch:
                    surface_list.append({
                        'id': surface.id,
                        'porch_id': None,
                        'city': surface.city.name,
                        'area': surface.street.area.name,
                        'street': surface.street.name,
                        'number': surface.house_number,
                        'porch': int(surface.porch_count()),
                        'intact_porch': intact_porch,
                        'broken_porch': broken_porch
                    })
        return {
            'surface_list': surface_list
        }
    else:
        return {
            'error': u'Что то пошло не так!'
        }


@ajax_request
def get_area_surface_list_with_damage(request):
    """
    Функция отображает список поверхностей для постановки задачи на ремонт.
    Показываются только поверхности имеющие повреждения (флаг damaged=1).
    """
    if request.GET.get('area'):
        porch_list = []
        r_area = request.GET.get('area')
        r_date = request.GET.get('date')
        at_surface_list_id = []
        if r_date:
            date = datetime.strptime(r_date, '%d.%m.%Y')
            at_surface = AdjusterTaskSurface.objects.filter(
                surface__street__area=int(r_area),
                adjustertask__date=date
            )
            at_surface_list_id = [int(i.surface.id) for i in at_surface]
        r_client = request.GET.get('client')
        order_dict = {}
        if r_client:
            client_qs = ClientOrderSurface.objects.filter(
                clientorder__client_id=int(request.GET.get('client')),
                surface__street__area=int(r_area)
            )
            order_dict = {c_surface.surface: str(c_surface.clientorder) for c_surface in client_qs}
            surface_ids = [c_surface.surface_id for c_surface in client_qs]
            surface_qs = Surface.objects.filter(id__in=surface_ids)
        else:
            surface_qs = Surface.objects.filter(street__area=int(r_area), has_broken=True)
        for surface in surface_qs.order_by('street__area', 'street__name', 'house_number'):
            if int(surface.id) not in at_surface_list_id:
                porch_qs = surface.porch_set.filter(is_broken=True)
                for porch in porch_qs:
                    type_list = []
                    if porch.broken_shield:
                        type_list.append(u'сломан щит')
                    if porch.broken_gib:
                        type_list.append(u'сломана прижимная планка')
                    if porch.no_glass:
                        type_list.append(u'отсутствует защитное стекло')
                    if porch.replace_glass:
                        type_list.append(u'заменить защитное стекло')
                    if porch.against_tenants:
                        type_list.append(u'жильцы против')
                    if porch.no_social_info:
                        type_list.append(u'отсутствует социальная информация')
                    damage_type = ', '.join(type_list)
                    porch_list.append({
                        'id': porch.id,
                        'city': porch.surface.city.name,
                        'area': porch.surface.street.area.name,
                        'street': porch.surface.street.name,
                        'house_number': porch.surface.house_number,
                        'number': porch.number,
                        'type': damage_type,
                        'order': order_dict.get(porch.surface, '')
                    })
        return {
            'porch_list': porch_list
        }
    else:
        return {
            'error': u'Что то пошло не так!'
        }


@ajax_request
@csrf_exempt
def get_photo_map(request):
    user = request.user
    qs = SurfacePhoto.objects.none()
    photo_list = []
    if user.type == 1:
        qs = SurfacePhoto.objects.select_related().all()
    elif user.type == 6:
        qs = SurfacePhoto.objects.select_related().filter(porch__surface__city__in=user.superviser.city_id_list())
    elif user.type == 2:
        qs = SurfacePhoto.objects.select_related().filter(porch__surface__city__moderator=user)
    elif user.type == 3:
        client = user.client
        clientorder_list = [int(i.id) for i in client.clientorder_set.filter(is_closed=False)]
        qs_list = []
        for corder in client.clientorder_set.all():
            s_qs = SurfacePhoto.objects.select_related().filter(porch__surface__clientordersurface__clientorder=corder).filter(date__gte=corder.date_start).filter(date__lte=corder.date_end)
            if s_qs:
                qs_list.append(s_qs)
        if qs_list:
            query_string_item = []
            for i in range(len(qs_list)):
                query_string_item.append('qs_list[%d]' % i)
            query_string = ' | '.join(query_string_item)
            qs = eval(query_string)
        else:
            qs = SurfacePhoto.objects.none()
    elif user.type == 5 and user.is_leader_manager():
        qs = SurfacePhoto.objects.select_related().filter(porch__surface__city__moderator=user.manager.moderator)

    city = request.POST.get('city')
    area = request.POST.get('area')
    street = request.POST.get('street')
    date_s = request.POST.get('date_s')
    date_e = request.POST.get('date_e')
    show_broken = request.session['show_broken']
    if qs.exists():
        qs = qs.filter(is_broken=show_broken)
        if city:
            qs = qs.filter(porch__surface__city=int(city))
            if area:
                qs = qs.filter(porch__surface__street__area=int(area))
                if street:
                    qs = qs.filter(porch__surface__street=int(street))
        if date_s:
            # rs_date = datetime.strptime(date_s, '%d.%m.%Y')
            # s_date = datetime.date(rs_date)
            qs = qs.filter(date__gte=datetime.strptime(date_s, '%d.%m.%Y'))
        if date_e:
            # re_date = datetime.strptime(date_e, '%d.%m.%Y')
            # e_date = datetime.date(re_date)
            qs = qs.filter(date__lte=datetime.strptime(date_e, '%d.%m.%Y'))
        for photo in qs:
            photo_list.append({
                'coord_y': str(photo.porch.surface.coord_y),
                'coord_x': str(photo.porch.surface.coord_x),
                'surface': photo.porch.surface.__unicode__(),
                'porch': photo.porch.__unicode__(),
                'image': photo.image_resize.url
            })
    return {
        'photo_list': photo_list
    }
