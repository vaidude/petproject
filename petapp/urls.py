from .import views
from django.urls import path

urlpatterns = [
    path('',views.index,name='index'),
    path('index/',views.index,name='index'),
         
    path('register/', views.register, name='register'),
    path('shopregister/',views.shopregister, name='shopregister'),  
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('shoplogin/', views.shoplogin, name='shoplogin'),
    path('home/', views.home, name='home'),
    path('shophome/', views.shophome, name='shophome'),
    
    path('shoplist/', views.shoplist, name='shoplist'),
    path('deleteshop/<int:id>/',views.deleteshop, name='deleteeshop'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('products/', views.products, name='products'),
    path('productlist/', views.productlist, name='productlist'),
    path('deleteproduct/<int:id>/', views.deleteproduct, name='deleteproduct'),
    
    path('pet_list/', views.pet_list, name='pet_list'),  
    path('add_pet/', views.add_pet, name='add_pet'),  
    path('delete/<int:pet_id>/', views.delete_pet, name='delete_pet'),
    path('pet_detail/<int:id>/', views.pet_detail, name='pet_detail'),
    path('buy_pet/', views.buy_pet, name='buy_pet'),
    path('payment/<int:id>/', views.process_payment, name='payment'),

    path('addvaccination/', views.add_vaccination, name='addvaccination'),
    path('adduserpet/', views.adduserpet, name='adduserpet'),
    path('mypet/', views.mypet, name='mypet'),
    path('vaccination/', views.vaccination_history,name='vaccination'),
    path('adopt/',views.addadopt, name='adopt'),
    path('adoptlist/', views.adopt_list, name='adoptlist'),
    path('petadopt/<int:id>/', views.petadopt, name='petadopt'),
    
    path('profile/', views.profile, name='profile'),
    path('editprofile/', views.editprofile, name='editprofile'),
    
    path('shopprofile/', views.shopprofile, name='shopprofile'),
    path('editshopprofile/', views.shopeditprofile, name='editshopprofile'),
    path('userlist/', views.userlist, name='userlist'),
    path('deleteuser/<int:id>/', views.deleteuser, name='deleteuser'),
    path('send_notifications/', views.send_notifications, name='send_notifications'),
    path('notifications/', views.notifications, name='notifications'),


    path('shelterregister/', views.shelterregister, name='shelterregister'),
    path('shelterlogin/', views.shelterlogin, name='shelterlogin'),
    path('shelterhome/',views.shelterhome,name='shelterhome'),
    path('shelterprofile/', views.shelterprofile, name='shelterprofile'),
    path('shelterlist/', views.shelterlist, name='shelterlist'),
    path('shelter/', views.book_shelter, name='shelter'),
    path('ShelterBooklist/', views.ShelterBooklist, name='ShelterBooklist'),
    
    path('adlogin/', views.adlogin, name='adlogin'),
    path('adhome/', views.adhome, name='adhome'),
    path('feedback/', views.feedback_rate, name='feedback'),
    path('feedbacklist/',views.feedbacklist,name='feedbacklist'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('delete_cart/<int:id>', views.delete_cart, name='delete_cart'),
    path('checkout/', views.cart_checkout, name='cart_checkout'),
    
    path('doctorregister/', views.register_doctor, name='doctorregister'),
    path('doctorlogin/', views.doctorlogin, name='doctorlogin'),
    path('doctorhome/', views.doctorhome, name='doctorhome'),
    path('doctorprofile/', views.doctorprofile, name='doctorprofile'),
    path('editdoctorprofile/', views.editdoctorprofile, name='editdoctorprofile'),
    
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('appointment-success/', views.appointment_success, name='appointment_success'),
    path('appointments/', views.doctor_appointments, name='doctor_appointments'),
    
    path('chatbot/', views.chatbot, name='chatbot'),
    path('classify/', views.classify, name='classify'),
     
    path('pet_insurance_view/<int:pet_id>/', views.pet_insurance_view, name='pet_insurance_view'),
    path('pet_insurance/<int:pet_id>/', views.add_or_update_pet_insurance, name='pet_insurance'),
    
]