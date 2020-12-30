from django.shortcuts import render
from testapp.models import UserRegister
import re
# Create your views here.


def user_login(request):
    msg = ''
    if request.method == 'POST':
        formdata = request.POST
        user = formdata['user']
        pswd = formdata['pass']
        if user and not pswd:
            msg = "please enter password"
            return render(request, 'login.html', {'resp': msg})
        elif pswd and not user:
            msg = "please enter username"
            return render(request, 'login.html', {'resp': msg})
        elif not user or not pswd:
            msg = "please provide username and password"
            return render(request, 'login.html', {'resp': msg})
        elif UserRegister.objects.filter(userName=user,password=pswd).first():
            request.session['userinfo'] = formdata['user']
            return render(request, 'dashboard.html',{'name':formdata['user']})
        else:
            msg = 'invalid credentials..please provide correct!!'
    return render(request,'login.html',{'resp':msg})

def logout(request):
    if request.session.has_key('userinfo'):
        del request.session['userinfo']
    return render(request,'logout.html')

def emp(request):
    if request.session.has_key('userinfo'):
        return render(request,'emp.html',{'name':request.session['userinfo']})
    else:
        msg = 'You need to first login to view employee page'
        return render(request, 'login.html',{'resp': msg})

def check_for_valid_data(formdata):
    fname = formdata['fname']
    lname = formdata['lname']
    email = formdata['email']
    phone = formdata['phone']
    user = formdata['user']
    pswd = formdata['pass']
    rpswd = formdata['rpass']

    error = {}

    if len(fname)<2 or not str(fname).isalpha():
        error['FIRSTNAME'] = 'Invalid first name should be gt 2 characters'
    if len(lname) < 2 or not str(lname).isalpha():
        error['LASTNAME'] = 'Invalid last name should be gt 2 characters'
    if not re.search('\S+@\S+',email):
        error['EMAIL'] = 'Invalid email'
    if len(phone) < 10 or len(phone) > 12:
        error['PHONE'] = "invalid phone number should be integer and len in between 10-12"
    if len(user) < 2:
        error['USERNAME'] = 'Invalid user name should be gt 2 characters'
    if pswd != rpswd or len(pswd)>8:
        error['PASSWORD'] = "both passwords must be same..and length should not be excced 8.!"

    if not error:
        userobj = UserRegister(firstName=fname, lastName=lname, email=email, phoneNo=phone, userName=user,password=pswd, rpassword=rpswd)
        return userobj
    return error

def user_register(request):
    msg = ''
    if request.method == 'POST':
        formdata = request.POST
        if len(formdata['fname'])<=0 or len(formdata['lname'])<=0 or len(formdata['email'])<=0 or len(formdata['phone'])<=0 or len(formdata['user'])<=0 or len(formdata['pass'])<=0 or len(formdata['rpass'])<=0:
            msg = "All Mandatory fileds required to fill"
        else:
            result = check_for_valid_data(formdata)
            if type(result)==dict:
                return render(request, 'register.html', {"error": result})
            else:
                result.save()
                msg = 'user info saved successfully..!'
    return render(request,'register.html',{"resp":msg})

