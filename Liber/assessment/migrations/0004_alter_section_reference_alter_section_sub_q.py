# Generated by Django 4.2.4 on 2023-08-26 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0003_alter_section_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='reference',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='sub_q',
            field=models.CharField(max_length=300),
        ),
    ]
