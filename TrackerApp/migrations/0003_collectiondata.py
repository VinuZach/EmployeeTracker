# Generated by Django 4.1.5 on 2023-01-22 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TrackerApp', '0002_delete_collectiondata'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previousCollectionID', models.PositiveIntegerField(blank=True, null=True)),
                ('feasibility', models.IntegerField(choices=[(1, 'High'), (2, 'Medium'), (3, 'Low')], default=3)),
                ('followUpDate', models.DateField()),
                ('remark', models.CharField(max_length=100)),
                ('reference', models.CharField(blank=True, max_length=100)),
                ('imageFileData', models.ImageField(blank=True, upload_to='images/')),
                ('companyId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TrackerApp.companydetails')),
            ],
        ),
    ]