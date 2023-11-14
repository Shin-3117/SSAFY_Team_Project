# Generated by Django 4.2.7 on 2023-11-14 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cur_unit', models.CharField(max_length=10)),
                ('cur_nm', models.CharField(max_length=50)),
                ('ttb', models.DecimalField(decimal_places=4, max_digits=12)),
                ('tts', models.DecimalField(decimal_places=4, max_digits=12)),
                ('deal_bas_r', models.DecimalField(decimal_places=4, max_digits=12)),
                ('krw_to_cur', models.DecimalField(decimal_places=2, max_digits=10)),
                ('req_dt', models.DateField(auto_now=True)),
            ],
        ),
    ]
