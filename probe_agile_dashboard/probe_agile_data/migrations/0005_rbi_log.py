# Generated by Django 4.2.7 on 2024-01-05 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('probe_agile_data', '0004_delete_base'),
    ]

    operations = [
        migrations.CreateModel(
            name='rbi_log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Sr_no', models.IntegerField()),
                ('source_name', models.CharField(max_length=255)),
                ('script_status', models.CharField(max_length=255)),
                ('data_available', models.IntegerField()),
                ('data_scraped', models.IntegerField()),
                ('month', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=255)),
                ('file_name', models.CharField(max_length=255)),
                ('failure_reason', models.CharField(max_length=255)),
                ('comments', models.CharField(max_length=255)),
                ('date_of_scraping', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'rbi_log',
            },
        ),
    ]