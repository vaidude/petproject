from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from .models import*
# Create your views here.

def index(request):
    return render(request, 'index.html')


def home(request):
    email=request.session.get('email')
    user = get_object_or_404(User, email=email)
    return render(request,'home.html',{'user':user})
def shophome(request):
    return render(request,'shophome.html')
def logout(request):
    request.session.flush()
    return redirect('index')
def shelterhome(request):
    return render(request,'shelterhome.html')
from django.db.models import Q
from .models import Product
import random

def products(request):
    products = Product.objects.all()
    
    query = request.GET.get('search', '')
    
    if query:
        products = products.filter(
            Q(productname__icontains=query) | Q(brand__icontains=query)
        )
    
    products = list(products)
    random.shuffle(products)

    context = {
        'products': products,
    }
    return render(request, 'products.html', context)


from django.contrib import messages
from .models import User

def addproduct(request):
    if request.method == 'POST':
        productname = request.POST.get('productname')
        price = request.POST.get('price')
        brand=request.POST.get('brand')
        product_pic = request.FILES.get('product_pic')
        Product(productname=productname, price=price,brand=brand,product_pic=product_pic).save()
        return redirect('shophome')
    return render(request, 'addproduct.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        location = request.POST.get('location')
        phone = request.POST.get('phone')

        # Simple validation
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            User.objects.create(name=name, email=email, password=password, location=location, phone=phone)
            messages.success(request, 'Registration successful!')
            return redirect('login')  # Redirect to login page or another page

    return render(request, 'register.html')
def shopregister(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        location = request.POST.get('location')
        phone = request.POST.get('phone')
        product_pic=request.FILES.get('product_pic')

        # Simple validation
        if Shop.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            Shop.objects.create(shopname=name, email=email, password=password, location=location, phone=phone,profile_pic=product_pic)
            messages.success(request, 'Registration successful!')
            return redirect('shoplogin')  # Redirect to login page or another page

    return render(request, 'shopregister.html')
from django.contrib import messages

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email, password=password)
            request.session['email'] = user.email
            return redirect('home')  # Redirect to a home page or dashboard
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid email or password.'})
    return render(request, 'login.html')

def shoplogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            shop = Shop.objects.get(email=email, password=password)
        
     
       
            request.session['email'] = shop.email
           
            return redirect('shophome')  
        except Shop.DoesNotExist:
            messages.error(request, "Invalid email or password.")
    
    return render(request, 'shoplogin.html')
def profile(request):
    email = request.session.get('email')
    
    if email is not None:
        try:
            user = User.objects.get(email=email)
            return render(request, 'profile.html', {'user': user})
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('login')  
    else:
        messages.warning(request, "You need to log in to access your profile.")
        return redirect('login') 
def shopprofile(request):
    email = request.session.get('email')
    
    if email is not None:
        try:
            user = Shop.objects.get(email=email)
            return render(request, 'shopprofile.html', {'user': user})
        except Shop.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('shoplogin')  
    else:
        messages.warning(request, "You need to log in to access your profile.")
        return redirect('shoplogin') 
def editprofile(request):
    email = request.session.get('email') 
    user = User.objects.get(email=email)  # Get the User object

    if request.method == 'POST':
        # Get the form data
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        profile_picture = request.FILES.get('profile_pic')

        # Update user profile fields
        user.name = name
        user.phone = phone
        user.location = location
        
        # Update profile picture if provided
        if profile_picture:
            user.profile_pic = profile_picture

        # Save the updated User
        user.save()

        # Send success message
        messages.success(request, 'Profile updated successfully!')

        return redirect('profile')  

    return render(request, 'profile.html', {'user': user})
def shopeditprofile(request):
    email = request.session.get('email') 
    user = Shop.objects.get(email=email)  # Get the Shop object

    if request.method == 'POST':
        # Get the form data
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        profile_picture = request.FILES.get('profile_picture')
        # Update user profile fields
        user.shopname = name
        user.phone = phone
        user.location = location
        
        # Update profile picture if provided
        if profile_picture:
            user.profile_pic = profile_picture  # Ensure this field is defined in your model

        # Save the updated User
        user.save()

        # Send success message
        messages.success(request, 'Profile updated successfully!')

        return redirect('shopprofile')  

    return render(request, 'shopprofile.html', {'user': user})
def contact(request):
    return render(request,'contact.html')

    
def logout(request):
    request.session.flush()
    return redirect('index')
def adlogin(request):
    if request.method=='POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        u = 'admin'
        p = 'admin'
        if name==u:
            if password==p:
                return redirect('adhome')
            else:
             return render(request,"adlogin.html")
        else:
             return render(request,"adlogin.html")
    else:
         return render(request,"adlogin.html")
def adhome(request):
    return render(request,'adhome.html')
def sell(request):
    if request.method == 'POST':
        productname = request.POST.get('productname')
        price = request.POST.get('price')
        brand=request.POST.get('brand')
        product_pic = request.FILES.get('product_pic')
        Product(productname=productname, price=price,brand=brand,product_pic=product_pic).save()
        return redirect('shophome')
    return render(request, 'addproduct.html')

def productlist(request):
    prod=Product.objects.all()
    return render(request, 'productlist.html', {'prod': prod})
# def products(request):
#     product=Product.objects.all()
#     return render(request,'products.html',{'product':product})

def deleteproduct(request,id):
    data=Product.objects.filter(id=id)
    data.delete()
    return redirect('productlist') 


def userlist(request):
    user=User.objects.all()
    return render(request,'userlist.html',{'user':user})
def deleteuser(request,id):
    data=User.objects.filter(id=id)
    data.delete()
    return redirect('userlist')

def shoplist(request):
    users=Shop.objects.all()
    return render(request,'shoplist.html',{'users':users})
def deleteshop(request,id):
    data=Shop.objects.filter(id=id)
    data.delete()
    return redirect('shoplist') 

def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    email = request.session.get('email')
    if email:
        user = get_object_or_404(User, email=email)
        cart_item, created = Cart.objects.get_or_create(
            user=user,
            product=product,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.total_price = cart_item.quantity * product.price
            cart_item.save()
        return redirect('cart')  # Replace 'view_cart' with your cart view name
    else:
        return JsonResponse({'authentication failed': 'User email not found in session. Please login first.'}, status=400)

  
def cart(request):
    # Retrieve the user's email from the session
    email = request.session.get('email')
    if email:

        user = get_object_or_404(User, email=email)
        cart_items = Cart.objects.filter(user=user)
        for item in cart_items:
            item.total_price = item.product.price * item.quantity
    
        total_price = sum(item.total_price for item in cart_items)
    
        return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})
    else:
        return render(request, 'cart.html', {'AUTHENTICATION FAILED': 'User email not found in session. Please login first.'})
    
    
