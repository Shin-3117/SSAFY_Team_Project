# Generated by Django 4.2.7 on 2023-11-16 16:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DepositOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intr_rate_type', models.TextField()),
                ('intr_rate_type_nm', models.CharField(max_length=100)),
                ('intr_rate', models.FloatField(blank=True, default=-1, null=True)),
                ('intr_rate2', models.FloatField()),
                ('save_trm', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DepositProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_prdt_cd', models.TextField(unique=True)),
                ('kor_co_nm', models.TextField()),
                ('fin_prdt_nm', models.TextField()),
                ('etc_note', models.TextField()),
                ('join_deny', models.IntegerField()),
                ('join_member', models.TextField()),
                ('join_way', models.TextField()),
                ('spcl_cnd', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SavingOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intr_rate_type', models.TextField()),
                ('intr_rate_type_nm', models.CharField(max_length=100)),
                ('intr_rate', models.FloatField(blank=True, default=-1, null=True)),
                ('intr_rate2', models.FloatField()),
                ('save_trm', models.IntegerField()),
                ('rsrv_type', models.TextField()),
                ('rsrv_type_nm', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SavingProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_prdt_cd', models.TextField(unique=True)),
                ('kor_co_nm', models.TextField()),
                ('fin_prdt_nm', models.TextField()),
                ('etc_note', models.TextField()),
                ('join_deny', models.IntegerField()),
                ('join_member', models.TextField()),
                ('join_way', models.TextField()),
                ('spcl_cnd', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SavingsSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscribe_date', models.DateTimeField(auto_now_add=True)),
                ('saving_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finlife.savingoptions')),
                ('saving_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finlife.savingproducts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='savingoptions',
            name='fin_prdt_cd',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='savingoptions', to='finlife.savingproducts'),
        ),
        migrations.CreateModel(
            name='DepositSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscribe_date', models.DateTimeField(auto_now_add=True)),
                ('deposit_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finlife.depositoptions')),
                ('deposit_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finlife.depositproducts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='depositoptions',
            name='fin_prdt_cd',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depositoptions', to='finlife.depositproducts'),
        ),
    ]
