# Generated by Django 3.1.2 on 2020-10-10 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('url', models.TextField()),
                ('company_name', models.TextField()),
                ('city', models.CharField(max_length=255)),
                ('salary', models.CharField(max_length=255)),
                ('employment', models.TextField()),
                ('prog_lang', models.TextField()),
                ('skills', models.TextField()),
                ('data_bases', models.TextField()),
                ('description', models.TextField()),
            ],
        ),
    ]