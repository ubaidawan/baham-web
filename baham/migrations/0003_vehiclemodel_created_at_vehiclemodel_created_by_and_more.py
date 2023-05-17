
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('baham', '0002_userprofile_remove_companion_user_ptr_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiclemodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehiclemodel',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_vehicle_models', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vehiclemodel',
            name='date_voided',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='vehiclemodel',
            name='is_voided',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vehiclemodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='vehiclemodel',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_vehicle_models', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vehiclemodel',
            name='void_reason',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='vehiclemodel',
            name='voided_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='voided_vehicle_models', to=settings.AUTH_USER_MODEL),
        ),
    ]