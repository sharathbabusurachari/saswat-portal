# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
import re
import uuid
from random import randint
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models import F, Q
from django.utils.translation import gettext as _



class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number


class UserDetails(models.Model):
    user_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=20)
    mid_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    work_dept = models.CharField(max_length=20)
    mobile_no = models.CharField(max_length=15)
    designation = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    designation_id = models.CharField(max_length=10,blank=True, null=True)

#     class Meta:
#         unique_together = ('user_id', 'mobile_no')

    def __str__(self):
        return f"{self.first_name} {self.mid_name} {self.last_name}_{self.user_id}"


class UserOtp(models.Model):
    # mobile_no = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    otp_generation_time = models.DateTimeField(auto_now_add=True)
    otp_expiration_time = models.DateTimeField()

    def __str__(self):
        return self.mobile_no

    def save(self, *args, **kwargs):

        if not self.pk:
            self.otp_expiration_time = timezone.now() + timedelta(minutes=2)
        super().save(*args, **kwargs)

    def is_expired(self):
        return self.otp_expiration_time < timezone.now()

    # @staticmethod
    # def delete_expired():
    #     expired_otps = UserOtp.objects.filter(otp_expiration_time__lte=datetime.now())
    #     expired_otps.delete()


class GpsModel(models.Model):
    user_id = models.CharField(max_length=10)
    mobile_no = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    gps_date = models.DateField()
    gps_time = models.TimeField()
    status = models.CharField(max_length=10)
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return self.name
        return str(self.id)


class Gender(models.Model):
    gender_id = models.IntegerField(primary_key=True)
    gender = models.CharField(max_length=20)

    def __str__(self):
        return self.gender


class State(models.Model):
    state_id = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=20)

    def __str__(self):
        return self.state


class CustomerTest(models.Model):
    c_id = models.IntegerField(primary_key=True)
    c_name = models.CharField(max_length=20)
    c_dob = models.DateField()
    gender_id = models.ForeignKey(Gender, on_delete=models.CASCADE, related_name='customers_gender')
    c_locality = models.CharField(max_length=200)
    state_id = models.ForeignKey(State, on_delete=models.CASCADE, related_name='customers_state')
    c_mobile_no = models.CharField(max_length=10)
    version = models.CharField(max_length=20)
    file = models.FileField(upload_to='documents/', blank=True)
    document_name = models.CharField(max_length=20)
    document_id = models.CharField(max_length=20)
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.c_name

class VleVillageInfo(models.Model):
    vle_id = models.IntegerField(primary_key=True)
    village_name = models.CharField(max_length=30, verbose_name="Village Name")
    post_office = models.CharField(max_length=30, verbose_name="Post Office")
    panchayat = models.CharField(max_length=30, verbose_name="Panchayath")
    hobli_block_kendra = models.CharField(max_length=30, verbose_name="Hobli / Block / Kendra")
    taluk = models.CharField(max_length=30, verbose_name="Taluk")
    district = models.CharField(max_length=30, verbose_name="District")
    pincode = models.CharField(max_length=20, verbose_name="Pincode")
    state = models.CharField(max_length=30, verbose_name="State")
    user_id = models.CharField(max_length=10, verbose_name="User Id")
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.vle_id)


    class Meta:
        db_table = 'vle_village_info'


class BmcBasicInformation(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="BMC Name")
    address = models.CharField(max_length=100, verbose_name="BMC / Milk Collection Centre Name and Address with PIN code")
    entity_type = models.CharField(max_length=100, verbose_name="BMC / Milk Centre Entity Type")
    dairy_associated = models.CharField(max_length=100, verbose_name="Dairy Associated")
    total_members = models.CharField(max_length=100, verbose_name="Total Members at the milk centre")
    active_milk_pouring_members = models.CharField(max_length=100, verbose_name="Active milk pouring members")
    morning_milk_pouring = models.CharField(max_length=100, verbose_name="Morning Milk pouring at centre")
    evening_milk_pouring = models.CharField(max_length=100, verbose_name="Evening milk pouring at the centre")
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.vle_id)
    class Meta:
        db_table = "bmc_basic_info"


