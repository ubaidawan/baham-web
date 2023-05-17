from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


from baham.constants import COLOURS, TOWNS
from baham.enum_types import VehicleType, VehicleStatus, UserType


# Custom validators
def validate_colour(value):
    '''
    Validate that the value exists in the list of available colours
    '''
    return value.upper() in COLOURS


# Create your models here.
class UserProfile(models.Model):
    # Should have one-to-one relationship with Django user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField()
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    type = models.CharField(max_length=10, choices=[(t.name, t.value) for t in UserType])
    primary_contact = models.CharField(max_length=20, null=False, blank=False)
    alternate_contact = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=255)
    address_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    address_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    landmark = models.CharField(max_length=255, null=False)
    town = models.CharField(max_length=50, null=False, choices=[(c, c) for c in TOWNS])
    active = models.BooleanField(default=True, editable=False)
    date_deactivated = models.DateTimeField(editable=False, null=True)
    bio = models.TextField()

    def __str__(self):
        return f"{self.username} {self.first_name} {self.last_name}"


class VehicleModel(models.Model):
    model_id = models.AutoField(primary_key=True, db_column='id')
    # Toyota, Honda, Suzuki, Kia, etc.
    vendor = models.CharField(max_length=20, null=False, blank=False)
    # Corolla, Vitz, City, Sportage, etc.
    model = models.CharField(max_length=20, null=False, blank=False, default='Unknown')
    # Sedan, Motorcyle, SUV, Van, etc.
    type = models.CharField(max_length=50, choices=[(t.name, t.value) for t in VehicleType],
                            help_text="Select the vehicle chassis type")
    # Sitting capacity
    capacity = models.PositiveSmallIntegerField(null=False, default=2)

    is_voided = models.BooleanField(default=False)
    date_voided = models.DateTimeField(null=True)
    void_reason = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_vehicle_models')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_vehicle_models')
    voided_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='voided_vehicle_models')


    def void(self, reason):
        self.is_voided = True
        self.date_voided = datetime.now()
        self.void_reason = reason
        self.save()

    def unvoid(self):
        self.is_voided = False
        self.date_voided = None
        self.void_reason = None
        self.save()

    class Meta:
        db_table = "baham_vehicle_model"

    def __str__(self):
        return f"{self.vendor} {self.model}"


class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True, db_column='id')
    # ABC-877
    registration_number = models.CharField(max_length=10, unique=True, null=False, blank=False,
                                           help_text="Unique registration/license plate no. of the vehicle.")
    colour = models.CharField(max_length=50, default='white', validators=[validate_colour])
    model = models.ForeignKey(VehicleModel, null=False, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[(t.name, t.value) for t in VehicleStatus])
    picture1 = models.ImageField(upload_to='pictures', null=True)
    picture2 = models.ImageField(upload_to='pictures', null=True)

    def __str__(self):
        return f"{self.model.vendor} {self.model.model} {self.colour}"


class Contract(models.Model):
    contract_id = models.AutoField(primary_key=True, db_column='id')
    vehicle = models.ForeignKey(Vehicle, null=False, on_delete=models.CASCADE)
    companion = models.ForeignKey(UserProfile, null=False, on_delete=models.CASCADE)
    effective_start_date = models.DateField(null=False)
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)
    fuel_share = models.PositiveSmallIntegerField(help_text="Percentage of fuel contribution.")
    maintenance_share = models.PositiveSmallIntegerField(help_text="Percentage of maintenance cost contribution.")
    schedule = models.CharField(max_length=255, null=False)  #TODO: use Django Scheduler