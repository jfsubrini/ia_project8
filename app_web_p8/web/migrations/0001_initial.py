# Generated by Django 4.1 on 2023-01-08 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_img', models.CharField(max_length=50, unique=True, verbose_name="Titre de l'image")),
                ('image', models.ImageField(upload_to='images')),
                ('title_msk', models.CharField(max_length=50, unique=True, verbose_name='Titre du mask')),
                ('mask', models.ImageField(upload_to='masks')),
                ('title_prediction', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Titre de la prédiction')),
                ('mask_pred', models.ImageField(blank=True, null=True, upload_to='prediction')),
            ],
            options={
                'verbose_name': 'Image & Mask storing',
            },
        ),
    ]