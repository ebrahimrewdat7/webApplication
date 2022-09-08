from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import  logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from odcs.UserBackEnd import UserBackEnd
from odcs.form import AddEmpForm
from odcs.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def login(request):
    return render(request, "login.html")

def do_login(request):
    
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = UserBackEnd.authenticate(request,username,password
                                         )
        if user is not None:
            auth.login(request, user)
            
            is_superuser = user.is_superuser
            
            # return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
            if is_superuser == True:
                return redirect('admin_home')

            elif is_superuser == False:
                # return HttpResponse("learner Login")
                return redirect('emp_home')
            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            return redirect('login')

@login_required()
def admin_home(request):
    if request.user.is_authenticated:

        all_admin_count = CustomUser.objects.filter(is_superuser=True).count()
        all_emp_count = CustomUser.objects.filter(is_superuser=False).count()
      

        # For Admin
        admin_name_list = []

        admins = CustomUser.objects.filter(is_superuser=True)
        for admin in admins:
            admin_name_list.append(admin.first_name)
        # For Employee
        emp_name_list = []

        emp = CustomUser.objects.filter(is_staff=True)
        for emp in emp:
            emp_name_list.append(CustomUser.first_name)

        context = {
        
            # "all_learner_count": all_learner_count,
            "all_emp_count": all_emp_count,
            "all_admin_count": all_admin_count,
            "admin_name_list": admin_name_list,
            "emp_name_list": emp_name_list,
        }
        return render(request, "admin_home.html", context)
    else:
        render(request, "login.html")
@login_required()
def emp_home(request):
    if request.user.is_authenticated:
        # For Learner
        emp_name_list = []

        emp = CustomUser.objects.filter(is_staff=True)
        for emp in emp:
            emp_name_list.append(emp.first_name)
            context = {

            "emp_name_list": emp_name_list,

            }
        return render(request, "emp/emp_home.html", context)
    else:
        render(request,'login.html')
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('login')

def add_emp(request):
    form = AddEmpForm()
    context = {
        "form": form
    }
    return render(request, 'add_emp.html', context)


def add_emp_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_emp')
    else:
        form = AddEmpForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            phoneNo = form.cleaned_data['phoneNo']
            if password1 == password2:
                if CustomUser.objects.filter(username=username).exists():
                    messages.info(request, 'Username Taken')
                    return redirect('add_emp')
                # elif validate_email('email'):
                # messages.info(request, 'Enter a valid email address')
                # return redirect('signup_instructor')
                elif CustomUser.objects.filter(email=email).exists():
                    messages.info(request, 'Email Taken')
                    return redirect('add_emp')
                else:
                    try:
                        user = CustomUser.objects.create_user(username=username, password=password1, email=email,
                                                              first_name=first_name, last_name=last_name,is_staff=True
                                                              ,user_type=2,phoneNo=phoneNo)
                        user.save()
                        messages.success(request, "Employee Added Successfully!!!")
                        return redirect('add_emp')
                    except:
                        messages.error(request, "Adding Employee Failed!")
                        return redirect('add_emp')
            else:
                messages.info(request, 'Password not matched')
                return redirect('add_emp')
        else:
            messages.error(request, 'Form is not Valid')
            return redirect('add_emp')

def edit_emp(request, id):
    emp = CustomUser.objects.get(id=id)
   
    context = {
        "emp": emp,
        "id": id
    }
    return render(request, "edit_emp.html", context)


def edit_emp_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        id = request.POST.get('id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')


        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            
            # INSERTING into Instructor Model


            messages.success(request, "Employee Updated Successfully.")
            return redirect('/edit_emp/'+id)

        except:
            messages.error(request, "Failed to Update Employee.")
            return redirect('/edit_emp/'+id)           
def delete_emp(request,id):
    emp = CustomUser.objects.get(id=id)
    try:
        emp.delete()
        messages.success(request, "employee Deleted Successfully.")
        return redirect('manage_emp')
    except:
        messages.error(request, "Failed to Delete Learner.")
        return redirect('manage_emp')

def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context = {
        "user": user
    }
    return render(request, 'admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')
def emp_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context = {
        "user": user
    }
    return render(request, 'emp/emp_profile.html', context)


def emp_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        dateOfBirth = request.POST.get('dateOfBirth')
        address = request.POST.get('address')
        phoneNo = request.POST.get('phoneNo')
        gender = request.POST.get('gender')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.dateOfBirth = dateOfBirth
            customuser.address = address
            customuser.phoneNo = phoneNo
            customuser.gender = gender
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('emp_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('emp_profile')


def manage_emp(request):
    emps = CustomUser.objects.filter(is_superuser=False)
    context = {
        "emps": emps
    }
    return render(request, 'manage_employee.html', context)

@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

def activate_deactivate_emp(request):
    emps = CustomUser.objects.filter(is_superuser=False).all()
    

    context = {
        "emps": emps
    }
    return render(request,"activate_deactivate_emp.html", context)
def deactivate_emp(request,id):
    
    try:
        CustomUser.objects.filter(id=id).update(is_staff=False)
        messages.success(request, "employee Deactivated Successfully.")
        return redirect('activate_deactivate_emp')
    except:
        messages.error(request, "Failed to Deactivated employee.")
        return redirect('activate_deactivate_emp')
def activate_emp(request,id):
    try:
        CustomUser.objects.filter(id=id).update(is_staff=True)
        messages.success(request, "employee Activated Successfully.")
        return redirect('activate_deactivate_emp')
    except:
        messages.error(request, "Failed to Activated employee.")
        return redirect('activate_deactivate_emp')