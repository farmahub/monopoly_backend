# Generated by Django 5.2 on 2025-04-13 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0002_property_colspan_property_colstart_property_rowspan_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='colSpan',
            new_name='h',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='colStart',
            new_name='w',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='rowSpan',
            new_name='x',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='rowStart',
            new_name='y',
        ),
    ]
