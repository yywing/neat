# Generated by Django 3.1 on 2020-09-13 06:41

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Raw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheme', models.CharField(choices=[('http', 'HTTP'), ('https', 'HTTPS')], max_length=255)),
                ('host', models.CharField(max_length=255)),
                ('port', models.IntegerField(validators=[django.core.validators.MaxValueValidator(65535), django.core.validators.MinValueValidator(1)])),
                ('raw_request', models.BinaryField(help_text='原始请求', max_length=5120)),
                ('raw_response', models.BinaryField(help_text='原始响应', max_length=1048576, null=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('PATCH', 'PATCH'), ('DELETE', 'DELETE'), ('MOVE', 'MOVE'), ('COPY', 'COPY'), ('HEAD', 'HEAD'), ('OPTIONS', 'OPTIONS'), ('TRACE', 'TRACE'), ('LINK', 'LINK'), ('UNLINK', 'UNLINK'), ('WRAPPED', 'WRAPPED'), ('EXTENSION_METHOD', 'EXTENSION_METHOD')], default='GET', help_text='请求方法', max_length=255)),
                ('request_headers', models.JSONField(editable=False, help_text='原始请求')),
                ('request_body', models.BinaryField(help_text='请求 body', max_length=5120)),
                ('request_type', models.CharField(choices=[('empty', 'empty'), ('json', 'json'), ('form', 'form'), ('other', 'other')], default='other', help_text='请求类型', max_length=255)),
                ('raw', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='request', to='raw.raw')),
            ],
            options={
                'ordering': ['url'],
            },
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheme', models.CharField(choices=[('http', 'HTTP'), ('https', 'HTTPS')], editable=False, max_length=255)),
                ('host', models.CharField(editable=False, max_length=255)),
                ('port', models.IntegerField(editable=False, validators=[django.core.validators.MaxValueValidator(65535), django.core.validators.MinValueValidator(1)])),
                ('path', models.CharField(editable=False, max_length=255)),
                ('url', models.CharField(editable=False, max_length=255, unique=True)),
                ('suffix', models.CharField(editable=False, max_length=255)),
            ],
            options={
                'ordering': ['url'],
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_code', models.IntegerField(editable=False, help_text='响应码')),
                ('response_header', models.JSONField(editable=False, help_text='原始请求')),
                ('response_body', models.BinaryField(help_text='响应 body', max_length=5120)),
                ('response_type', models.CharField(choices=[('empty', 'empty'), ('jsonp', 'jsonp'), ('html', 'html'), ('json', 'json'), ('form', 'form'), ('xml', 'xml'), ('image', 'image'), ('font', 'font'), ('css', 'css'), ('js', 'js'), ('other', 'other')], default='other', help_text='响应类型', max_length=255)),
                ('raw', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='response', to='raw.raw')),
                ('request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='response', to='raw.request')),
                ('url', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='response', to='raw.url')),
            ],
            options={
                'ordering': ['url'],
            },
        ),
        migrations.AddField(
            model_name='request',
            name='url',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='raw.url'),
        ),
        migrations.AddField(
            model_name='raw',
            name='url',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raws', to='raw.url'),
        ),
        migrations.AddConstraint(
            model_name='response',
            constraint=models.UniqueConstraint(fields=('url', 'raw', 'request'), name='unique_response'),
        ),
        migrations.AddConstraint(
            model_name='request',
            constraint=models.UniqueConstraint(fields=('url', 'raw'), name='unique_request'),
        ),
    ]
