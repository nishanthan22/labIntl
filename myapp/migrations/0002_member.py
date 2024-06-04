# Generated by Django 5.0.6 on 2024-06-03 21:04

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('status', models.IntegerField(choices=[(1, 'Regular member'), (2, 'Premium Member'), (3, 'Guest Member')], default=1)),
                ('address', models.CharField(max_length=300)),
                ('city', models.CharField(max_length=20)),
                ('province', models.CharField(default='ON', max_length=2)),
                ('last_renewal', models.DateField(default=django.utils.timezone.now)),
                ('auto_renew', models.BooleanField(default=True)),
                ('borrowed_books', models.ManyToManyField(blank=True, to='myapp.book')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
