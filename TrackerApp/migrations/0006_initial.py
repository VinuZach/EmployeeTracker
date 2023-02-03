# Generated by Django 4.1.5 on 2023-01-22 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('TrackerApp', '0005_remove_collectiondata_companyid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyName', models.CharField(max_length=200, unique=True)),
                ('companyRepresentative', models.CharField(max_length=100)),
                ('status', models.IntegerField(choices=[(0, 'In Active'), (1, 'Active')], default=3)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locationName', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ModeOfBusiness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('businessMode', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneNumber', models.CharField(max_length=20)),
                ('companyId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TrackerApp.companydetails')),
            ],
        ),
        migrations.AddField(
            model_name='companydetails',
            name='modeOfBusiness',
            field=models.ManyToManyField(to='TrackerApp.modeofbusiness'),
        ),
        migrations.CreateModel(
            name='CollectionData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previousCollectionID', models.PositiveIntegerField(blank=True, default=0)),
                ('feasibility', models.IntegerField(choices=[(1, 'High'), (2, 'Medium'), (3, 'Low')], default=3)),
                ('followUpDate', models.DateField()),
                ('remark', models.CharField(max_length=100)),
                ('reference', models.CharField(blank=True, max_length=100)),
                ('imageFileData', models.ImageField(blank=True, upload_to='images/')),
                ('companyId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TrackerApp.companydetails')),
            ],
        ),
    ]