# Generated by Django 4.2.4 on 2023-08-24 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_alter_testquestion_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='OptionImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='options/')),
            ],
        ),
    ]