class VleBasicInformation(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    vle_name = models.CharField(max_length=100, verbose_name="VLE Name")
    # full_name = models.CharField(max_length=255, verbose_name="VLE Name - Full Name")
    # calling_name = models.CharField(max_length=100, verbose_name="Calling Name")
    vle_age = models.CharField(max_length=100, verbose_name="VLE Age")
    vle_qualifications = models.CharField(max_length=100, verbose_name="VLE Qualifications")
    vle_current_position = models.CharField(max_length=100, verbose_name="VLE Current position at Milk Centre")
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.vle_name

    class Meta:
        db_table = "vle_basic_info"


class VleMobileNumber(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    vle_mobile_number = models.CharField(max_length=15, verbose_name="Mobile number of VLE", unique=True)
    otp = models.CharField(max_length=15, verbose_name="OTP", null=True, blank=True)
    alternative_mobile_number = models.CharField(max_length=260, verbose_name="Alternative Mobile number of VLE",
                                                 null=True, blank=True)
    alternative_mobile_numbers = models.JSONField(verbose_name="Alternative Mobile numbers of VLE",
                                                  null=True, blank=True, default=list)
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=50, verbose_name="OTP Verification Status", null=True, blank=True)
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.vle_mobile_number

    class Meta:
        db_table = "vle_mobile_number"


class PhotoOfBmc(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    vle_full_photo = models.ImageField(upload_to='vle_photos/', verbose_name="Full Photo of VLE")
    vle_with_sales_officer_photo = models.ImageField(upload_to='vle_photos/', verbose_name="Photo of VLE with Sales officer and milk centre in background")
    vle_passport_photo = models.ImageField(upload_to='vle_photos/', verbose_name="Passport Photo of VLE")
    bmc_photo_1 = models.ImageField(upload_to='bmc_photos/', verbose_name="Photo of BMC / Milk collection centre 1")
    bmc_photo_2 = models.ImageField(upload_to='bmc_photos/', verbose_name="Photo of BMC / Milk collection centre 2")
    bmc_photo_3 = models.ImageField(upload_to='bmc_photos/', verbose_name="Photo of BMC / Milk collection centre 3")
    bmc_photo_4 = models.ImageField(upload_to='bmc_photos/', verbose_name="Photo of BMC / Milk collection centre 4")
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Photo Information"

    class Meta:
        db_table = "photo_of_bmc"


class VLEBankDetails(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    cheque_or_statement = models.ImageField(upload_to='vle_documents/', verbose_name="Cheque or first page of statement or passbook")
    pan_card = models.ImageField(upload_to='vle_documents/', verbose_name="PAN Card")
    id_card = models.ImageField(upload_to='vle_documents/', verbose_name="ID card (Masked AADHAR / Driving license / Passport / Voter ID / Any govt ID)")
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return "Bank Account Details of VLE"

    class Meta:
        db_table = "vle_bank_details"


class SkillsAndKnowledge(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    smartphone_literacy = models.CharField(max_length=255, verbose_name="Smartphone literacy")
    financial_literacy = models.CharField(max_length=255, verbose_name="Financial Literacy")
    stability_of_stay = models.CharField(max_length=255, verbose_name="Stability of stay")
    financial_standing = models.CharField(max_length=255, verbose_name="Financial Standing")
    vintage_experience = models.CharField(max_length=255, verbose_name="Vintage / Experience")
    integrity = models.CharField(max_length=255, verbose_name="Integrity")
    financial_standing_sales_officer = models.CharField(max_length=255, verbose_name="Financial Standing from Sales officer understanding")
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Skills and Knowledge of VLE"

    class Meta:
        db_table = "skills_and_knowledge"


class VLEEconomicAndSocialStatusInfo(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    financial_standing_actual = models.CharField(max_length=255, verbose_name="Financial Standing - Actual")
    approximate_hh_income = models.CharField(max_length=255, verbose_name="Approximate HH income from all sources")
    network_farmers = models.CharField(max_length=255, verbose_name="Network Farmers")
    loans_taken = models.CharField(max_length=255, verbose_name="Loans taken")
    other_income_source = models.CharField(max_length=255, verbose_name="Other Income source of VLE")
    land_holding = models.CharField(max_length=255, verbose_name="Land holding of VLE")
    social_standing = models.CharField(max_length=255, verbose_name="Social standing (ability to represent Saswat)")
    influence = models.CharField(max_length=255, verbose_name="Influence (ability to handle trouble or day to day issues)")
    reference_name = models.CharField(max_length=255, verbose_name="Reference Check")
    reference_number = models.CharField(max_length=255, verbose_name="Reference Check")
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Economic and Social Status Information of VLE"

    class Meta:
        db_table = "economic_and_social_status_info"



class VleNearbyMilkCenterContact(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    # vle = models.ForeignKey('VLE', on_delete=models.CASCADE, related_name='nearby_milk_center_contacts', verbose_name="VLE")
    name = models.CharField(max_length=255, verbose_name="Name of the person", blank=True, null=True)
    mobile_number = models.CharField(max_length=15, verbose_name="Mobile number", blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name="Address of milk collection centre", blank=True, null=True)
    reason_not_provided = models.CharField(max_length=255, blank=True, null=True, verbose_name="Reason for not providing contacts (Leave this blank if above 3 fields are filled")
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True, default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
     db_table = "vle_nearby_milk_center_contact"


class VillageDetails(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    water_sources = models.CharField(max_length=255, verbose_name="Water sources details")
    number_of_houses = models.CharField(max_length=255, verbose_name="Number of houses in village")
    voting_number = models.CharField(max_length=255, verbose_name="Voting number at the village")
    approximate_population = models.CharField(max_length=255, verbose_name="Approximate village population")
    description = models.CharField(max_length=255, verbose_name="Description")
    name_of_financial_institution = models.CharField(max_length=255, verbose_name="Name of other financial institution providing loans")
    financial_institution_description = models.CharField(max_length=255, verbose_name="Financial Institution Description")
    dairy_name = models.CharField(max_length=255, verbose_name="Name of other milk center Dairy name")
    total_members = models.CharField(max_length=255, verbose_name="Total Members at the milk centre (Active milk pouring and non-milk pouring) ")
    active_milk_pouring_members = models.CharField(max_length=255, verbose_name="Active milk pouring members ")
    morning_milk_pouring = models.CharField(max_length=255, verbose_name="Morning Milk pouring at centre ")
    evening_milk_pouring = models.CharField(max_length=255, verbose_name="Evening Milk pouring at the centre ")
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Village Social, Nature, and Economic Details"

    class Meta:
        db_table = "village_details"

class VleMobileVOtp(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    otp_generation_time = models.DateTimeField(auto_now_add=True)
    otp_expiration_time = models.DateTimeField()
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'vle_mobile_no_verification'

    def __str__(self):
        return self.mobile_no

    def save(self, *args, **kwargs):
        if not self.pk:
            self.otp_expiration_time = datetime.now() + timedelta(minutes=1)
        super().save(*args, **kwargs)

    def is_expired(self):
        return self.otp_generation_time < timezone.now() - timezone.timedelta(minutes=1)


class VleOtp(models.Model):
    vle_id = models.OneToOneField(VleVillageInfo, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    otp_generation_time = models.DateTimeField(auto_now_add=True)
    otp_expiration_time = models.DateTimeField()
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=50, verbose_name="User Id")
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'vle_otp'

    def __str__(self):
        return self.mobile_no

    def save(self, *args, **kwargs):
        if not self.pk:
            self.otp_expiration_time = datetime.now() + timedelta(minutes=1)
        super().save(*args, **kwargs)

    def is_expired(self):
        return self.otp_generation_time < timezone.now() - timezone.timedelta(minutes=1)

# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*------Dashboard API------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------
# -----------------------------------*-------------------------*--------------------------------------*-----------------


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    country_id = models.IntegerField(unique=True)
    country_name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255, verbose_name="Created By")
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    modified_by = models.CharField(max_length=255, verbose_name="Modified By")

    def __str__(self):
        return self.country_name

    class Meta:
        db_table = 'country'


class District(models.Model):
    id = models.AutoField(primary_key=True)
    district_id = models.IntegerField(unique=True)
    district_name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    created_by = models.CharField(max_length=255, verbose_name="Created By")
    modified_by = models.CharField(max_length=255, verbose_name="Modified By")

    def __str__(self):
        return self.district_name

    class Meta:
        db_table = 'district'


class DesignationDetails(models.Model):
    id = models.AutoField(primary_key=True)
    designation_id = models.IntegerField(unique=True)
    designation_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    created_by = models.CharField(max_length=255, verbose_name="Created By")
    modified_by = models.CharField(max_length=255, verbose_name="Modified By")

    def __str__(self):
        return self.designation_name

    class Meta:
        db_table = 'designation_details'


class WeekDetails(models.Model):

    WEEK_DATES_FORMAT = "%d-%d"

    id = models.AutoField(primary_key=True)
    week_number = models.IntegerField(verbose_name="Week Number (e.g. 18)")
    week_name = models.CharField(max_length=20, verbose_name="Week Name (e.g. week18)")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    week_dates = models.CharField(max_length=20, verbose_name="Week Dates", editable=False)
    working_days = models.IntegerField()
    month = models.IntegerField(verbose_name="Month", editable=False)
    month_name = models.CharField(max_length=20, verbose_name="Month Name", editable=False)
    year = models.CharField(max_length=4, verbose_name="Year", editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255, verbose_name="Created By")
    modified_by = models.CharField(max_length=255, verbose_name="Modified By")

    def __str__(self):
        return f"{self.week_name}_{self.month_name}_{self.year}"

    def clean(self):
        super().clean()
        if self.start_date and self.end_date:
            if self.start_date.month != self.end_date.month or self.start_date.year != self.end_date.year:
                raise ValidationError("Start date and end date must be in the same month and year.")
            if self.start_date > self.end_date:
                raise ValidationError("End date must be greater than or equal to start date")
            overlapping_ranges = WeekDetails.objects.filter(
                start_date__lte=self.end_date,
                end_date__gte=self.start_date
            ).exclude(pk=self.pk)
            if overlapping_ranges.exists():
                raise ValidationError("The date range overlaps with an existing date range.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Perform validation before saving
        self.month = self.start_date.month
        self.month_name = self.start_date.strftime('%B')  # Format the start date to get the month name
        self.year = str(self.start_date.year)
        self.week_dates = self.WEEK_DATES_FORMAT % (self.start_date.day, self.end_date.day)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'week_details'


class EmployeeDetails(models.Model):

    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(UserDetails, on_delete=models.CASCADE,
                                 related_name='employees', verbose_name="Employee")
    designation = models.ForeignKey(DesignationDetails, on_delete=models.SET_NULL, verbose_name="Designation",
                                    blank=True, null=True)
    full_name = models.CharField(max_length=255, verbose_name="Employee Full Name")
    mobile_number = models.CharField(max_length=15, verbose_name="Mobile Number", unique=True)
    alternate_mobile_number = models.CharField(max_length=15, verbose_name="Alternate Mobile Number",
                                               blank=True, null=True)
    official_email = models.EmailField(max_length=255, verbose_name="Official Email ID", unique=True,
                                       blank=True, null=True)
    reporting_manager = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                                          related_name='reportees', verbose_name="Reporting Manager")
    cluster_head = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                                     related_name='cluster_members', verbose_name="Cluster Head")
    hobli_block = models.CharField(max_length=100, verbose_name="Hobli / Block")
    taluk = models.CharField(max_length=100, verbose_name="Taluk")
    cluster = models.CharField(max_length=100, verbose_name="Cluster")
    district = models.CharField(max_length=100, verbose_name="District")
    state = models.CharField(max_length=100, verbose_name="State")
    full_address = models.TextField(verbose_name="Full address")
    pin_code = models.CharField(max_length=10, verbose_name="PIN CODE")
    work_department = models.CharField(max_length=20, null=True, blank=True)
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255, verbose_name="Created By")
    modified_by = models.CharField(max_length=255, verbose_name="Modified By")

    def __str__(self):
        return f"{self.full_name} - {self.designation}"

    class Meta:
        db_table = "employee_details"
        unique_together = ('employee',)


class EmployeeTargetDetails(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE,
                                 related_name='employee_targets', verbose_name="Employee")
    year = models.CharField(max_length=4, verbose_name="Year", editable=False)
    month = models.IntegerField(verbose_name="Month", editable=False)
    month_name = models.CharField(max_length=20, verbose_name="Month Name", editable=False)
    week = models.ForeignKey(WeekDetails, on_delete=models.CASCADE, verbose_name="Week")
    date = models.DateField()
    visit_achieved = models.IntegerField()
    login_achieved = models.IntegerField()
    disbursement_achieved = models.IntegerField()
    version = models.IntegerField(default=1, editable=False, null=True, blank=True)
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255)
    modified_by = models.CharField(max_length=255)

    def __str__(self):
        return self.employee.full_name

    def clean(self):
        super().clean()
        if self.date and self.date > timezone.now().date():
            raise ValidationError("You can not know the Targets achieved by a user for a "
                                  "future date (Correct the Date).")
        if self.week_id and self.date:
            week = WeekDetails.objects.get(pk=self.week_id)
            if not (week.start_date <= self.date <= week.end_date):
                raise ValidationError(f"Date {self.date} is outside the range of selected week: {week.week_name} ({week.start_date} - {week.end_date})")
        if self.employee_id and self.week_id and self.date:
            month = self.date.month
            year = str(self.date.year)
            is_target_set = EmployeeSetTargetDetails.objects.filter(employee_id=self.employee_id, month=month,
                                                                    year=year, week_id=self.week_id)
            if not is_target_set.exists():
                raise ValidationError(f'Kindly set a target first for the employee - {self.employee}, '
                                      f'for the selected week.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Perform validation before saving

        if not self.pk:  # Check if it's a new entry
            # Annotate the queryset to count existing entries for the same user and date
            existing_entries_count = EmployeeTargetDetails.objects.filter(
                employee=self.employee,
                date=self.date
            ).annotate(
                num_entries=F('id')
            ).count()
            # Set the version to the count + 1
            self.version = existing_entries_count + 1

        self.month = self.date.month
        self.month_name = self.date.strftime('%B')  # Format the start date to get the month name
        self.year = str(self.date.year)
        super().save(*args, **kwargs)

    class Meta:
        db_table = "employee_target_details"


class EmployeeSetTargetDetails(models.Model):

    MONTH_CHOICES = [
        (1, 'January'), (2, 'February'), (3, 'March'),
        (4, 'April'), (5, 'May'), (6, 'June'),
        (7, 'July'), (8, 'August'), (9, 'September'),
        (10, 'October'), (11, 'November'), (12, 'December')
    ]

    YEAR_CHOICES = [(str(i), str(i)) for i in range(2020, 2051)]

    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE,
                                 related_name='employee_set_targets', verbose_name="Employee")
    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.CharField(choices=YEAR_CHOICES, max_length=4)
    month_name = models.CharField(max_length=20, verbose_name="Month Name", editable=False)
    week = models.ForeignKey(WeekDetails, on_delete=models.CASCADE, related_name='employee_week_set_targets',
                             verbose_name="Week")
    visit_target = models.IntegerField()
    login_target = models.IntegerField()
    disbursement_target = models.IntegerField()
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255)
    modified_by = models.CharField(max_length=255)

    def __str__(self):
        return self.employee.full_name

    def clean(self):
        super().clean()
        if self.employee_id and self.month and self.year and self.week_id:
            if (EmployeeSetTargetDetails.objects.
                    filter(employee=self.employee, month=self.month, year=self.year, week=self.week).exists()):
                month_name = dict(self.MONTH_CHOICES)[self.month]
                raise ValidationError(f"The Target for '{self.week}' has already been set for '{self.employee}' \
                for {month_name}-{self.year}. Kindly delete that entry first and then Create another entry")
        if self.employee_id and self.month and self.year and self.week_id:
            week_identifier_qs = WeekDetails.objects.filter(month=self.month, year=self.year)
            week_identifier_list = list(week_identifier_qs.values_list('id', flat=True))
            if self.week_id not in week_identifier_list:
                month_name = dict(self.MONTH_CHOICES)[self.month]
                raise ValidationError(f"The selected Week - '{self.week}' does not belong to {month_name},{self.year}.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Perform validation before saving
        self.month_name = dict(self.MONTH_CHOICES)[self.month]
        super().save(*args, **kwargs)

    class Meta:
        db_table = "employee_set_target_details"


class LoanApplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'PENDING'), ('CCPU HOLD', 'CCPU HOLD'), ('SALES HOLD', 'SALES HOLD'),
        ('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED'),
        ('E-SIGN RECEIVED', 'E-SIGN RECEIVED'), ('E-SIGN DONE', 'E-SIGN DONE'),
        ('DMS', 'DMS'), ('DISBURSED', 'DISBURSED'), ('AUTHORISED', 'AUTHORISED')
    ]

    id = models.AutoField(primary_key=True)
    saswat_application_number = models.CharField(max_length=10, unique=True)
    loan_id = models.CharField(max_length=10, null=True, blank=True, verbose_name="Lender ID")
    date_of_login = models.DateField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)
    customer_name = models.CharField(max_length=255)
    sales_officer = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE, verbose_name="Sales Person")
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255, verbose_name="Created By")
    modified_by = models.CharField(max_length=255, verbose_name="Modified By")

    @property
    def sales_officer_rm(self):
        if self.sales_officer and self.sales_officer.reporting_manager:
            return self.sales_officer.reporting_manager.full_name
        return None

    @property
    def sales_officer_district(self):
        return self.sales_officer.district

    @property
    def sales_officer_cluster(self):
        return self.sales_officer.cluster

    def __str__(self):
        return self.saswat_application_number

    class Meta:
        db_table = 'loan_application'

