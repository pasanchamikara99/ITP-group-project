
############################ pasan start###############################

from contextlib import redirect_stderr
from http.client import HTTPResponse
from pickle import NONE
from re import template
from urllib import response
from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from authentication.models import EmployeesReg,Leave,employee_positions,leave_types
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
from django.core.mail import send_mail
from datetime import datetime

import re







# Create your views here.

context = {}
employee = {}
leave = {}

#send employee to his userid and password
def sendMail(fname,email,empID,password):

    subject = "Employee Registration"
    message = "Hello " + fname + "\nYour Employee id is " + empID + "\nUser password is  " + password
    #server = smtplib.SMTP('smtp.gmail.com',587)
    #server.starttls()
    #server.login('jayanandanafachion@gmail.com','ncipterepthpugjl')
    #server.sendmail('jayanandanafashion@gmail.com',email,subject)

    send_mail(
        subject,message,'jayanandanafachion@gmail.com',[email]
    )




##register employee to the system
def register(request):

    if request.method == "POST":

        empID = request.POST['empid']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        position = request.POST['position']
        password = request.POST.get('password')
        passwordc = request.POST.get('passwordc')

        ##null point validation
        if len(empID) == 0  or len(fname) == 0 or len(lname) == 0 or len(email) == 0 or len(position) == 0 or len(password) == 0 or len(passwordc) == 0:
            messages.success(request,"Please fill all the fields !!! ")
       
        else:
            patt = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,3}'
            pattern = re.compile(patt)
            
            ##validate email
            if re.match(pattern,email) is None :
                messages.success(request,"invalid email , try again !!! ")
                
            #check password are match
            elif password != passwordc :
                messages.success(request,"Password mismatch , try again !!! ")

            ##check employee id already in database
            elif EmployeesReg.objects.filter(empid = empID).exists() :
                messages.success(request,"Employee ID already exists, try new ID  !!! ")
        
        ##elif EmployeesReg.objects.filter(email = email).exists() :
               # messages.success(request,"Employee email already exists, try new email  !!! ")

            else:
                saveRecord = EmployeesReg()
                saveRecord.empid = empID
                saveRecord.fname = fname
                saveRecord.lname = lname
                saveRecord.email = email
                saveRecord.position = position
                saveRecord.password = make_password(password) ##password hashing
                
                saveRecord.save()  ##save data in DB

                sendMail(fname,email,empID,password)#call mail function
                messages.success(request,"Employee Registraion sucessfully")

           
           
    return  redirect("adminpage")




def index(request):
    context = {}
    return  render(request,"index.html",context)



    

def login(request):

    if request.method == "POST":
        empID = request.POST['empid']
        password = request.POST.get('password')

        employees = EmployeesReg.objects.all()  ##get all the employee details in DB

        for emp in employees:   
            flag = check_password(password,emp.password) ##check hashed password
            if emp.empid == empID and flag :
                empid = request.POST.get('empid',None)
                context['empid'] = empid
                context['fname'] = emp.fname
                employee['fname'] = emp.fname
                leave['fname'] = emp.fname


                ##add session values
                request.session['username'] = emp.fname
                request.session['empid'] = empid
                request.session['type'] = emp.position
                           
                if emp.position == "admin" :  ## user position admin redire to admin page
                    messages.success(request,"Admin login sucessfully")
                    return  redirect("adminpage")
                else :
                    messages.success(request,"Employee login sucessfully")
                    return  redirect("userpage")
                 

   
   
    messages.info(request,"Invalid Login")
    return  redirect("index")



def adminpage(request):


    if 'username' not in request.session:
        return  redirect("index")
    else :
        type = request.session.get('type')

        if type != "admin":
            return  redirect("index")
        else:
            result = EmployeesReg.objects.all() 
            count = EmployeesReg.objects.all().count() 
            position = employee_positions.objects.all().count() 
            positiondetails = employee_positions.objects.all()

            admincount = EmployeesReg.objects.filter(position = "admin").count()
            salescount = EmployeesReg.objects.filter(position = "salesManager").count()
            ordercount = EmployeesReg.objects.filter(position = "order manager").count()
            eventcount = EmployeesReg.objects.filter(position = "Event manager").count()
            stockcount = EmployeesReg.objects.filter(position = "Stock manager").count()
            employeecount = EmployeesReg.objects.filter(position = "Employee manager").count()
            suppliercount = EmployeesReg.objects.filter(position = "supplier manager").count()

            employee["count"] = count
            employee["position"] = position
            employee["details"] = result
            employee["positionDetails"] = positiondetails
            employee["admincount"] = admincount
            employee["ordercount"] = ordercount
            employee["salescount"] = salescount
            employee["eventcount"] = eventcount
            employee["stockcount"] = stockcount
            employee["employeecount"] = employeecount
            employee["suppliercount"] = suppliercount

            employee['navabar'] = "adminPage"


            return render(request,"admin.html",employee)






