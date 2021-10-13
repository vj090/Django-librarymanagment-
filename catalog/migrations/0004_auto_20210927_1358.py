# Generated by Django 3.2.7 on 2021-09-27 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_venue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='contact_number',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='venue',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='venue',
            name='last_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]