class QueryDocuments(models.Model):
    document_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.document_name

    class Meta:
        db_table = 'query_documents'


class ShortenedQueries(models.Model):
    document = models.ForeignKey(QueryDocuments, on_delete=models.CASCADE, verbose_name="AI Documents", null=True, blank=True)
    shortened_query = models.CharField(max_length=255, verbose_name="AI Shortened Query")
    description = models.CharField(max_length=255, verbose_name="AI Description", null=True, blank=True)
    additional_info = models.CharField(max_length=255, verbose_name="AI Additional Information", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.shortened_query)

    class Meta:
        db_table = 'shortened_queries'


class QueryModel(models.Model):
    QUERY_STATUS_CHOICES = [
        ('OPEN', 'OPEN'), ('ANSWERED', 'ANSWERED'), ('VERIFIED', 'VERIFIED'), ('DRAFT', 'DRAFT')
    ]
    id = models.AutoField(primary_key=True)
    saswat_application_number = models.ForeignKey(LoanApplication, on_delete=models.CASCADE)
    query_id = models.CharField(max_length=6, verbose_name="Query ID")
    query_date = models.DateField()
    document = models.ForeignKey(QueryDocuments, on_delete=models.CASCADE, verbose_name="AI Documents", null=True, blank=True)
    shortened_query = models.ForeignKey(ShortenedQueries, related_name='queries_as_shortened', on_delete=models.CASCADE, verbose_name="AI Question")
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name="AI Description")
    additional_info = models.CharField(max_length=255, null=True, blank=True, verbose_name="AI Additional Info")
    question_or_query = models.CharField(max_length=255, verbose_name="Analyst Remark")
    query_status = models.CharField(choices=QUERY_STATUS_CHOICES, max_length=20)
    remarks_by_ta = models.CharField(max_length=255, null=True, blank=True)
    remarks_by_so = models.CharField(max_length=255, null=True, blank=True)
    version = models.IntegerField(default=1, editable=False, null=True, blank=True)
    remarks = models.JSONField(max_length=255, verbose_name='Remarks', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255, verbose_name="Created By")
    modified_by = models.CharField(max_length=255, verbose_name="Modified By")

    @property
    def loan_id(self):
        return self.saswat_application_number.loan_id if self.saswat_application_number.loan_id else None

    @property
    def get_shortened_query(self, obj):
        return obj.shortened_query.shortened_query if obj.shortened_query else None

    def __str__(self):
        return str(self.saswat_application_number)

    class Meta:
        db_table = 'query_model'


