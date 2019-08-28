# Generated by Django 2.2.1 on 2019-08-28 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('backend', '0009_auto_20190828_2056'),
    ]

    operations = [
        migrations.CreateModel(
            name='Duration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('consumingtime', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Rectangle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('x1', models.FloatField()),
                ('y1', models.FloatField()),
                ('x2', models.FloatField()),
                ('y2', models.FloatField()),
            ],
        ),
    ]
