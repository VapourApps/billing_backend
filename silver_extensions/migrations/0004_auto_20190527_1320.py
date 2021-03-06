# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-27 13:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('silver_extensions', '0003_auto_20190527_1307'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='planfeatures',
            options={'verbose_name_plural': 'Plan Features'},
        ),
        migrations.AlterModelOptions(
            name='planstep',
            options={'verbose_name_plural': 'Plan Steps'},
        ),
        migrations.AlterModelOptions(
            name='stepfield',
            options={'verbose_name_plural': 'Step Fields'},
        ),
        migrations.AddField(
            model_name='planstep',
            name='belongs_to',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='silver.Plan'),
            preserve_default=False,
        ),
    ]