class QnaAttachment(models.Model):
    query = models.ForeignKey(QueryModel, on_delete=models.CASCADE, related_name='qna_attachments')
    so_attachment = models.FileField(upload_to='so_attachments/', null=True, blank=True)
    ta_attachment = models.FileField(upload_to='ta_attachments/', null=True, blank=True)
    attach_query_id = models.CharField(max_length=6, verbose_name="Query ID", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,)
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255, verbose_name="Created By")
    modified_by = models.CharField(max_length=255, verbose_name="Modified By")
    additional_details = models.JSONField(verbose_name="Additional Details", null=True, blank=True)

    class Meta:
        db_table = 'q_n_a_attachment'

    def __str__(self):
        return str(self.query)


class SignInSignOut(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, verbose_name="User")
    client_id = models.CharField(max_length=50, verbose_name='Client ID')
    event_type = models.CharField(max_length=20, verbose_name=' Event Type (Sign In / Sign Out)')
    event_date = models.DateField(verbose_name='Event Date')
    event_time = models.TimeField(verbose_name='Event Time')
    gps = models.ForeignKey(GpsModel, on_delete=models.CASCADE, verbose_name='GPS Reference', blank=True, null=True)
    remarks = models.JSONField(max_length=1000, verbose_name='Remarks', blank=True, null=True)
    remarks_one = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        db_table = 'signin_signout'


