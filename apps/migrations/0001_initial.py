# Generated by Django 4.2.2 on 2023-08-02 17:36

import apps.managers
import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('is_verified', models.BooleanField(default=False)),
                ('otp', models.CharField(blank=True, max_length=20, null=True)),
                ('username', models.CharField(blank=True, max_length=150, null=True, unique=True)),
                ('password', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, unique=True)),
                ('address', models.TextField(blank=True, max_length=250)),
                ('jwt_token', models.CharField(blank=True, max_length=250, null=True, unique=True)),
                ('token', models.CharField(blank=True, max_length=250, null=True, unique=True)),
                ('is_logged_in', models.BooleanField(default=False)),
                ('display_picture', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='Display Picture')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'User',
            },
            managers=[
                ('objects', apps.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'Cart',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=50)),
                ('item_price', models.FloatField()),
                ('item_image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='Item Image')),
                ('is_available', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.category')),
            ],
            options={
                'db_table': 'Item',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('zip_code', models.CharField(max_length=10)),
                ('place', models.CharField(max_length=100)),
                ('payment_method', models.CharField(choices=[('CASH ON DELIVERY', 'COD'), ('UPI', 'UPI'), ('CARD', 'CARD')], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sizes', models.CharField(max_length=5, verbose_name='Item size')),
            ],
            options={
                'db_table': 'Cloth sizes',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('total_price', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.items')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.order')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.size')),
            ],
        ),
        migrations.AddField(
            model_name='items',
            name='size',
            field=models.ManyToManyField(to='apps.size'),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.cart')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.items')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.size')),
            ],
            options={
                'db_table': 'Cart_Items',
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(through='apps.CartItem', to='apps.items'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]