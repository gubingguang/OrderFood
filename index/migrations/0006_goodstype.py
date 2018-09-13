# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-09-06 09:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_auto_20180905_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='商品类型名称')),
                ('picture', models.ImageField(null=True, upload_to='static/upload/goodstype', verbose_name='商品类型图片')),
                ('desc', models.TextField(verbose_name='商品类型描述')),
            ],
            options={
                'db_table': 'GoodsType',
                'verbose_name': '商品类型',
                'verbose_name_plural': '商品类型',
            },
        ),
    ]