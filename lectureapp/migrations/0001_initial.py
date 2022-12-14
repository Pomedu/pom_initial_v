# Generated by Django 3.2 on 2022-08-06 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teacherapp', '0001_initial'),
        ('studentapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('status', models.CharField(choices=[('P', '대기'), ('O', '진행중'), ('F', '종강')], max_length=20)),
                ('cost', models.IntegerField()),
                ('students', models.ManyToManyField(related_name='lectures', through='lectureapp.CourseRegistration', to='studentapp.Student')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lectures', to='teacherapp.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='CourseTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('1', '월'), ('2', '화'), ('3', '수'), ('4', '목'), ('5', '금'), ('6', '토'), ('0  ', '일')], max_length=3)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time', to='lectureapp.lecture')),
            ],
        ),
        migrations.AddField(
            model_name='courseregistration',
            name='lecture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='lectureapp.lecture'),
        ),
        migrations.AddField(
            model_name='courseregistration',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='studentapp.student'),
        ),
        migrations.AlterUniqueTogether(
            name='courseregistration',
            unique_together={('student', 'lecture')},
        ),
    ]
