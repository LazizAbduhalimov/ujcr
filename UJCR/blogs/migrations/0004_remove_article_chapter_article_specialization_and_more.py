# Generated by Django 4.0.2 on 2023-04-25 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_authors_city_alter_authors_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='chapter',
        ),
        migrations.AddField(
            model_name='article',
            name='specialization',
            field=models.CharField(default='', max_length=70, verbose_name='Специальность'),
        ),
        migrations.AddField(
            model_name='article',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blogs.articlesection', verbose_name='Раздел'),
        ),
        migrations.AddField(
            model_name='article',
            name='udk',
            field=models.CharField(default='', max_length=255, verbose_name='УДК'),
        ),
    ]