def delete_cart(request, id):
    if request.method == "POST":
        cart_item = get_object_or_404(Cart, id=id)
        cart_item.delete()
        return redirect('cart')
    return render(request, 'cart.html')

def feedback_rate(request):
    if request.method == "POST":
        feedback_text = request.POST.get('feedback_text')
        rating = request.POST.get('rating')
        
        if not feedback_text or not rating:
            # Handle missing fields
            messages.error(request, "Please fill in all required fields.")
            
        
        try:
            rating = int(rating)
            if rating not in [1, 2, 3, 4, 5]:
                raise ValueError("Invalid rating value")
        except (ValueError, TypeError):
            # Handle invalid rating
            messages.error(request, "Invalid rating value. Please select a valid rating.")
            return HttpResponse(messages)

        # Create and save the Feedback instance
        feedback = Feedback(
            feedback_text=feedback_text,
            rating=rating
        )
        feedback.save()
        messages.success(request, "Feedback submitted successfully!")

        # Redirect to a success page
        return redirect('feedback')
    
    else:
        # Render the feedback form
        return render(request, 'feedback.html')
def feedbacklist(request):
    data=Feedback.objects.all()
    return render(request,'feedbacklist.html',{'data':data})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Notification

def send_notifications(request):
    if request.method == 'POST':
        selected_user_ids = request.POST.getlist('selected_users')
        message = request.POST.get('message')
        if selected_user_ids and message:
            selected_users = User.objects.filter(id__in=selected_user_ids)
            for user in selected_users:
                Notification.objects.create(user=user, message=message)
            messages.success(request, "Notifications sent successfully.")
            return redirect('userlist')  
        else:
            messages.error(request, "Please select at least one user and enter a message.")
            return redirect('userlist')  
    users = User.objects.all() 
    return render(request, 'sendnotification.html', {'users': users})

