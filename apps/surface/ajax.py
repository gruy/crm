from datetime import datetime
from random import randint

from annoying.decorators import ajax_request
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from PIL import Image

from apps.adjuster.models import SurfacePhoto
from apps.city.models import Surface
from apps.client.models import Client

__author__ = 'alexy'


@ajax_request
@csrf_exempt
def ajax_photo_rotate(request):
    if request.method == 'POST':
        photo_id = request.POST.get('id')
        angle = request.POST.get('angle')
        if photo_id and angle:
            photo = SurfacePhoto.objects.get(id=int(photo_id))
            image = Image.open(photo.image)
            angle = 0 - int(angle)
            # print angle
            image_resize = Image.open(photo.image_resize)
            image.rotate(angle, expand=1).save(photo.image.path)
            image_resize.rotate(angle, expand=1).save(photo.image_resize.path)
            image.close()
            image_resize.close()
            return {
                'success': True,
                'image': u'%s?%s' % (photo.image.url, randint(1, 9)),
                'image_resize': u'%s?%s' % (photo.image_resize.url, randint(1, 9)),
                # 'id': photo.id,
                # 'address': photo.porch.surface.__unicode__(),
                # 'porch_number': photo.porch.number
            }
        else:
            return {
                'success': False
            }
    else:
        return {
            'success': False
        }


@ajax_request
@csrf_exempt
def surface_map(request):
    user = request.user
    surface_list = []
    if user.type == 1:
        qs = Surface.objects.select_related().all()
    elif user.type == 6:
            qs = Surface.objects.select_related().filter(city__in=user.superviser.city_id_list())
    elif user.type == 2:
        qs = Surface.objects.select_related().filter(city__moderator=user)
    elif user.type == 5:
        qs = Surface.objects.select_related().filter(city__moderator=user.manager.moderator)
    else:
        qs = None
    # фильтрация поверхностей по городам, районам, улицам
    management = request.POST.get('management')
    city = request.POST.get('city')
    area = request.POST.get('area')
    street = request.POST.get('street')
    release_date = request.POST.get('release_date')
    free = request.POST.get('free')
    if management:
        if int(management) == 0:
            qs = qs
        elif int(management) == -1:
            qs = qs.filter(management__isnull=True)
        else:
            qs = qs.filter(management=int(management))
    if city and int(city) != 0:
        qs = qs.filter(city=int(city))
    if area and int(area) != 0:
        qs = qs.filter(street__area=int(area))
    if street:
        qs = qs.filter(street__name__icontains=street)
    if release_date:
        qs = qs.filter(release_date__lte=datetime.strptime(release_date, '%d.%m.%Y'))
    if free:
        if int(free) == 1:
            qs = qs.filter(free=True)
        if int(free) == 2:
            qs = qs.filter(free=False)
    for surface in qs:
        surface_list.append({
            'coord_y': surface.coord_y,
            'coord_x': surface.coord_x,
            'name': surface.__unicode__(),
            'porch_count': surface.porch_total_count
        })
    return {
        'surface_list': surface_list
    }


@ajax_request
def surfaces_clients_by_dates(request):
    """ Показываем в фильтре только тех клиентов, у которых в данном диапазоне даты есть заказы """
    date_start = datetime.strptime(request.GET.get('date_start'), '%d.%m.%Y')
    date_end = datetime.strptime(request.GET.get('date_end'), '%d.%m.%Y')
    city_id = request.GET.get('city_id', None)
    qs = Client.objects.filter(
        (
            Q(clientorder__date_start__gte=date_start)
            | Q(clientorder__date_end__gte=date_start)
        )
        & Q(clientorder__date_start__lte=date_end)
    ).distinct()
    if city_id:
        qs = qs.filter(city_id=city_id)
    return {'clients': [{'id': c.id, 'legal_name': c.legal_name} for c in qs]}
