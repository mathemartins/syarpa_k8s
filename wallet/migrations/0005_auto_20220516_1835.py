# Generated by Django 3.2.10 on 2022-05-16 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0004_binancecoin_binanceusd'),
    ]

    operations = [
        migrations.CreateModel(
            name='TetherUSDBEP20',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, max_length=256, null=True)),
                ('name', models.CharField(default='TetherUSD', max_length=256)),
                ('short_name', models.CharField(default='USDT', max_length=12)),
                ('network', models.CharField(default='BEP20', max_length=256)),
                ('icon', models.URLField(blank=True, null=True)),
                ('encrypted_private_key', models.TextField(blank=True, null=True)),
                ('public_key', models.CharField(blank=True, help_text='address', max_length=256, null=True)),
                ('previous_bal', models.DecimalField(decimal_places=18, default=0, max_digits=100)),
                ('available_bal', models.DecimalField(decimal_places=18, default=0, max_digits=100)),
                ('frozen', models.BooleanField(default=False)),
                ('frozen_bal', models.DecimalField(decimal_places=18, default=0, max_digits=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'tetherUsdBEP20',
                'verbose_name_plural': 'tetherUsdBEP20',
                'db_table': 'tetherUsdBEP20',
            },
        ),
        migrations.CreateModel(
            name='TetherUSDTRC20',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, max_length=256, null=True)),
                ('name', models.CharField(default='TetherUSD', max_length=256)),
                ('short_name', models.CharField(default='USDT', max_length=12)),
                ('network', models.CharField(default='BEP20', max_length=256)),
                ('icon', models.URLField(blank=True, null=True)),
                ('encrypted_private_key', models.TextField(blank=True, null=True)),
                ('public_key', models.CharField(blank=True, help_text='address', max_length=256, null=True)),
                ('previous_bal', models.DecimalField(decimal_places=18, default=0, max_digits=100)),
                ('available_bal', models.DecimalField(decimal_places=18, default=0, max_digits=100)),
                ('frozen', models.BooleanField(default=False)),
                ('frozen_bal', models.DecimalField(decimal_places=18, default=0, max_digits=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'tetherUsdTRC20',
                'verbose_name_plural': 'tetherUsdTRC20',
                'db_table': 'tetherUsdTRC20',
            },
        ),
        migrations.CreateModel(
            name='Tron',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, max_length=256, null=True)),
                ('name', models.CharField(default='Tron', max_length=256)),
                ('short_name', models.CharField(default='TRX', max_length=12)),
                ('icon', models.URLField(blank=True, null=True)),
                ('encrypted_private_key', models.TextField(blank=True, null=True)),
                ('public_key', models.CharField(blank=True, help_text='address', max_length=256, null=True)),
                ('previous_bal', models.DecimalField(decimal_places=18, default=0, max_digits=100)),
                ('available_bal', models.DecimalField(decimal_places=18, default=0, max_digits=100)),
                ('frozen', models.BooleanField(default=False)),
                ('frozen_bal', models.DecimalField(decimal_places=18, default=0, max_digits=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'tron',
                'verbose_name_plural': 'tron',
                'db_table': 'tron',
            },
        ),
        migrations.AddField(
            model_name='tetherusd',
            name='network',
            field=models.CharField(default='ERC20', max_length=256),
        ),
    ]
