# Generated by Django 3.2.4 on 2022-03-14 13:19

import core.files
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('manager', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('city', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legal_name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Юридическое название')),
                ('actual_name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Фактическое название')),
                ('inn', models.CharField(blank=True, max_length=50, null=True, verbose_name='ИНН')),
                ('kpp', models.CharField(blank=True, max_length=50, null=True, verbose_name='КПП')),
                ('ogrn', models.CharField(blank=True, max_length=50, null=True, verbose_name='ОГРН')),
                ('bank', models.CharField(blank=True, max_length=50, null=True, verbose_name='Банк')),
                ('bik', models.CharField(blank=True, max_length=50, null=True, verbose_name='БИК')),
                ('account', models.CharField(blank=True, max_length=50, null=True, verbose_name='Расчётный счёт')),
                ('account_cor', models.CharField(blank=True, max_length=50, null=True, verbose_name='Кор. счёт')),
                ('signer_post_dec', models.CharField(blank=True, max_length=50, null=True, verbose_name='должность подписанта')),
                ('signer_name_dec', models.CharField(blank=True, max_length=50, null=True, verbose_name='имя подписанта')),
                ('signer_doc_dec', models.CharField(blank=True, max_length=50, null=True, verbose_name='действует на основании')),
                ('legal_address', models.TextField(blank=True, null=True, verbose_name='Физический адрес')),
                ('leader', models.CharField(blank=True, max_length=100, null=True, verbose_name='Руководитель')),
                ('leader_function', models.CharField(blank=True, max_length=100, null=True, verbose_name='Должность руководителя')),
                ('work_basis', models.CharField(blank=True, max_length=256, null=True, verbose_name='Основание для работы')),
                ('photo_additional', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='накрутка к кол-ву фотографий')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city.city', verbose_name='Город')),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manager.manager', verbose_name='Менеджер')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ClientJournal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена за стенд, руб')),
                ('add_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Наценка, %')),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Скидка, %')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('has_payment', models.BooleanField(default=False, verbose_name='Есть поступления')),
                ('full_payment', models.BooleanField(default=False, verbose_name='Оплачено')),
                ('total_stand_count', models.IntegerField(blank=True, default=0, null=True)),
                ('full_cost', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('total_payment', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client', verbose_name='клиент')),
            ],
            options={
                'verbose_name': 'Покупка',
                'verbose_name_plural': 'Покупки',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='ClientOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField(verbose_name='Дата начала размещения')),
                ('date_end', models.DateField(verbose_name='Дата окончания размещения')),
                ('is_closed', models.BooleanField(default=False, verbose_name='Заказ закрыт')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Название')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client', verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['-date_start'],
            },
        ),
        migrations.CreateModel(
            name='ClientOrderSurface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clientorder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.clientorder', verbose_name='Заказ')),
                ('surface', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city.surface', verbose_name='Рекламная поверхность')),
            ],
            options={
                'verbose_name': 'Пункт заказа',
                'verbose_name_plural': 'Пункты заказа',
            },
        ),
        migrations.CreateModel(
            name='ClientMaket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('file', models.FileField(upload_to=core.files.upload_to, verbose_name='Файл макета')),
                ('date', models.DateField(verbose_name='Дата размещения макета')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client', verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Макет',
                'verbose_name_plural': 'Макеты',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='ClientJournalPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum', models.DecimalField(decimal_places=2, max_digits=11, verbose_name='Сумма')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client', verbose_name='Клиент')),
                ('clientjournal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.clientjournal', verbose_name='Покупка')),
            ],
            options={
                'verbose_name': 'Поступление',
                'verbose_name_plural': 'Поступления',
                'ordering': ['-created'],
            },
        ),
        migrations.AddField(
            model_name='clientjournal',
            name='clientorder',
            field=models.ManyToManyField(to='client.ClientOrder', verbose_name='заказ клиента'),
        ),
    ]