class ESign(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, verbose_name="User")
    customer_mobile_number = models.CharField(max_length=10, verbose_name="Customer Mobile Number")
    customer_name = models.CharField(max_length=100, verbose_name="Customer Name")
    file_name = models.CharField(max_length=100, verbose_name="File Name")
    file = models.FileField(upload_to='files_to_esign/', verbose_name="File to E-Sign")
    file_data_base64 = models.TextField(verbose_name="Base 64 Data of File")
    validate_login_api_response = models.JSONField(null=True, blank=True, verbose_name="Validate Login API Response")
    embedded_signing_api_response = models.JSONField(null=True, blank=True, verbose_name="Embedded SIgnin API Response")
    esign_status = models.CharField(max_length=255, null=True, blank=True, verbose_name="E Sign Status")
    remarks = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255, verbose_name="Created By", null=True, blank=True)
    modified_by = models.CharField(max_length=255, verbose_name="Modified By", null=True, blank=True)

    def __str__(self):
        return self.customer_mobile_number

    class Meta:
        db_table = 'e_sign'


class EMICollections(models.Model): # loan_details
    saswat_loan_id = models.CharField(max_length=50, verbose_name='Saswat Loan ID', null=True, blank=True) # 28-08-2024
    lender_name = models.CharField(max_length=50, verbose_name='Lender Name', blank=True, null=True)
    customer_name = models.CharField(max_length=100, verbose_name='Customer Name', blank=True, null=True)
    co_applicant_name = models.CharField(max_length=100, verbose_name='Co Applicant Name', blank=True, null=True)
    lender_loan_id = models.CharField(max_length=50, verbose_name='Lender Loan ID', unique=True)
    prospect_id = models.IntegerField(unique=True, verbose_name='Prospect Id', blank=True, null=True)
    product_name = models.CharField(max_length=100, verbose_name='Product Name', blank=True, null=True)
    bank_name = models.CharField(max_length=100, verbose_name='Bank Name', blank=True, null=True)
    branch = models.CharField(max_length=100, verbose_name='Branch Name', blank=True, null=True)
    state = models.CharField(max_length=100, verbose_name='State ', blank=True, null=True)
    cheque_no = models.CharField(max_length=100, verbose_name='Cheque Number', blank=True, null=True)
    sanctioned_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Sanctioned Amount', default=0)
    location = models.CharField(max_length=50, verbose_name='Location', blank=True, null=True)
    sm = models.CharField(max_length=50, verbose_name='SM', blank=True, null=True)
    modes = models.CharField(max_length=50, verbose_name='Modes', blank=True, null=True)
    ops = models.CharField(max_length=50, verbose_name='OPS Remark', blank=True, null=True)
    loan_status = models.CharField(max_length=100, verbose_name='Loan Status', blank=True, null=True)
    installment_no = models.IntegerField(verbose_name='Installments Number', blank=True, null=True)
    emi_amt = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='EMI Amount', default=0)
    balance_amt = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Balance Amount', default=0)
    paid_amt = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Paid Amount', default=0)
    due_date = models.DateField(verbose_name='Due Date', blank=True, null=True)
    interest = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Interest', blank=True, null=True)
    principal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Principle', blank=True, null=True)
    umrn = models.CharField(max_length=100, verbose_name='UMRN', blank=True, null=True)
    disbursed_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Disbursed Amount',default=0)
    remark = models.CharField(max_length=100, verbose_name='Remark', blank=True, null=True)
    applicant_mobile_no = models.CharField(max_length=15, verbose_name="Applicant Mobile Number",
                                           blank=True, null=True)
    co_applicant_mobile_no = models.CharField(max_length=15, verbose_name="Co-Applicant Mobile Number",
                                              blank=True, null=True)
    village_details = models.CharField(max_length=100, verbose_name="Village Details")
    block = models.CharField(max_length=100, blank=True, null=True, verbose_name="Block")
    taluk = models.CharField(max_length=100, blank=True, null=True, verbose_name="Taluk")
    cluster = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cluster")
    paid_status = models.CharField(max_length=100, blank=True, null=True, verbose_name="Paid Status")
    collections_status = models.CharField(max_length=100, verbose_name="Collection Status", default='', blank=True)
    payment_row_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Payment Row Id")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, verbose_name="Created By", null=True, blank=True)
    modified_by = models.CharField(max_length=255, verbose_name="Modified By", null=True, blank=True)

    def clean(self):
        if self.due_date:
            due_date_str = self.due_date.strftime('%d-%m-%Y')
            try:
                datetime.strptime(due_date_str, '%d-%m-%Y')
            except ValueError:
                raise ValidationError("The Due Date must be in the format dd-mm-yyyy.")
        if self.sanctioned_amount < self.disbursed_amount:
            raise ValidationError("The Sanctioned Amount must not be less than the Disbursed Amount.")

        phone_pattern = re.compile(r'^\d{10}$')

        # Validate the phone number
        if self.applicant_mobile_no and not phone_pattern.match(self.applicant_mobile_no):
            raise ValidationError({
                'applicant_mobile_no': "The Applicant Mobile Number must contain exactly 10 digits."
            })

            # Validate the co_applicant_mobile_no
        if self.co_applicant_mobile_no and not phone_pattern.match(self.co_applicant_mobile_no):
            raise ValidationError({
                'co_applicant_mobile_no': "The Co-Applicant Mobile Number must contain exactly 10 digits."
            })

    def save(self, *args, **kwargs):
        # Ensure clean is called before saving
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_name} - {self.lender_loan_id}"

    class Meta:
        db_table = 'emi_collection'