def userpage(request):

    if 'username' in request.session:
        return render(request,"user.html",context)
    else :
        return redirect("index")

    






def changepassword(request):



    if 'username' not in request.session:
        return render(request,"index.html",context)
    else :
        context['navbar'] = "changePassword"
        if request.method == "POST":
            empID = request.POST.get('empid')
            password = request.POST.get('password')
            passwordc = request.POST.get('passwordc')


            if len(password) == 0 or len(password) == 0:  ##check passwords are null or not
                messages.success(request,"Please fill all the fields !!! ")
                return  redirect("changepassword")
            
            ##check password are match
            else:
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



def applyOT(request,id):
 
    if 'username' not in request.session:
        return render(request,"index.html",context)
    else :
        
        if request.method == "POST":
            empID = request.POST.get('empid')
            otHours = request.POST.get('othours')
           
        
            if len(otHours) == 0 :
                messages.success(request,"Please fill all the feilds")
            else:
                subject = "Apply OT "
                message = "Employee ID : " + empID + "\n And Total No of OT Hours : " + otHours 
                send_mail(
                        subject,message,'jayanandanafachion@gmail.com',['pasanchamikara989@gmail.com']
                    )
                messages.success(request,"Apply OT  sucessfully")
                return  redirect("userpage")


        return render(request,"applyOT.html",context)









def applyleave(request,id):
 
    if 'username' not in request.session:
        return render(request,"index.html",context)
    else :
        
        leave_type = leave_types.objects.all()
        count = Leave.objects.filter(empid = id , status = "approve").count()
        leaves = Leave.objects.filter(empid = id)
        context['leaveType'] = leave_type
        context['count'] = count
        context['navbar'] = "leavePage"
        context['leaves'] = leaves
        context['avaliable'] = 20 - count

        today = datetime.now()
    
        if request.method == "POST":
            empID = request.POST.get('empid')
            date = request.POST.get('date')
            reason = request.POST.get('reason')
            leavetype = request.POST.get('leavetype')

            past = datetime.strptime(date, '%Y-%m-%d')
        

            if len(reason) == 0 or len(date) == 0 :
                messages.success(request,"Please fill all the feilds")
            elif past.date() < today.date():
                messages.success(request,"Please select  valid date ")

            elif count > 20 :
                messages.success(request,"Cannot apply leave ...  ")
            else:
                saveRecord = Leave()
                saveRecord.empid = empID
                saveRecord.date = date
                saveRecord.reason = reason
                saveRecord.leaveType = leavetype
                saveRecord.status = "pending"
                saveRecord.save()
                messages.success(request,"Apply leave sucessfully")
                return  redirect("userpage")


        return render(request,"applyleave.html",context)


#def generatepdf(request):

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




def printFile(request):

    employee = EmployeesReg.objects.all()

    template_path = 'pdf.html'  ##get template
    context['pdf'] = employee

    response = HttpResponse(content_type = 'application/pdf')
    response['content_Disposition'] = 'filename = "employee_report.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html,dest=response)
    
    if pisa_status.err:
        return HttpResponse('We had some errors')
    return response




def update_emp(request,id):
    positiondetails = employee_positions.objects.all() ##get all employee position details
    employee = EmployeesReg.objects.get(id = id) ##get employee details using id
    context['id'] = employee.id
    context['empid'] = employee.empid
    context['fname'] = employee.fname
    context['lname'] = employee.lname
    context['email'] = employee.email
    context['position'] = employee.position
    context['positiondetails'] = positiondetails
    return render(request,"updateEmp.html",context)  ##load all data to update employee detail template





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



def view_emp(request,id):
    employee = EmployeesReg.objects.get(empid = id)##get employee details using id
    leave_count = Leave.objects.filter(empid = id).count 
    context['id'] = employee.id
    context['empid'] = employee.empid
    context['fname'] = employee.fname
    context['lname'] = employee.lname
    context['email'] = employee.email
    context['position'] = employee.position
    context['total_leave'] = leave_count

    

    template_path = 'leave_report.html'  ##get template

    response = HttpResponse(content_type = 'application/pdf')
    response['content_Disposition'] = 'filename = "employee_report_leave.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html,dest=response)
    
    if pisa_status.err:
        return HttpResponse('We had some errors')
    return response
    
    







