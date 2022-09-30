# Generated by Django 3.2 on 2022-08-06 11:48

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teacherapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consulting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=100)),
                ('client_phone_number', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='올바른 전화번호 양식을 입력해주세요 ex)010-0000-0000', regex='^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')])),
                ('client_school', models.CharField(max_length=20, null=True)),
                ('client_grade', models.CharField(choices=[('M1', '중1'), ('M2', '중2'), ('M3', '중3'), ('H1', '고1'), ('H2', '고2'), ('H3', '고3'), ('E4', '초4'), ('E5', '초5'), ('E6', '초6')], max_length=20)),
                ('content', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('P', '대기'), ('F', '완료'), ('N', '재상담요')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('in_charge_A', models.ForeignKey(blank=True, limit_choices_to={'role': 'A'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consultings', to=settings.AUTH_USER_MODEL)),
                ('in_charge_T', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consultings', to='teacherapp.teacher')),
            ],
        ),
    ]