class Collection(models.Model):
    STATUS_CHOICES = [
        ('Collected', 'Collected'), ('Collected - Need to be Verified', 'Collected - Need to be Verified'),
        ('Partial collected', 'Partial collected'),
        ('Partial collected - Need to be verified', 'Partial collected - Need to be verified'),
        ('Not collected', 'Not collected')
    ]
    employee_details = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE, verbose_name="Employee Details")
    loan_details = models.ForeignKey(EMICollections, on_delete=models.CASCADE, verbose_name="Loan Details")
    status = models.CharField(choices=STATUS_CHOICES, max_length=100, verbose_name="Status")
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True, )
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255, verbose_name="Created By", null=True, blank=True)
    modified_by = models.CharField(max_length=255, verbose_name="Modified By", null=True, blank=True)
    remarks = models.JSONField(verbose_name="Additional Details", null=True, blank=True)
    collection_status = models.CharField(max_length=20, null=True, blank=True)

    def clean(self):
        # Call the parent class's clean method
        super().clean()

        # Ensure end_date is not earlier than start_date
        if self.end_date < self.start_date:
            raise ValidationError("The End Date must not be earlier than the Start Date.")

        if Collection.objects.filter(loan_details=self.loan_details).exclude(id=self.id).exists():
            raise ValidationError(_("This loan is already assigned to another employee."))

    def save(self, *args, **kwargs):
        # Ensure clean is called before saving
        self.clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.loan_details}"

    class Meta:
        db_table = 'collection'


