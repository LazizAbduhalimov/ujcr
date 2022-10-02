# Generated by Django 4.0.2 on 2022-03-15 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0017_tags_title_en_tags_title_ru'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tags',
            options={'verbose_name': 'Ключевое слово', 'verbose_name_plural': 'Ключевые слова'},
        ),
        migrations.AddField(
            model_name='article',
            name='position',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(related_name='tags', to='blogs.Tags', verbose_name='Ключевые слова'),
        ),
    ]