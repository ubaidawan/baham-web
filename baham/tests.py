# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from baham.models import UserProfile, Vehicle, Contract, VehicleModel


class VehicleContractTestCase(TestCase):
    def setUp(self):
        self.userOwner = User.objects.create_user(username='TestOwner', password='WeakestPassword')
        self.userprofileOwner = UserProfile.objects.create(user=self.userOwner, birthdate="2000-05-11", type='OWNER')
        self.vehicleModel = VehicleModel.objects.create(vendor="Honda", model="CD70", type="MOTORCYCLE", capacity="1")
        self.vehicle = Vehicle.objects.create(registration_number='ABC-123', model=self.vehicleModel, owner=self.userOwner)

        self.userCompanion = User.objects.create_user(username='TestCompanion', password='WeakestPassword')
        self.userprofileCompanion = UserProfile.objects.create(user=self.userCompanion, birthdate="2001-10-21", type='COMPANION')

        self.contract = Contract.objects.create(vehicle=self.vehicle, effective_start_date="2023-05-15", expiry_date="2023-06-15",
                                                fuel_share="50",
                                                maintenance_share="50",
                                                companion=self.userprofileCompanion,
                                                is_active=True)

    def test_one_vehicle_per_owner(self):
        with self.assertRaises(Exception):
            Vehicle.objects.create(registration_number='XYZ-789', model=self.vehicleModel, owner=self.userOwner)

    def test_passengers_capacity(self):
        with self.assertRaises(Exception):
            Contract.objects.create(vehicle=self.vehicle, effective_start_date="2023-05-31", expiry_date="2023-06-31",
                                    fuel_share="50", maintenance_share="50",
                                    companion=self.userprofileCompanion, is_active=True)

    def test_total_share(self):
        invalid_contract = Contract.objects.create(vehicle=self.vehicle, companion=self.userprofileCompanion,
                                                   effective_start_date="2023-05-31", expiry_date="2023-06-31",
                                                   is_active=True, fuel_share=110, maintenance_share=50)

        self.assertLessEqual(invalid_contract.fuel_share + invalid_contract.maintenance_share, 100)

    def test_multiple_active_contracts(self):
        invalid_contract = Contract.objects.create(vehicle=self.vehicle, companion=self.userprofileCompanion,
                                                    effective_start_date="2023-05-29", expiry_date="2023-06-10",
                                                    is_active=True, fuel_share=50, maintenance_share=30)

        self.assertFalse(invalid_contract.is_active)

    def tearDown(self):
        UserProfile.objects.all().delete()
        Vehicle.objects.all().delete()
        Contract.objects.all().delete()
        User.objects.all().delete()