class ModesOfPayment(models.Model):
    modes = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.modes

    class Meta:
        db_table = 'modes_of_payment'


class CollectionType(models.Model):
    type_of_collection = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type_of_collection

    class Meta:
        db_table = 'collection_type'


class CollectionPayment(models.Model): # payment collection details
    user_id = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    modes = models.ForeignKey(ModesOfPayment, on_delete=models.CASCADE, null=True, blank=True)
    loan_id = models.ForeignKey(Collection, on_delete=models.CASCADE)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    balance_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    emi_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    ref_number = models.CharField(max_length=100, null=True, blank=True)
    customer_name = models.CharField(max_length=100, null=True, blank=True)
    mobile_number = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    is_flagged = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)
    location_attachment = models.ImageField(upload_to='location_attachments/', null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    attachment = models.ImageField(upload_to='collection_attachments/', null=True, blank=True)
    promise_date = models.DateField(null=True, blank=True)
    partial_paid = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    photo_with_customer = models.ImageField(upload_to='location_attachments/', null=True, blank=True)
    house_photo = models.ImageField(upload_to='location_attachments/', null=True, blank=True)
    cattle_photo = models.ImageField(upload_to='location_attachments/', null=True, blank=True)
    vle_remark = models.CharField(max_length=100, null=True, blank=True)
    neighbour_remark = models.CharField(max_length=100, null=True, blank=True)
    customer_remark = models.CharField(max_length=100, null=True, blank=True)
    version = models.IntegerField(default=1, editable=False, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    remarks = models.JSONField(verbose_name="Additional Details", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255, verbose_name="Created By", null=True, blank=True)
    modified_by = models.CharField(max_length=255, verbose_name="Modified By", null=True, blank=True)

    def __str__(self):
        return str(self.customer_name)

    class Meta:
        db_table = 'collection_payment'


class LoanAutoPayBase(models.Model): #//copy of emi collection

    customer_name = models.CharField(max_length=100, verbose_name='Customer Name', blank=True, null=True)
    customer_email = models.CharField(max_length=100, verbose_name='Customer Email', blank=True, null=True)
    address1 = models.CharField(max_length=100, verbose_name='Customer Address 1', blank=True, null=True)
    address2 = models.CharField(max_length=100, verbose_name='Customer Address 2', blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name='Customer CITY', blank=True, null=True)
    zipcode = models.CharField(max_length=100, verbose_name='ZIPCODE', blank=True, null=True)
    county = models.CharField(max_length=100, verbose_name='Country', blank=True, null=True)
    co_applicant_name = models.CharField(max_length=100, verbose_name='Co Applicant Name', blank=True, null=True)
    lender_loan_id = models.CharField(max_length=50, verbose_name='Lender Loan ID', unique=True)
    prospect_id = models.IntegerField(unique=True, verbose_name='Prospect Id', blank=True, null=True)
    product_name = models.CharField(max_length=100, verbose_name='Product Name', blank=True, null=True)
    bank_name = models.CharField(max_length=100, verbose_name='Bank Name', blank=True, null=True)
    branch = models.CharField(max_length=100, verbose_name='Branch Name', blank=True, null=True)
    state = models.CharField(max_length=100, verbose_name='State ', blank=True, null=True)
    cheque_no = models.CharField(max_length=100, verbose_name='Cheque Number', blank=True, null=True)
    sanctioned_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Sanctioned Amount',
                                            blank=True, null=True)
    location = models.CharField(max_length=50, verbose_name='Location', blank=True, null=True)
    sm = models.CharField(max_length=50, verbose_name='SM', blank=True, null=True)
    modes = models.CharField(max_length=50, verbose_name='Modes', blank=True, null=True)
    ops = models.CharField(max_length=50, verbose_name='OPS', blank=True, null=True)
    loan_status = models.CharField(max_length=100, verbose_name='Loan Status', blank=True, null=True)
    installment_no = models.IntegerField(verbose_name='Installments Number', blank=True, null=True)
    emi_amt = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='EMI Amount', blank=True, null=True)
    due_date = models.DateField(verbose_name='Due Date', blank=True, null=True)
    interest = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Interest', blank=True, null=True)
    principal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Principle', blank=True, null=True)
    umrn = models.CharField(max_length=100, verbose_name='UMRN', blank=True, null=True)
    disbursed_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Disbursed Amount', blank=True,
                                           null=True)
    remark = models.CharField(max_length=100, verbose_name='Remark', blank=True, null=True)
    applicant_mobile_no = models.CharField(max_length=15, verbose_name="Applicant Mobile Number",
                                           blank=True, null=True)
    co_applicant_mobile_no = models.CharField(max_length=15, verbose_name="Co-Applicant Mobile Number",
                                              blank=True, null=True)
    village_details = models.CharField(max_length=100, verbose_name="Village Details")
    block = models.CharField(max_length=100, blank=True, null=True, verbose_name="Block")
    taluk = models.CharField(max_length=100, blank=True, null=True, verbose_name="Taluk")
    cluster = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cluster")
    paid_status = models.CharField(max_length=100, blank=True, null=True, verbose_name="Paid Status")
    payment_row_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Payment Row Id")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, verbose_name="Created By", null=True, blank=True)
    modified_by = models.CharField(max_length=255, verbose_name="Modified By", null=True, blank=True)

    def __str__(self):
        return f"{self.customer_name} - {self.lender_loan_id}"
    class Meta:
        db_table = 'loan_autopay_base'