def delete_emp(request,id):
    employee = EmployeesReg.objects.get(id = id)
    empLeave = Leave.objects.filter(empid = employee.empid)  
    context['item'] = employee

    if request.method == "POST":
        empLeave.delete()
        employee.delete()
        messages.success(request,"Delete details sucessfully")
        return  redirect("adminpage")
 

    
    return render(request,'confirmDelete.html',context)





def delete_position(request,id):  
    position = employee_positions.objects.get(id = id)  
    employee = EmployeesReg.objects.filter(position = position.name)
    context['item'] = position

    if request.method == "POST":
        position.delete()
        employee.delete()
        messages.success(request,"Delete details sucessfully")
        return  redirect("adminpage")
   
    return render(request,'deletePosition.html',context)





def leaves(request):

    if 'username' not in request.session:
        return  redirect("index")
    else :
        type = request.session.get('type')

        if type != "admin":
            return  redirect("index")
        else :
            result = Leave.objects.all()
            pending_list = Leave.objects.filter(status = "pending") 
            count = EmployeesReg.objects.all().count()
            leave_type = leave_types.objects.all()
            leave_type_count = leave_types.objects.all().count()
            pending = Leave.objects.filter(status = "pending").count()
            reject = Leave.objects.filter(status = "reject").count()
            approve = Leave.objects.filter(status = "approve").count()

            leave['approve'] = approve
            leave['leaveDetails'] = result
            leave['reject'] = reject
            leave['count'] = count
            leave['pending_list'] = pending_list
            leave['pendingCount'] = pending
            leave['leave_type'] = leave_type
            leave['leave_type_count'] = leave_type_count

            leave['navabar'] = "leavePage"

            return render(request,"table.html",leave)



def leaveMail(fname,email,date,status):

    #subject = "Hello " + fname + "\n Your Leave request on   " + date + "\n is  " + status
    #server = smtplib.SMTP('smtp.gmail.com',587)
    #server.starttls()
    #server.login('jayanandanafachion@gmail.com','ncipterepthpugjl')
    #server.sendmail('jayanandanafashion@gmail.com',email,subject)

    subject = "Leave Application"
    message = "Hello " + fname + "\n Your Leave request on   " + date + "\n is  " + status
    
    send_mail(
        subject,message,'jayanandanafachion@gmail.com',[email]
    )


def approve_leave(request,id):
    leave = Leave.objects.get(id = id)
    saveRecord = Leave()
    saveRecord.id = leave.id
    saveRecord.empid = leave.empid
    saveRecord.date = leave.date
    saveRecord.leaveType = leave.leaveType
    saveRecord.reason = leave.reason
    saveRecord.status = "approve"
    saveRecord.save()

    result = EmployeesReg.objects.get(empid=leave.empid)
    status = "approve"
    leaveMail(result.fname,result.email,leave.date,status)
    messages.success(request,"Approve  leave Sucessfully")

    return  redirect("leaves")

def reject_leave(request,id):
    leave = Leave.objects.get(id = id)
    saveRecord = Leave()
    saveRecord.id = leave.id
    saveRecord.empid = leave.empid
    saveRecord.date = leave.date
    saveRecord.leaveType = leave.leaveType
    saveRecord.reason = leave.reason
    saveRecord.status = "reject"
    saveRecord.save()

    result = EmployeesReg.objects.get(empid=leave.empid)
    status = "rejected"
    leaveMail(result.fname,result.email,leave.date,status)
    messages.success(request,"Reject  leave Sucessfully")

    return  redirect("leaves")


def addNewLeave(request):
     if request.method == "POST":
        leaveType = request.POST['leaveType']
        description = request.POST.get('description')

        saveRecord = leave_types()
        saveRecord.leave_type = leaveType
        saveRecord.description = description
        saveRecord.save()
        messages.success(request,"Add Leave Type sucessfully")

        return  redirect("leaves")




def addNewEmpPosition(request):
     if request.method == "POST":
        positionType = request.POST['positionType']
        description = request.POST.get('description')

        saveRecord = employee_positions()
        saveRecord.name = positionType
        saveRecord.description = description
        saveRecord.save()
        messages.success(request,"Add Employee Type sucessfully")

        return  redirect("adminpage")



def delete_leave(request,id):
    leave = Leave.objects.get(id = id)   
    leave.delete()
    messages.success(request,"Delete details sucessfully")
    return  redirect("leaves")


def logout(request):
    if 'username' in request.session:
        request.session.flush()
    return redirect("index")




############################ pasan  end ###############################



       


    





    