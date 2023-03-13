# Generated by Django 4.1 on 2023-03-13 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_dob'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='text',
            new_name='body',
        ),
        migrations.RenameField(
            model_name='scrapbook',
            old_name='name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.AddField(
            model_name='comment',
            name='authorid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comment_author', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='page',
            name='body',
            field=models.CharField(default='body Default', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='page',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='title',
            field=models.CharField(default='title default', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='page', to='accounts.page'),
        ),
    ]
