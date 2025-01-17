from django.db import models

# Create your models here.
# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    phone= models.IntegerField()
    profile_pic = models.FileField(upload_to='profile',blank=True, null=True)
    def __str__(self):
        return f"{self.name}"
    
class Shop(models.Model):
    shopname = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    phone= models.IntegerField()
    profile_pic = models.FileField(upload_to='profile',blank=True, null=True)
    def __str__(self):
        return f"{self.shopname}"
class Product(models.Model):
    productname=models.CharField(max_length=100)
    price=models.IntegerField()
    brand=models.CharField(max_length=20)
    product_pic = models.FileField(upload_to='profile',blank=True, null=True)
    def __str__(self):
        return f"{self.productname}"
    
    
    
    
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.name}"
    
class Feedback(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        ]
        
    feedback_text = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
         return f"Rating: {self.rating}, Feedback: {self.feedback_text[:50]}..."
     
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.name}"
    
import qrcode
from io import BytesIO
from django.core.files import File
from django.urls import reverse
from django.db import models
import os


class Pet(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pet_images/')
    price = models.IntegerField(blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Ensure instance is saved once to generate an ID
        if not self.id:
            super().save(*args, **kwargs)  # Save the object to generate an ID

        # Generate the pet detail URL for the QR code
        pet_url = f"http://0.0.0.0:8000{reverse('pet_detail', args=[self.id])}"

        # Check if a QR code already exists, remove the old file if present
        if self.qr_code and os.path.exists(self.qr_code.path):
            os.remove(self.qr_code.path)

        # Create the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(pet_url)
        qr.make(fit=True)

        # Save the QR code image
        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        # Assign the QR code file to the field
        self.qr_code.save(f'pet_{self.id}_qrcode.png', File(buffer), save=False)

        # Final save to ensure QR code is persisted
        super().save(*args, **kwargs)

    def str(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    phone = models.IntegerField()
    profile_pic = models.FileField(upload_to='profile', blank=True, null=True)
    
    specialization = models.CharField(max_length=100, blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)  # Qualifications info
    years_of_experience = models.PositiveIntegerField(default=0)  # Experience in years
    
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
        # Choices for availability
    DAYS_OF_WEEK = [
        ('MONDAY', 'Monday'),
        ('TUESDAY', 'Tuesday'),
        ('WEDNESDAY', 'Wednesday'),
        ('THURSDAY', 'Thursday'),
        ('FRIDAY', 'Friday'),
        ('SATURDAY', 'Saturday'),
        ('SUNDAY', 'Sunday'),
    ]

    # List to store available days of the week
    availability = models.CharField(
        max_length=50,
        choices=DAYS_OF_WEEK,
        blank=True,
        null=True,
        help_text="Select the days of the week available."
    )

    def __str__(self):
        return f"{self.name}, {self.specialization}"



class VetAppointment(models.Model):
    pet_name = models.CharField(max_length=255)
    pet_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')  # Add doctor
    appointment_date = models.DateTimeField()
    pet_type = models.CharField(max_length=100)  # Dog, Cat, etc.
    reason_for_visit = models.TextField()  # Description of the reason for the appointment
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Completed', 'Completed')], default='Pending')

    def __str__(self):
        return f"{self.pet_name} - {self.appointment_date} with {self.doctor.name}"

class Payment(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)  # The pet being purchased
    buyer_name = models.CharField(max_length=200)  # Name of the buyer
    buyer_email = models.EmailField()  # Email of the buyer
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Payment amount
    payment_id = models.CharField(max_length=200, blank=True, null=True)  # Razorpay payment ID
    order_id = models.CharField(max_length=200, blank=True, null=True)  # Razorpay order ID
    status = models.CharField(max_length=50, choices=[('PENDING', 'Pending'), ('SUCCESS', 'Success'), ('FAILED', 'Failed')], default='PENDING')
    date = models.DateTimeField(auto_now_add=True)  # Timestamp of the payment

    def __str__(self):
        return f"Payment for {self.pet.name} by {self.buyer_name} - {self.get_status_display()}"
class Payment2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed')], default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
class UserPet(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=50, choices=[('Male', 'Male'), ('Female', 'Female')])
    color = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pet_image/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pets")  # Link to User
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    def __str__(self):
        return f"{self.name} - {self.owner.name}"
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        pet_url = f"http://0.0.0.0:8000{reverse('pet_detail', args=[self.id])}"




        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(pet_url)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        self.qr_code.save(f'pet_{self.id}_qrcode.png', File(buffer), save=False)
        super().save(*args, **kwargs)
    
class Vaccinations(models.Model):
    pet = models.ForeignKey(UserPet, on_delete=models.CASCADE, related_name="vaccinations")
    vaccine_name = models.CharField(max_length=100)
    batch_number = models.CharField(max_length=100)
    veterinarian = models.CharField(max_length=100)
    date_administered =models.DateTimeField(auto_now_add=True)
    next_due_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vaccination for {self.pet.name} - {self.vaccine_name}"

class Adopt(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pet_image/')
    price=models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'),('Adopted', 'Adopted')], default='Pending')
    
from django.db import models

class Shelter(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    phone = models.IntegerField()
    profile_pic = models.FileField(upload_to='profile', blank=True, null=True)
    available_slots = models.IntegerField(default=0)  # Number of available slots
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)  # Price per day

    def __str__(self):
        return f"{self.name}"

    def reduce_slot(self):
        self.available_slots -= 1
        self.save()

class ShelterBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    details = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)  # Start date of the shelter booking
    end_date = models.DateField(null=True, blank=True)    # End date of the shelter booking
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Total price for the booking

    def __str__(self):
        return f"Booking by {self.user.name} at {self.shelter.name}"

    def calculate_total_price(self):
        # Calculate the total price based on the number of days booked
        days = (self.end_date - self.start_date).days
        self.total_price = days * self.shelter.price_per_day
        self.save()
class PetInsurance(models.Model):
    pet = models.OneToOneField(UserPet, on_delete=models.CASCADE, related_name='insurance')
    provider = models.CharField(max_length=255)
    policy_number = models.CharField(max_length=255)
    coverage = models.CharField(max_length=255)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)

    def __str__(self):
        return f"Insurance for {self.pet.name} - {self.provider}"
class Adoptpet(models.Model):
    adopter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adopted_pets')
    pet = models.ForeignKey(Adopt, on_delete=models.CASCADE)
    adopt_date = models.DateTimeField(auto_now_add=True)