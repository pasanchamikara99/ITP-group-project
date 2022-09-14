from contextlib import redirect_stderr
from http.client import HTTPResponse
from pickle import NONE
from re import template
from urllib import response
from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from authentication.models import EmployeesReg,EmployeeLeave
from cryptography.fernet import Fernet
import smtplib
from django.contrib.auth.hashers import check_password,make_password
from django.http import HttpResponse,FileResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter







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

    result = EmployeesReg.objects.all() 
    employee = {
        "details" :result
    }

    return render(request,"admin.html",employee)

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


def generatepdf(request):

    buf = io.BytesIO()
    c = canvas.Canvas(buf,pagesize=letter,bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)


    result = EmployeesReg.objects.all()

    lines = []

    for emp in result:
       lines.append("Employee ID : " + emp.empid)
       lines.append("Employee First Name : " + emp.fname)
       lines.append("Employee Last Name : " + emp.lname)
       lines.append("Employee Email : " + emp.email)
       lines.append("Employee Position : " + emp.position)
       lines.append("====================")

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)


    return FileResponse(buf,as_attachment=True,filename='employee.pdf')


def update_emp(request,id):
    employee = EmployeesReg.objects.get(id = id)
    context['id'] = employee.id
    context['empid'] = employee.empid
    context['fname'] = employee.fname
    context['lname'] = employee.lname
    context['email'] = employee.email
    context['position'] = employee.position
    return render(request,"updateuser.html",context)

def updateuser(request):
    if request.method == "POST":
        empID = request.POST['empid']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        position = request.POST['position']

        result = EmployeesReg.objects.filter(empid=empID)   
        for re in result:
            saveRecord = EmployeesReg()
            saveRecord.id = re.id
            saveRecord.empid = empID
            saveRecord.fname = fname
            saveRecord.lname = lname
            saveRecord.email = email
            saveRecord.position = position
            saveRecord.password = re.password
            saveRecord.save()
            messages.success(request,"Update details sucessfully")

    return  redirect("adminpage")


def delete_emp(request,id):

    print(id)
    employee = EmployeesReg.objects.get(id = id)

    





    