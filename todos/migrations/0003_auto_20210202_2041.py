# Generated by Django 3.1.5 on 2021-02-02 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0002_auto_20210202_2037'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='todo_text',
            new_name='text',
        ),
    ]