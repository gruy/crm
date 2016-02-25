# coding=utf-8
from datetime import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.adjuster.models import SurfacePhoto
from apps.city.forms import CityAddForm, StreetForm, AreaAddForm, ManagementCompanyForm
from apps.city.models import City, Area, Street, ManagementCompany

__author__ = 'alexy'


class CityListView(ListView):
    model = City

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.type == 1:
            qs = City.objects.all()
        elif self.request.user.type == 2:
            qs = City.objects.filter(moderator=user_id)
        else:
            qs = None
        if self.request.GET.get('moderator'):
            qs = qs.filter(moderator__email=self.request.GET.get('moderator'))
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            qs = qs.filter(id=int(self.request.GET.get('city')))
        return qs

    @csrf_exempt
    def get_context_data(self, **kwargs):
        context = super(CityListView, self).get_context_data()
        if self.request.user.type == 1:
            qs = City.objects.all()
        elif self.request.user.type == 2:
            qs = City.objects.filter(moderator=self.request.user.id)
        else:
            qs = None
        context.update({
            'user_city_list': qs
        })
        if self.request.user.type == 1:
            a_qs = SurfacePhoto.objects.all()
        elif self.request.user.type == 2:
            a_qs = SurfacePhoto.objects.filter(porch__surface__city__moderator=int(self.request.user.id))
        else:
            a_qs = None
        # установка флага отображения - таблица, плитка
        try:
            self.request.session['grid']
        except:
            self.request.session['grid'] = False
        if self.request.GET.get('grid'):
            if int(self.request.GET.get('grid')) == 1:
                self.request.session['grid'] = True
            else:
                self.request.session['grid'] = False
        # установка флага фильтрации - порвеждённые, целые
        try:
            self.request.session['show_broken']
        except:
            self.request.session['show_broken'] = False
        if self.request.GET.get('broken'):
            if int(self.request.GET.get('broken')) == 1:
                self.request.session['show_broken'] = True
            else:
                self.request.session['show_broken'] = False
        context.update({
            'show_broken': self.request.session['show_broken'],
            'grid': self.request.session['grid']
        })
        # try:
        #     self.request.session['a_city']
        # except:
        #     self.request.session['a_city'] = False
        # if self.request.GET.get('a_city'):
        # установка флага города для фильтрации
        try:
            a_city = int(self.request.GET.get('a_city'))
            area_list = Area.objects.filter(city=a_city)
        except:
            a_city = None
            area_list = None
        # self.request.session['a_city'] = a_city
        # установка флага района для фильтрации
        try:
            a_area = int(self.request.GET.get('a_area'))
            street_list = Street.objects.filter(area=a_area)
        except:
            a_area = None
            street_list = None
        # self.request.session['a_area'] = a_area
        # установка флага улицы для фильтрации
        try:
            a_street = int(self.request.GET.get('a_street'))
        except:
            a_street = None
        # self.request.session['a_street'] = a_street
        # установка флага начальной даты для фильтрации
        try:
            a_date_s = self.request.GET.get('a_date_s')
        except:
            a_date_s = None
        # установка флага начальной даты для фильтрации
        try:
            a_date_e = self.request.GET.get('a_date_e')
        except:
            a_date_e = None
        # self.request.session['a_date_s'] = a_date_s
        context.update({
            'a_city': a_city,
            'a_area': a_area,
            'a_street': a_street,
            'area_list': area_list,
            'street_list': street_list,
            'a_date_s': a_date_s,
            'a_date_e': a_date_e
        })
        if a_qs:
            a_qs = a_qs.filter(is_broken=self.request.session['show_broken'])
            if a_city:
                a_qs = a_qs.filter(porch__surface__city=int(a_city))
                if a_area:
                    a_qs = a_qs.filter(porch__surface__street__area=int(a_area))
                    if a_street:
                        a_qs = a_qs.filter(porch__surface__street=int(a_street))
            if a_date_s:
                rs_date = datetime.strptime(a_date_s, '%d.%m.%Y')
                s_date = datetime.date(rs_date)
                a_qs = a_qs.filter(date__gte=s_date)
                if a_date_e:
                    re_date = datetime.strptime(a_date_e, '%d.%m.%Y')
                    e_date = datetime.date(re_date)
                    a_qs = a_qs.filter(date__lte=e_date)

        paginator = Paginator(a_qs, 20) # Show 25 contacts per page
        page = self.request.GET.get('page')
        try:
            address_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            address_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            address_list = paginator.page(paginator.num_pages)
        context.update({
            'address_list': address_list
        })

        return context


