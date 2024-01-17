# Generated by Django 4.1.3 on 2022-12-16 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MoodTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mood_score', models.IntegerField(null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('sms_received', models.DateTimeField(null=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mood_tracker_scores', to='patient.patient')),
            ],
        ),
        migrations.AddIndex(
            model_name='moodtracker',
            index=models.Index(fields=['patient', 'date'], name='mood_patient_date_index'),
        ),
        migrations.AddIndex(
            model_name='moodtracker',
            index=models.Index(fields=['patient', 'date', 'active'], name='active_tracker'),
        ),
        migrations.AddIndex(
            model_name='moodtracker',
            index=models.Index(fields=['date', 'active'], name='date_active'),
        ),
    ]