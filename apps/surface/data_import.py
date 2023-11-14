from django.urls import reverse
from django.http import HttpResponseRedirect
import pyexcel
from apps.city.models import Area, City, ManagementCompany, Porch, Street, Surface


def address_list_import(request):
    """
    Структура колонок таблицы:
    - город
    - район
    - улица
    - номер дома
    - количество подъездов
    - УК
    - количество этажей
    """

    if request.method == 'POST' and 'file' in request.FILES:
        filename = request.FILES['file'].name
        extension = filename.split(".")[1]
        content = request.FILES['file'].read()
        sheet = pyexcel.get_sheet(file_type=extension, file_content=content, start_row=1)
        for row in sheet:
            if row != 'Series_1':
                city = row[0]
                area = row[1]
                street = row[2]
                house_number = row[3]
                try:
                    porches = int(row[4])
                except ValueError:
                    porches = 0
                company_name = row[5]
                try:
                    floors = int(row[6])
                except ValueError:
                    floors = None

                try:
                    # пробуем получить город
                    city_instance = City.objects.get(name__iexact=city)

                    try:
                        # пробуем получить район
                        area_instance = Area.objects.get(city=city_instance, name__iexact=area)
                    except Area.DoesNotExist:
                        # создаём новый район
                        area_instance = Area(city=city_instance, name=area)
                        area_instance.save()

                    try:
                        # пробуем получить улицу
                        street_instance = Street.objects.get(
                            city=city_instance, area=area_instance, name__iexact=street
                        )
                    except Street.DoesNotExist:
                        # создаём новую улицу
                        street_instance = Street(city=city_instance, area=area_instance, name=street)
                        street_instance.save()

                    try:
                        # пробуем получить поверхность
                        surface_instance = Surface.objects.get(
                            city=city_instance, street=street_instance, house_number=house_number
                        )
                    except Surface.DoesNotExist:
                        # создаём поверхность
                        surface_instance = Surface(city=city_instance, street=street_instance, house_number=house_number)

                    try:
                        surface_instance.management = ManagementCompany.objects.get(
                            city=city_instance, name=company_name
                        )
                    except ManagementCompany.DoesNotExist:
                        pass

                    if floors:
                        surface_instance.floors = floors

                    surface_instance.save()

                    for i in range(porches):
                        # пробегаемся по списку подъездов
                        try:
                            Porch.objects.get(surface=surface_instance, number=i)
                        except Porch.DoesNotExist:
                            porch = Porch(surface=surface_instance, number=i)
                            porch.save()
                except Exception:
                    pass

    return HttpResponseRedirect(reverse('surface:list'))
