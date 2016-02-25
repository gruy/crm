# coding=utf-8
from annoying.decorators import ajax_request
from apps.adjuster.models import Adjuster
from apps.city.forms import AreaAddForm, StreetForm
from apps.city.models import Area, City, Street, Surface, Porch
from apps.client.models import Client, ClientOrder
from apps.surface.forms import PorchAddForm
from core.models import User

__author__ = 'alexy'


@ajax_request
def get_city_area(request):
    """
    получение списка районов данного города.
    Опциоанльно - список монтажников данного города
    """
    if request.GET.get('city'):
        area_list = []
        adjuster_list = []
        r_city = request.GET.get('city')
        area_qs = Area.objects.filter(city=int(r_city))
        adjuster_qs = Adjuster.objects.filter(city=int(r_city))
        print area_qs
        print adjuster_qs
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
        print area_list
        print adjuster_list
        return {
            'area_list': area_list,
            'adjuster_list': adjuster_list
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
        print street_qs
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



@ajax_request
def get_free_area_surface(request):
    if request.GET.get('area') and request.GET.get('order'):
        surface_list = []
        area_pk = int(request.GET.get('area'))
        order = ClientOrder.objects.get(pk=int(request.GET.get('order')))
        print u'дата начала размещения по заказу %s' % order.date_start
        surface_qs = Surface.objects.filter(street__area=area_pk, release_date__lt=order.date_start)
        for surface in surface_qs:
            if surface.id:
                surface_list.append({
                    'id': surface.id,
                    'street': surface.street.name,
                    'number': surface.house_number
                })
        return {
            'surface_list': surface_list
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
                    'name': i.name
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
    Если задача по адресам - показываются только целые и не полностью повреждённые поверхности (флаг damaged=0).
    Если зада на ремонт - показываются только поверхности имеющие повреждения (флаг damaged=1).
    """
    if request.GET.get('area'):
        surface_list = []
        r_area = request.GET.get('area')
        surface_qs = Surface.objects.filter(street__area=int(r_area), full_broken=False)
        for surface in surface_qs:
            print u'Поверхность: %s' % surface
            broken_porch = []
            intact_porch = []
            for porch in surface.porch_set.all():
                print porch
                if porch.is_broken:
                    broken_porch.append(porch.number)
                else:
                    intact_porch.append(porch.number)
            print u'Поломанные подъезды: %s' % broken_porch
            print u'Целые подъезды: %s' % intact_porch
            surface_list.append({
                'id': surface.id,
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
        surface_qs = Surface.objects.filter(street__area=int(r_area), has_broken=True)
        for surface in surface_qs:
            porch_qs = surface.porch_set.filter(is_broken=True)
            print porch_qs

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
                })
            print porch_list
        return {
            'porch_list': porch_list
        }
    else:
        return {
            'error': u'Что то пошло не так!'
        }

