# Generated by Django 2.2.4 on 2020-08-26 23:53

from django.db import migrations, models
import django.db.models.deletion
import upload.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login_app', '0003_auto_20200819_0851'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=55)),
                ('slug', models.SlugField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Sound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('soundfile', models.FileField(blank=True, null=True, upload_to=upload.models.Sound.get_upload_path, verbose_name='')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload.Category')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sounds_created', to='login_app.User')),
            ],
        ),
    ]