# Generated by Django 4.2.4 on 2023-08-25 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0002_question_module_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='reference',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]