def notifications(request):
    email = request.session.get('email')
    
    if email:
        # Retrieve the user based on the email
        user = get_object_or_404(User, email=email)
        notifications = Notification.objects.filter(user=user).order_by('-created_at')

    return render(request, 'notifications.html', {'notifications': notifications})


def shelterregister(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        location = request.POST.get('location')
        phone = request.POST.get('phone')

        # Simple validation
        if Shelter.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            Shelter.objects.create(name=name, email=email, password=password, location=location, phone=phone)
            messages.success(request, 'Registration successful!')
            return redirect('shelterlogin')  # Redirect to login page or another page

    return render(request, 'shelterregister.html')

def shelterlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Shelter.objects.get(email=email, password=password)
        
      
          
            request.session['email'] = user.email
           
            return redirect('shelterhome')  
        except Shelter.DoesNotExist:
            return render(request, 'shelterlogin.html', {'error': 'Invalid email or password.'})

    return render(request, 'shelterlogin.html')

def shelterprofile(request):
    email = request.session.get('email')
    
    if email is not None:
        try:
            user = Shelter.objects.get(email=email)
            return render(request, 'shelterprofile.html', {'user': user})
        except Shelter.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('shelterlogin')  
    else:
        messages.warning(request, "You need to log in to access your profile.")
        return redirect('shelterlogin') 
    
def shelterlist(request):
    data=Shelter.objects.all()
    return render(request,'shelterlist.html',{'data':data})
def adlogin(request):
    if request.method=='POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        u = 'admin'
        p = 'admin'
        if name==u:
            if password==p:
                return redirect('adhome')
            else:
             return render(request,"adlogin.html")
        else:
             return render(request,"adlogin.html")
    else:
         return render(request,"adlogin.html")
def adhome(request):
    return render(request,'adhome.html')
def adduserpet(request):
    email = request.session.get('email')
    user = get_object_or_404(User, email=email)

    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        color = request.POST.get("color")
        breed = request.POST.get("breed")
        image = request.FILES.get("image")  # Ensure image is uploaded
        
        try:
            pet = UserPet(
                name=name,
                age=int(age),
                gender=gender,
                color=color,
                breed=breed,
                image=image,
                owner=user  # Set the owner to the logged-in user
            )
            pet.save()
            return redirect('mypet')  # Redirect to the vaccination or pet list page
        except ValueError:
            return render(request, 'adduserpet.html', {'error': 'Invalid input. Please check your entries.'})

    return render(request, 'adduserpet.html')

def mypet(request):
    email=request.session.get('email')
    user = get_object_or_404(User, email=email)
    pets = UserPet.objects.filter(owner=user)  # Filter pets belonging to the logged-in user
    return render(request, 'vaccinations.html', {'pets': pets})

from django.db import IntegrityError
def add_pet(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        color = request.POST.get('color')
        breed = request.POST.get('breed')
        price = request.POST.get('price')
        image = request.FILES.get('image')

        try:
            # Create a new Pet instance and save to the database
            pet = Pet.objects.create(
                name=name,
                age=age,
                gender=gender,
                color=color,
                breed=breed,
                price=price,
                image=image
            )
            return HttpResponse(
                "<script>alert('Pet added successfully!'); window.location.href='/pet_list/';</script>"
            )  # Redirect to the pet list page after adding the pet
        except IntegrityError:
            return HttpResponse(
               "<script>alert('Pet added successfully!'); window.location.href='/pet_list/';</script>"
            )
        except Exception:
            return HttpResponse(
                "<script>alert('An unexpected error occurred. Please try again later.'); window.location.href='/add_pet/';</script>"
            )

    return render(request, 'add_pet.html')


        


def pet_list(request):
    pets = Pet.objects.all()  # Get all pets from the database
    return render(request, 'petlist.html', {'pets': pets})
def addadopt(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        color = request.POST.get('color')
        breed = request.POST.get('breed')
        image = request.FILES.get('image')  # Handle image file uploads

        # Create a new Pet instance and save to the database
        pet = Adopt.objects.create(
            name=name,
            age=age,
            gender=gender,
            color=color,
            breed=breed,
            image=image
        )
        
        return redirect('adoptlist')  # Redirect to the pet list page after adding the pet
    return render(request, 'adoption.html')
def adopt_list(request):
    pets = Adopt.objects.all()  
    return render(request, 'adoptlist.html', {'pets': pets})

def petadopt(request, id):
  
    email = request.session.get('email')
    user = User.objects.get(email=email)
    pet = get_object_or_404(Adopt, id=id)

    if pet.status == 'Adopted':
     
        messages.info(request, 'This pet has already been adopted.')
        return redirect('pet_already_adopted')  

  
    pet.status = 'Adopted'
    pet.save()

 
    if Adoptpet.objects.filter(adopter=user, pet=pet).exists():
        
        messages.info(request, 'This pet is adopted')
        return redirect('adoptlist')  

    # Add the pet to the user's cart
    Adoptpet.objects.create(adopter=user, pet=pet)

    # Add a success message
    messages.success(request, 'Pet adopted successfully.')
    
    # Redirect to the adopt list page
    return redirect('adoptlist')

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import razorpay
from .models import Pet, Payment, User

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def buy_pet(request):
    pets = Pet.objects.all()  # Fetch all pets from the database
    return render(request, 'pets.html', {'pets': pets})
def pet_detail(request, id):
    pet = UserPet.objects.get(id=id)  # Get the pet with the given ID
    return render(request, 'pet_detail.html', {'pet': pet}) 
@csrf_exempt
def process_payment(request, id):
    pet = get_object_or_404(Pet, id=id)  # Fetch the selected pet
    email = request.session.get('email')
    user = User.objects.get(email=email)

    amount = int(pet.price) * 100  # Convert price to paisa
    currency = 'INR'

    if request.method == "GET":
        # Create Razorpay order
        razorpay_order = razorpay_client.order.create(
            dict(amount=amount, currency=currency, payment_capture='0')
        )
        razorpay_order_id = razorpay_order['id']

        # Save the payment record
        Payment.objects.create(
            pet=pet,
            buyer_name=user.name,
            buyer_email=user.email,
            amount=pet.price,
            order_id=razorpay_order_id,
            status='PENDING',
        )

        context = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_merchant_key': settings.RAZOR_KEY_ID,
            'razorpay_amount': amount,
            'currency': currency,
            'pet': pet,
        }

        return render(request, 'payment.html', context)

    elif request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')

            if not payment_id or not razorpay_order_id:
                print("Missing payment details.")
                return HttpResponseBadRequest("Payment details are incomplete.")

            # Directly capture payment without signature verification
            razorpay_client.payment.capture(payment_id, amount)

            # Update payment status
            payment = Payment.objects.get(order_id=razorpay_order_id)
            payment.status = 'SUCCESS'
            payment.payment_id = payment_id
            payment.save()

            return HttpResponse(
                "<script>alert('Payment successful!'); window.location.href='/buy_pet/';</script>"
            )
        except Exception as e:
            print(f"Error in payment processing: {e}")
            return HttpResponseBadRequest(f"Invalid payment request. Error: {e}")
    else:
        return HttpResponseBadRequest("Only GET and POST requests are allowed.")



# def cart_checkout(request):
#     email = request.session.get('email')
#     user = User.objects.get(email=email)
#     cart_items = Cart.objects.filter(user=user)

#     if not cart_items:
#         return redirect('cart')  # Redirect to cart if empty

#     # Calculate the total price
#     total_price = sum([item.product.price * item.quantity for item in cart_items])

#     # Create Razorpay order
#     amount = total_price * 100  # Convert price to paisa
#     razorpay_order = razorpay_client.order.create(dict(amount=amount, currency='INR', payment_capture='0'))
#     razorpay_order_id = razorpay_order['id']

#     # Save the payment record
#     Payment2.objects.create(user=user, amount=total_price, order_id=razorpay_order_id, status='PENDING')

#     context = {
#         'razorpay_order_id': razorpay_order_id,
#         'razorpay_amount': amount,
#         'cart_items': cart_items,
#         'total_price': total_price
#     }

#     return render(request,'cart_checkout.html', context)


@csrf_exempt
def cart_checkout(request):
    email = request.session.get('email')
    user = User.objects.get(email=email)
    cart_items = Cart.objects.filter(user=user)

    if not cart_items:
        return redirect('cart')  # Redirect to cart if empty

    total_price = sum([item.product.price * item.quantity for item in cart_items])
    amount = total_price * 100  # Convert to paisa

    if request.method == "GET":
        # Create Razorpay order
        razorpay_order = razorpay_client.order.create(dict(amount=amount, currency='INR', payment_capture='0'))
        razorpay_order_id = razorpay_order['id']

        # Save payment record
        Payment2.objects.create(user=user, amount=total_price, order_id=razorpay_order_id, status='PENDING')

        context = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_amount': amount,
            'cart_items': cart_items,
            'total_price': total_price,
            'user': user,
            'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        }
        return render(request, 'cart_checkout.html', context)

    elif request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')

            if not payment_id or not razorpay_order_id:
                return HttpResponseBadRequest("Payment details are incomplete.")

            # Capture payment
            razorpay_client.payment.capture(payment_id, amount)

            # Update payment status
            payment = Payment2.objects.get(order_id=razorpay_order_id)
            payment.status = 'SUCCESS'
            payment.payment_id = payment_id
            payment.save()

            # Clear cart after successful payment
            cart_items.delete()

            return HttpResponse(
                "<script>alert('Payment successful!'); window.location.href='/home/';</script>"
            )
        except Exception as e:
            print(f"Error: {e}")
            return HttpResponseBadRequest("Payment failed.")
    else:
        return HttpResponseBadRequest("Invalid request method.")





def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    pet.delete()  
    return redirect('pet_list') 

def register_doctor(request):
    if request.method == 'POST':
        # Get the form data from the request
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        location = request.POST.get('location')
        phone = request.POST.get('phone')
        specialization = request.POST.get('specialization')
        qualifications = request.POST.get('qualifications')
        years_of_experience = request.POST.get('years_of_experience')
        availability = request.POST.get('availability')
        consultation_fee = request.POST.get('consultation_fee')
        
        # Handle profile picture
        profile_pic = request.FILES.get('profile_pic')

        # Create the new doctor record
        doctor = Doctor(
            name=name,
            email=email,
            password=password,
            location=location,
            phone=phone,
            specialization=specialization,
            qualifications=qualifications,
            years_of_experience=years_of_experience,
            availability=availability,
            consultation_fee=consultation_fee,
            profile_pic=profile_pic
        )
        
        # Save the doctor instance to the database
        doctor.save()
        
        # Redirect to a success page or show a confirmation
        return redirect('doctorlogin')  # Example redirect (you can create a doctor list page)
    
    return render(request, 'doctorregister.html')

def doctorlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Doctor.objects.get(email=email, password=password)
        
      
          
            request.session['email'] = user.email
           
            return redirect('doctorhome')  # Redirect to a home page or dashboard
        except Shelter.DoesNotExist:
            return render(request, 'doctorlogin.html', {'error': 'Invalid email or password.'})

    
    return render(request, 'doctorlogin.html')

def doctorhome(request):
    return render(request, 'doctorhome.html')
def doctorprofile(request):
    email = request.session.get('email')
    
    if email is not None:
        try:
            user = Doctor.objects.get(email=email)
            return render(request, 'doctorprofile.html', {'user': user})
        except Doctor.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('doctorlogin')  
    else:
        messages.warning(request, "You need to log in to access your profile.")
        return redirect('doctorlogin') 
def editdoctorprofile(request):
    email = request.session.get('email') 

    if email is not None:
        try:
            user = Doctor.objects.get(email=email)

            if request.method == 'POST':
                # Update the doctor's details
                user.location = request.POST.get('location')
                user.phone = request.POST.get('phone')
                user.specialization = request.POST.get('specialization')
                user.qualifications = request.POST.get('qualifications')
                user.years_of_experience = request.POST.get('years_of_experience')
                user.consultation_fee = request.POST.get('consultation_fee')
                selected_days = request.POST.getlist('availability')
                user.availability = ', '.join(selected_days)

                user.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('doctorprofile')
            
            return render(request, 'doctorprofile.html', {'user': user})

        except Doctor.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('doctorlogin')
    else:
        messages.warning(request, "You need to log in to access your profile.")
        return redirect('doctorlogin')

from django.shortcuts import render, redirect
from .models import VetAppointment, Doctor

def book_appointment(request):
    doctors = Doctor.objects.all()
    email = request.session.get('email')
    
    if email:
        # Retrieve the user based on the email
        user = get_object_or_404(User, email=email)# Fetch all doctors

    if request.method == "POST":
        # Handle form submission to book an appointment
        pet_name = request.POST.get("pet_name")
        doctor_id = request.POST.get("doctor")  # Get selected doctor ID
        doctor = Doctor.objects.get(id=doctor_id)
        appointment_date = request.POST.get("appointment_date")
        pet_type = request.POST.get("pet_type")
        reason_for_visit = request.POST.get("reason_for_visit")

        # Create a new appointment
        appointment = VetAppointment(
            pet_name=pet_name,
            pet_owner=user,  # Link appointment to the logged-in user
            doctor=doctor,
            appointment_date=appointment_date,
            pet_type=pet_type,
            reason_for_visit=reason_for_visit,
        )
        appointment.save()

        # Redirect to a success page
        return redirect('appointment_success')

    # If it's a GET request, show the available doctors
    return render(request, 'book_appointment.html', {'doctors': doctors})


def appointment_success(request):
    email = request.session.get('email')
    
    if email:
        # Retrieve the user based on the email
        user = get_object_or_404(User, email=email)#
        appointment = VetAppointment.objects.filter(pet_owner=user)
        return render(request, 'appointments.html', {'appointment': appointment})
    return render(request, 'appointments.html')



def doctor_appointments(request):
  
    doctor_email = request.session.get('email')  # Assume the email is stored in the session
    if not doctor_email:
        return redirect('doctorlogin') 
    
    doctor=Doctor.objects.get(email=doctor_email)
    appointments = VetAppointment.objects.filter(doctor=doctor).order_by('appointment_date')
    
    # Handle POST request to update appointment status
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        new_status = request.POST.get('status')
        appointment = get_object_or_404(VetAppointment, id=appointment_id, doctor__email=doctor_email)
        if new_status in dict(VetAppointment._meta.get_field('status').choices):
            appointment.status = new_status
            appointment.save()
        return redirect('doctor_appointments')
    
    return render(request, 'doctorappoinments.html', {'appointments': appointments})

# In your petapp/views.py
import openai
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Set OpenAI API key
openai.api_key = settings.OPENAI_API_KEY

@csrf_exempt
def chatbot(request):
    if request.method == 'GET':
        return render(request, 'chatbot.html')  # Just renders the page for GET request

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            # Making the call to OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",  # You can use other models too (gpt-3.5-turbo, etc.)
                messages=[{"role": "user", "content": user_message}],
                max_tokens=150
            )

            chatbot_reply = response['choices'][0]['message']['content'].strip()
            return JsonResponse({'response': chatbot_reply})

        except Exception as e:
            return JsonResponse({'response': f"Error: {str(e)}"})

    return JsonResponse({'response': 'Invalid request method'}, status=405)





def add_vaccination(request):
    if request.method == 'POST':
        pet_id = request.POST.get('pet')  # Get selected pet ID
        vaccine_name = request.POST.get('vaccine_name')
        batch_number = request.POST.get('batch_number')
        veterinarian = request.POST.get('veterinarian')
        

        try:
            # Validate and save data
            pet = UserPet.objects.get(id=pet_id)  # Fetch the pet by ID
            Vaccinations.objects.create(
                pet=pet,
                vaccine_name=vaccine_name,
                batch_number=batch_number,
                veterinarian=veterinarian,
            )
            messages.success(request, "Vaccination record added successfully.")
        except UserPet.DoesNotExist:
            messages.error(request, "Invalid pet selected. Please try again.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        
        return redirect('addvaccination')

   
    pets = UserPet.objects.all()
    return render(request, 'add_vaccination.html', {'pets': pets})


def vaccination_history(request):
    email = request.session.get('email')
    user = get_object_or_404(User, email=email)
    pets = UserPet.objects.filter(owner=user)  # Fetch all pets for the user
    vaccinations = Vaccinations.objects.filter(pet__owner=user)  # Fetch vaccinations for the user's pets
    return render(request, 'pet_vaccination_history.html', {'pets': pets, 'vaccinations': vaccinations})

# views.py
import os
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
import numpy as np
from PIL import Image

# Load the pre-trained ResNet50 model
model = ResNet50(weights='imagenet')

# Function to prepare the image for classification
def prepare_image(img_path):
    img = Image.open(img_path).resize((224, 224))  # Resize the image
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

# View to handle image upload and classification
def classify(request):
    predictions = None

    if request.method == 'POST' and request.FILES['image']:
        # Get the uploaded file
        uploaded_file = request.FILES['image']
        
        # Save the file to the server (optional: customize storage location)
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
        file_path = fs.save(uploaded_file.name, uploaded_file)
        img_path = fs.url(file_path)
        
        # Prepare the image
        img_array = prepare_image(os.path.join(settings.MEDIA_ROOT, 'uploads', uploaded_file.name))
        
        # Predict breed using the model
        predictions = model.predict(img_array)
        decoded_predictions = decode_predictions(predictions, top=3)[0]
        
        # Extract the labels and scores
        predictions = [(label, score * 100) for (_, label, score) in decoded_predictions if score >= 0.70]

    return render(request, 'classify.html', {'predictions': predictions})

from datetime import datetime
def book_shelter(request):
    email = request.session.get('email')
    user = get_object_or_404(User, email=email)

    if request.method == "POST":
        # Handle shelter booking
        shelter_id = request.POST.get("shelter_id")
        details = request.POST.get("details")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        shelter = get_object_or_404(Shelter, id=shelter_id)

        if shelter.available_slots <= 0:
            messages.error(request, "No slots available at this shelter.")
        else:
            # Convert string dates to datetime objects
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
            duration = (end_date_obj - start_date_obj).days + 1
            total_price = duration * shelter.price_per_day

            # Create the booking
            booking = ShelterBooking.objects.create(
                user=user,
                shelter=shelter,
                details=details,
                start_date=start_date_obj,
                end_date=end_date_obj,
                total_price=total_price
            )

            # Calculate total price
            

            # Reduce the available slots in the shelter
            shelter.reduce_slot()

            messages.success(request, f"Shelter '{shelter.name}' booked successfully!")

    # List all shelters
    shelters = Shelter.objects.all()
    return render(request, "book_shelter.html", {"shelters": shelters})
def ShelterBooklist(request):
    email = request.session.get('email')
    user = get_object_or_404(User, email=email)
    bookings = ShelterBooking.objects.filter(user=user)
    return render(request, 'shelter_bookings.html', {'bookings': bookings})
def deletebookings(request):
    email = request.session.get('email')
    user = get_object_or_404(User, email=email)
    bookings = ShelterBooking.objects.filter(user=user)
    if request.method == 'POST':
        for booking in bookings:
            booking.delete()
        messages.success(request, "bookings deleted successfully!")
    return redirect('shelterbookings')


from datetime import datetime

def add_or_update_pet_insurance(request, pet_id):
    pet = get_object_or_404(UserPet, id=pet_id)
    # Get or create the insurance object for the pet
    insurance, created = PetInsurance.objects.get_or_create(pet=pet)

    # If the insurance is created, set a default value for the 'price' field
    if created :
        insurance.price = 0.00
        insurance.save()

    # Handle form submission (POST request)
    if request.method == 'POST':
        provider = request.POST.get('provider')
        policy_number = request.POST.get('policy_number')
        coverage = request.POST.get('coverage')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        price = request.POST.get('price')

        # Validate fields
        if not provider or not policy_number or not coverage or not start_date or not end_date or not price:
            error = "All fields are required"
            return render(request, 'petinsurance.html', {'pet': pet, 'insurance': insurance, 'error': error})

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            price = float(price)
        except ValueError:
            error = "Invalid date format or price"
            return render(request, 'petinsurance.html', {'pet': pet, 'insurance': insurance, 'error': error})

        # Update the insurance details
        insurance.provider = provider
        insurance.policy_number = policy_number
        insurance.coverage = coverage
        insurance.start_date = start_date
        insurance.end_date = end_date
        insurance.price = price
        insurance.save()

        return redirect('pet_insurance_view', pet_id=pet.id)

    # Render the form with existing insurance data
    return render(request, 'petinsurance.html', {'pet': pet, 'insurance': insurance})


def pet_insurance_view(request, pet_id):
    try:
        pet = UserPet.objects.get(id=pet_id)
        
        insurance = PetInsurance.objects.get(pet=pet)  
    except UserPet.DoesNotExist:
        return HttpResponse("Pet not found")
    except PetInsurance.DoesNotExist:
        insurance = None 
    
    return render(request, 'insurance.html', {'pet': pet, 'insurance': insurance})