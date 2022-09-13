from contextlib import redirect_stderr
from http.client import HTTPResponse
from pickle import NONE
from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from authentication.models import EmployeesReg,EmployeeLeave
from cryptography.fernet import Fernet
import smtplib
from django.contrib.auth.hashers import check_password,make_password





# Create your views here.

context = {}

#send employee to his userid and password
def sendMail(fname,email,empID,password):

    subject = "Hello " + fname + "\n Your Employee id is " + empID + "\n User password is  " + password
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('jayanandanafachion@gmail.com','ncipterepthpugjl')
    server.sendmail('jayanandanafashion@gmail.com',email,subject)



def register(request):

    if request.method == "POST":

        empID = request.POST['empid']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        position = request.POST['position']
        password = request.POST.get('password')
        passwordc = request.POST.get('passwordc')
        
        if password != passwordc :
                messages.success(request,"Password mismatch , try again !!! ")
        else:
                saveRecord = EmployeesReg()
                saveRecord.empid = empID
                saveRecord.fname = fname
                saveRecord.lname = lname
                saveRecord.email = email
                saveRecord.position = position
                #saveRecord.password = encryptedPassword(password)
                saveRecord.password = make_password(password)
                
                saveRecord.save()

                sendMail(fname,email,empID,password)#call mail function
                messages.success(request,"Employee Registraion sucessfully")

           
           
    return  render(request,"register.html")




def index(request):
    return  render(request,"index.html")



    

def login(request):

    if request.method == "POST":
        empID = request.POST['empid']
        password = request.POST.get('password')

        employees = EmployeesReg.objects.all()

        

        for emp in employees:   
            flag = check_password(password,emp.password)
            if emp.empid == empID and flag :


                empid = request.POST.get('empid',None)
                context['empid'] = empid
                context['fname'] = emp.fname

                if emp.position == "admin" :
                    messages.success(request,"Admin login sucessfully")
                    return  redirect("adminpage")
                else :
                    messages.success(request,"Employee login sucessfully")
                    return  redirect("userpage")
                 

   
   
    messages.info(request,"Invalid Login")
    return  redirect("index")



def adminpage(request):
    return render(request,"admin.html",context)

def userpage(request):
    return render(request,"user.html",context)

def changepassword(request):

    if request.method == "POST":
        empID = request.POST.get('empid')
        password = request.POST.get('password')
        passwordc = request.POST.get('passwordc')

        if password != passwordc:
            messages.success(request,"Password mismatch , try again !!! ")
            return  redirect("changepassword")
        else:
                result = EmployeesReg.objects.filter(empid=empID)   
                for re in result:
                    saveRecord = EmployeesReg()
                    saveRecord.id = re.id
                    saveRecord.empid = empID
                    saveRecord.fname = re.fname
                    saveRecord.lname = re.lname
                    saveRecord.email = re.email
                    saveRecord.position = re.position
                    saveRecord.password = make_password(password)
                    saveRecord.save()
                    messages.success(request,"Change password sucessfully")
                    return  redirect("userpage")



            


            
    


            




    



    return render(request,"changepassword.html",context)

    

        
        



    return render(request,"changepassword.html",context)



def applyleave(request):
    if request.method == "POST":
        empID = request.POST.get('empid')
        date = request.POST.get('date')
        reason = request.POST.get('reason')

        saveRecord = EmployeeLeave()
        saveRecord.empid = empID
        saveRecord.date = date
        saveRecord.reason = reason
        saveRecord.save()
        messages.success(request,"Apply leave sucessfully")


    return render(request,"applyleave.html",context)



    