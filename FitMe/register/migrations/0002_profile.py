# Generated by Django 4.0.4 on 2022-05-18 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('dob', models.DateField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Male', max_length=32)),
                ('height', models.CharField(max_length=50)),
                ('weight', models.DecimalField(decimal_places=1, max_digits=5)),
                ('allergies', models.CharField(max_length=500)),
                ('health_issues', models.CharField(max_length=500)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='register.person')),
            ],
        ),
    ]