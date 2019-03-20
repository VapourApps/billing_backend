# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-20 11:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('silver', '0048_auto_20190320_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(b'success', b'success'), (b'fail', b'fail'), (b'invalid_data', b'invalid_data')], max_length=9)),
                ('data', models.CharField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='Payment_Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redirect_ok_url', models.CharField(blank=True, max_length=2083, null=True)),
                ('redirect_fail_url', models.CharField(blank=True, max_length=2083, null=True)),
                ('status', models.CharField(choices=[(b'generated', b'generated'), (b'success', b'success'), (b'fail', b'fail')], default=b'generated', max_length=9)),
                ('data', models.CharField(max_length=5000)),
                ('post_url', models.CharField(max_length=2083)),
                ('invoices', models.ManyToManyField(related_name='invoice_payment_requests', to='silver.Invoice')),
                ('proformas', models.ManyToManyField(related_name='proforma_payment_requests', to='silver.Proforma')),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='payment_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='silver_cpay.Payment_Request'),
        ),
    ]