class AutopayAssigned(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Initiate', 'Initiate'),
        ('Success', 'Success'),
        ('Failure', 'Failure'),
    ]
    employee_details = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE, verbose_name="Employee Details")
    loan_details = models.ForeignKey(LoanAutoPayBase, on_delete=models.CASCADE, verbose_name="Loan Details")
    status = models.CharField(choices=STATUS_CHOICES, max_length=100, verbose_name="Status")
    start_date = models.DateField()
    end_date = models.DateField()

    created_date = models.DateTimeField(auto_now_add=True, )
    modified_date = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255, verbose_name="Created By", null=True, blank=True)
    modified_by = models.CharField(max_length=255, verbose_name="Modified By", null=True, blank=True)
    remarks = models.JSONField(verbose_name="Additional Details", null=True, blank=True)

    def __str__(self):
        return f"{self.loan_details}"

    class Meta:
        db_table = 'autopay_assigned'


class CollectionAutopay(models.Model):
    user_id = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    loan_id = models.ForeignKey(AutopayAssigned, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    customer_mobile = models.CharField(max_length=100, null=True, blank=True)
    customer_email = models.EmailField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    max_amount = models.DecimalField(max_digits=8, decimal_places=2)
    product_info = models.CharField(max_length=100)
    final_collection_date = models.DateField(null=True, blank=True)
    sub_merchant_id = models.CharField(max_length=100, null=True, blank=True)
    address_one = models.TextField()
    address_two = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=6)
    initiate_payment_api_response = models.JSONField(null=True, blank=True)
    debit_request_api_response = models.JSONField(null=True, blank=True)
    transaction_status_api_response = models.JSONField(null=True, blank=True)
    cancel_mandate_api_response = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True)
    remarks = models.JSONField(verbose_name="Additional Details", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255, verbose_name="Created By", null=True, blank=True)
    modified_by = models.CharField(max_length=255, verbose_name="Modified By", null=True, blank=True)

    def __str__(self):
        return self.customer_mobile

    class Meta:
        db_table = 'collection_autopay'


class EMIDetails(models.Model):
    emi_details_id = models.AutoField(primary_key=True)
    lender_name = models.CharField(max_length=50, verbose_name='Lender Name', blank=True, null=True)
    lender_loan_id = models.ForeignKey(EMICollections, on_delete=models.CASCADE, verbose_name="Loan Details")
    type_of_emi = models.CharField(max_length=50, verbose_name='Type Of EMI', blank=True, null=True)
    due_date = models.DateField(verbose_name='Due Date')
    modes = models.CharField(max_length=50, verbose_name='Modes', blank=True, null=True)
    ops_remark = models.CharField(max_length=50, verbose_name='OPS Remark', blank=True, null=True)
    bank_name = models.CharField(max_length=100, verbose_name='Bank Name')
    cheque_no = models.CharField(max_length=100, verbose_name='Cheque Number', blank=True, null=True)
    installment_no = models.IntegerField(verbose_name='Installments Number', blank=True, null=True)
    emi_amt = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='EMI Amount', default=0)
    interest = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Interest', default=0)
    principal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Principle', default=0)
    charges = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Charges', default=0)
    ref_for_charges = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ref For Charges', default=0)
    umrn = models.CharField(max_length=100, verbose_name='UMRN', blank=True, null=True)
    payment_status = models.CharField(max_length=100, verbose_name='Payment Status', blank=True, null=True)
    payment_details = models.CharField(max_length=100, verbose_name='Payment Details', blank=True, null=True)
    emi_month = models.CharField(max_length=100, verbose_name='EMI Month', blank=True, null=True)
    balance_amt = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Balance Amount', default=0)
    paid_amt = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Paid Amount', default=0)
    collections_status = models.CharField(max_length=100, verbose_name="Collection Status", default='', blank=True)
    payment_row_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Payment Row Id")

    remarks = models.JSONField(verbose_name="Additional Details", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255, verbose_name="Created By")
    modified_by = models.CharField(max_length=255, verbose_name="Modified By")

    def __str__(self):
        return str(self.lender_loan_id)

    class Meta:
        db_table = 'emi_details'