class CityCreateView(CreateView):
    model = City
    form_class = CityAddForm
    template_name = 'city/city_add.html'


def city_update(request, pk):
    user = request.user
    city = City.objects.get(pk=int(pk))
    if city.moderator == user or user.type == 1:
        # Если пользователь не является модератором города или администратором:
        # перенаправить его на страницу со списком своих городов
        pass
    else:
        return HttpResponseRedirect(reverse('city:list'))

    if request.method == 'POST':
        form = CityAddForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(city.get_absolute_url())
    else:
        form = CityAddForm(instance=city)
        if user.type == 2:
            form.fields['name'].widget.attrs['readonly'] = True
            form.fields['moderator'].widget.attrs['readonly'] = True
    context = {
        'form': form,
        'city': city
    }
    return render(request, 'city/city_update.html', context)


def city_area(request, pk):
    context = {}
    city = City.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = AreaAddForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('city:area', args=(city.id, )))
        else:
            return HttpResponseRedirect(reverse('city:area', args=(city.id, )))
    else:
        form = AreaAddForm(
            initial={
                'city': city
            }
        )
    context.update({
        'city': city,
        'area_form': form
    })
    return render(request, 'city/city_area.html', context)


def city_area_update(request, pk):
    context = {}
    area = Area.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = AreaAddForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('city:area', args=(area.city.id, )))
        else:
            return HttpResponseRedirect(reverse('city:area-update', args=(area.id, )))
    else:
        form = AreaAddForm(instance=area)
    context.update({
        'city': area.city,
        'area': area,
        'area_form': form
    })
    return render(request, 'city/city_area_update.html', context)


def city_street(request, pk):
    context = {}
    city = City.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = StreetForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('city:street', args=(city.id, )))
    else:
        form = StreetForm(
            initial={
                'city': city
            }
        )
        form.fields['area'].queryset = city.area_set.all()
    context.update({
        'city': city,
        'street_form': form
    })
    return render(request, 'city/city_street.html', context)


def city_street_update(request, pk):
    context = {}
    street = Street.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = StreetForm(request.POST, instance=street)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('city:street', args=(street.city.id, )))
        else:
            return HttpResponseRedirect(reverse('city:street-update', args=(street.id, )))
    else:
        form = StreetForm(instance=street)
        form.fields['area'].queryset = street.city.area_set.all()
    context.update({
        'city': street.city,
        'street': street,
        'street_form': form
    })
    return render(request, 'city/city_street_update.html', context)


def management_company_list(request):
    context = {}
    if request.user.type == 1:
        qs = ManagementCompany.objects.all()
        city_qs = City.objects.all()
    elif request.user.type == 2:
        qs = ManagementCompany.objects.filter(city__moderator=request.user)
        city_qs = City.objects.filter(moderator=request.user)
    else:
        qs = None
        city_qs = None
    if request.GET.get('city') and int(request.GET.get('city')) != 0:
        qs = qs.filter(city=int(request.GET.get('city')))
        context.update({
            'city_id': int(request.GET.get('city'))
        })
    if request.GET.get('name'):
        qs = qs.filter(name__icontains=request.GET.get('name'))
    context.update({
        'object_list': qs,
        'city_list': city_qs
    })
    return render(request, 'city/management_company_list.html', context)


def management_company_add(request):
    context = {}
    if request.method == 'POST':
        form = ManagementCompanyForm(request.POST, request=request)
        if form.is_valid():
            management_company = form.save()
            return HttpResponseRedirect(reverse('city:management-company-update', args=(management_company.id, )))
    else:
        form = ManagementCompanyForm(request=request)
    context.update({
        'form': form
    })
    return render(request, 'city/management_company.html', context)


def management_company_update(request, pk):
    context = {}
    m_company = ManagementCompany.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = ManagementCompanyForm(request.POST, request=request, instance=m_company)
        if form.is_valid():
            form.save()
    else:
        form = ManagementCompanyForm(request=request, instance=m_company)
    context.update({
        'form': form,
        'object': m_company
    })
    return render(request, 'city/management_company.html', context)
