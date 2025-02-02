import os
from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import qrcode
from PIL import Image
from django.conf import settings



# Create your views here.
from myapp.models import *


def login(request):
    return render(request,'admin/index.html')


def login_post(request):
    username=request.POST["textfield"]
    password=request.POST["textfield2"]

    a=login_table.objects.filter(username=username, password=password)
    if a.exists():
        b = login_table.objects.get(username=username, password=password)
        request.session['lid'] = b.id
        if b.type == 'admin':
            return HttpResponse('''<script>alert('success');window.location='/HOME'</script>''')
        else:
            return HttpResponse('''<script>alert('invalid');window.location='/'</script>''')
    else:
        return HttpResponse('''<script>alert('invalid');window.location='/'</script>''')


def BUSROUTE(request):
    return render(request,'admin/ADMIN_ADDBUSROUTE.html')


def BUSROUTE_post(request):
    FROM = request.POST["textfield22"]
    TO = request.POST["textfield2"]
    BUS_NO=request.POST["textfield3"]

    a=busroute_table()
    a.from1=FROM
    a.to=TO
    a.busnum=BUS_NO
    a.save()
    return HttpResponse('''<script>alert('Added');window.location='/MANAGEBUSROUTE'</script>''')





def MANAGESTUDENT(request):
    ob = busroute_table.objects.filter()
    kk = student_table.objects.all().order_by('-id')
    return render(request, 'admin/MANAGE STUDENT.html',{"val": ob, "data": kk})

def MANAGESTUDENT_post(request):
    busroute = request.POST.get("select")
    s = request.POST.get('s', '')  # Use get() to safely fetch 's' with a default empty string
    OB = busroute_table.objects.all()

    # Check if 'busroute' is provided, and filter the students accordingly
    if busroute:
        kk = student_table.objects.filter(STOP__BUSROUTE__id=busroute, name__startswith=s)
    else:
        # If no busroute selected, fetch students with the search string 's'
        kk = student_table.objects.filter(name__startswith=s)

    return render(request, 'admin/MANAGE STUDENT.html', {"val": OB, "data": kk, "busroute": int(busroute) if busroute else None})


def VERIFYSTUDENT(request):
    OB = busroute_table.objects.filter()
    x=student_table.objects.all().order_by('-id')
    return render(request,'admin/ADMIN _VERIFYSTUDENT.html',{"route":OB,"data":x})


def VERIFYSTUDENT_post(request):
    name= request.POST["select"]
    s=request.POST['s']
    x = student_table.objects.filter(name__icontains=s)
    OB = busroute_table.objects.filter()
    return render(request, 'admin/ADMIN _VERIFYSTUDENT.html', {"route": OB, "data": x})


def MANAGEBUSROUTE(request):
    ob=busroute_table.objects.all()
    return render(request,'admin/ADMIN_MANAGEBUSROUTE.html',{"val":ob})
def MANAGEBUSROUTE_post(request):
    busroute=request.POST["select"]

def EDIT_BUSROUTE(request,id):
    kk = busroute_table.objects.get(id=id)
    return render(request,'admin/EDIT_BUSROUTE.html',{"val": kk})

def EDIT_BUSROUTE_post(request):
     id = request.POST['id']
     FROM = request.POST["textfield22"]
     TO = request.POST["textfield2"]
     BUS_NO = request.POST["textfield3"]

     a = busroute_table.objects.get(id=id)
     a.from1 = FROM
     a.to = TO
     a.busnum = BUS_NO
     a.save()
     return HttpResponse('''<script>alert('Edited');window.location='/MANAGEBUSROUTE'</script>''')


def DELETE_BUSROUTE(request, id):
    ob = busroute_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('Deleted');window.location='/MANAGEBUSROUTE'</script>''')


# def BUSSTAFF(request):
#     ob = busroute_table.objects.all()
#     kk = bussstaff_table.objects.all()
#     return render(request, 'admin/ADMIN_MANAGESTAFF.html',{"val":ob,"data":kk})

def BUSSTAFF(request):
    ob = busroute_table.objects.all()
    kk = bussstaff_table.objects.select_related('BUSROUTE', 'login').all()
    return render(request, 'admin/ADMIN_MANAGESTAFF.html', {"val": ob, "data": kk})



def BUSSTAFF_post(request):
    ob = busroute_table.objects.filter()
    busroute = request.POST["select"]
    kk = bussstaff_table.objects.filter(BUSROUTE__id=busroute)
    return render(request, 'admin/ADMIN_MANAGESTAFF.html', {"val": ob, "data": kk})


def EDITSTAFF(request):
    kk = busroute_table.objects.get(id=id)
    return render(request, 'admin/EDIT_STAFF.html', {"val": kk})


def addbusstop(request):
    ob=busroute_table.objects.all()
    return render(request,'admin/ADMIN_ADDSTOP.html',{"val":ob})

def addbusstop_post(request):
    BUS_ROUTE = request.POST["select"]
    STOP = request.POST["textfield2"]
    LATITUDE = request.POST["textfield3"]
    LONGITUDE = request.POST["textfield4"]
    FEE = request.POST["textfield5"]
    a=stop_table()
    a.stop=STOP
    a.BUSROUTE=busroute_table.objects.get(id=BUS_ROUTE)
    a.latitude=LATITUDE
    a.longitude=LONGITUDE
    a.fee=FEE
    a.save()
    return HttpResponse('''<script>alert('Added');window.location='/MANAGEBUSSTOP'</script>''')


def EDITbusstop(request,id):
    request.session['sid']=id
    kk=stop_table.objects.get(id=id)
    ob=busroute_table.objects.all()
    return render(request,'admin/EDIT_BUSSTOP.html',{"val":ob,"value":kk})

def editbusstop_post(request):
    BUS_ROUTE = request.POST["select"]
    STOP = request.POST["textfield2"]
    LATITUDE = request.POST["textfield3"]
    LONGITUDE = request.POST["textfield4"]
    FEE = request.POST["textfield5"]
    a=stop_table.objects.get(id=request.session['sid'])
    a.stop=STOP
    a.BUSROUTE=busroute_table.objects.get(id=BUS_ROUTE)
    a.latitude=LATITUDE
    a.longitude=LONGITUDE
    a.fee=FEE
    a.save()
    return HttpResponse('''<script>alert('Added');window.location='/MANAGEBUSSTOP'</script>''')



def BLOCKSTUDENT(request):
    OB = student_table.objects.all().order_by('-id')
    x = busroute_table.objects.all()
    return render(request, 'admin/ADMIN_BLOCKSTUDENT.html', {"data": OB, "route": x})

def BLOCKSTUDENT_search(request):
    # route=request.POST["select"]
    route=request.POST.get("select","")
    name=request.POST.get("textfield","")
    print(request.POST)
    if route == "":
        print("===r")
        OB = student_table.objects.filter(name__icontains=name).order_by('-id')
    elif name == "":
        print("===na")
        OB = student_table.objects.filter(STOP__BUSROUTE_id=route).order_by('-id')
    else:
        print("===else")

        OB = student_table.objects.filter(STOP__BUSROUTE_id=route,name__icontains=name).order_by('-id')
    rt = request.POST["select"]
    x = busroute_table.objects.all()
    return render(request, 'admin/ADMIN_BLOCKSTUDENT.html', {"data": OB, "route": x,'busroute':int(rt)})


def BLOCKSTUDENT_post(request,id):
    ob = login_table.objects.get(id=id)
    ob.type = "BLOCK"
    ob.save()
    return HttpResponse('''<script>alert('BLOCKED');window.location='/BLOCKSTUDENT'</script>''')


def UNBLOCK(request,id):
    ob=login_table.objects.get(id=id)
    ob.type="students"
    ob.save()
    return HttpResponse('''<script>alert('accepted');window.location='/BLOCKSTUDENT'</script>''')


from django.shortcuts import render
from .models import payment_table  # Import your model


def VIEWPAYMENT(request, id):
    # Store the student ID in the session
    request.session['sid'] = id
    ob = payment_table.objects.filter(STUDENT_id=id)
    return render(request, 'admin/ADMIN_VIEWPAYMENT.html', {"val": ob})


def add_payment(request):
    id=request.session['sid']
    ob=student_table.objects.get(id=id)
    fee=ob.STOP.fee
    return render(request,'admin/admin_add_pay.html',{'fee':fee})






def insert_payment(request):
    lid=request.session['sid']
    amt=request.POST['amount']
    # package=request.POST['packageSelect']
    a = student_table.objects.get(id=lid)
    p = balance_table.objects.filter(STUDENT_id=lid)
    if p.exists():
        pl = balance_table.objects.get(STUDENT_id=lid)
        if int(pl.balance) <= 3:

            ob = payment_table()
            samt = a.STOP.fee
            tc = int(amt) // samt
            ob.STUDENT_id = lid
            ob.BUSSSTAFF_id = a.STOP.BUSROUTE.id
            ob.date = datetime.now().date()
            ob.amount = amt
            ob.save()
            obp = balance_table.objects.filter(STUDENT__id=lid)
            if len(obp) == 0:
                obp = balance_table()
                obp.STUDENT_id = lid
                obp.balance = tc
                obp.date = datetime.today()
                obp.save()

            else:
                obp = obp[0]
                obp.balance += tc
                obp.date = datetime.today()
                obp.save()

            return HttpResponse('''<script>alert('accepted');window.location='/BLOCKSTUDENT'</script>''')
        else:
            return HttpResponse('''<script>alert('rejected');window.location='/BLOCKSTUDENT'</script>''')
    else:
        ob = payment_table()
        samt = a.STOP.fee
        tc = int(amt) // samt
        ob.STUDENT_id = lid
        ob.BUSSSTAFF_id = a.STOP.BUSROUTE.id
        ob.date = datetime.now().date()
        ob.amount = amt
        ob.save()
        obp = balance_table.objects.filter(STUDENT__id=lid)
        if len(obp) == 0:
            obp = balance_table()
            obp.STUDENT_id = lid
            obp.balance = tc
            obp.date = datetime.today()
            obp.save()

        else:
            obp = obp[0]
            obp.balance += tc
            obp.date = datetime.today()
            obp.save()

        return HttpResponse('''<script>alert('accepted');window.location='/BLOCKSTUDENT'</script>''')
    return render(request,'admin/ADMIN_VIEWPAYMENT.html',{"val":fee})

def SENDNOTIFICATION(request):

    return render(request,'admin/ADMIN_SENDNOTIFICATION.html')

def SENDNOTIFICATION_POST(request):
    type= request.POST["select"]
    notification=request.POST["textarea"]

    a=notification_table()
    a.notification=notification
    a.type=type
    a.date=datetime.now().today().date()
    a.save()
    return HttpResponse('''<script>alert('Added');window.location='/SENDNOTIFICATION'</script>''')

def NOTIFICATIONTOBUS(request):
    bus = busroute_table.objects.all()

    return render(request,'admin/ADMIN_NOTIFICATIONTOBUS.html',{'bus':bus})

def NOTIFICATIONTOBUS_post(request):
    type= request.POST["bus_number"]
    notification=request.POST["notification"]

    a=busnotification()
    a.notification=notification
    a.BUSSROUTENUMBER=busroute_table.objects.get(id=type)
    a.save()
    return HttpResponse('''<script>alert('SENDED SUCCESSFULLY');window.location='/VIEWHOME'</script>''')



def VIEWCOMPLAINTS(request):
     complaint= complaint_table.objects.all().order_by('-id')
     # type=request.POST["select"]
     return render(request,'admin/ADMIN_VIEWCOMPLAINT.html',{"comp": complaint})

def VIEWCOMPLAINTS_post(request):
    s=request.POST['select']
    complaint = complaint_table.objects.filter(LOGIN__type__iexact=s)
    # type=request.POST["select"]
    return render(request, 'admin/ADMIN_VIEWCOMPLAINT.html', {"comp": complaint})


def REPLY(request,id):
    request.session['cid']=id
    return render(request,'admin/ADMIN_SENDREPLY.html')
def REPLY_post(request):
    rp= request.POST["textarea"]
    ob=complaint_table.objects.get(id=request.session['cid'])
    ob.reply=rp
    ob.save()
    return HttpResponse('''<script>alert('reply sended successfully');window.location='/VIEWCOMPLAINTS'</script>''')


def HOME(request):
    return render(request,'admin/indexhome.html')

def ADDSTUDENT(request):
    ob=busroute_table.objects.all()
    return render(request,'admin/ADMIN_ADDSTUDENT.html',{"val":ob})

def ADDSTUDENT_post(request):

    NAME= request.POST["textfield"]
    number = request.POST["textfield2"]
    BATCH = request.POST["textfield3"]
    DEPARTMENT = request.POST["textfield4"]
    ROUTE = request.POST["select1"]
    PHOTO= request.FILES["photo"]
    fn=FileSystemStorage()
    fs=fn.save(PHOTO.name,PHOTO)
    PHONE_no=request.POST["textfield7"]
    ADDRESS=request.POST["textarea"]
    username=request.POST["textfield9"]
    EMAIL=request.POST["textfield11"]
    PASSWORD=request.POST["textfield10"]
    b=login_table()
    b.username = username
    b.password = PASSWORD
    b.type="pending"
    b.save()
    a=student_table()
    a.STOP=stop_table.objects.get(id=ROUTE)
    a.name=NAME
    a.email=EMAIL
    a.phone=PHONE_no
    a.photo=fs
    a.admissions=number
    a.batch=BATCH
    a.department=DEPARTMENT
    a.address=ADDRESS
    a.balance="0"
    a.status="pending"
    a.LOGIN=b
    a.save()

    photo_url = f"{settings.MEDIA_URL}{a.photo}"
    print(a.id,"============")

    # Generate the student's details string for the QR code
    student_details = f"""
        Id: {a.id}
        Name: {a.name}
        Email: {a.email}
        Phone: {a.phone}
        Admissions: {a.admissions}
        Batch: {a.batch}
        Department: {a.department}
        Address: {a.address}
        """

    # Create a QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Higher error correction for embedded images
        box_size=10,
        border=4,
    )
    qr.add_data(student_details)
    qr.make(fit=True)

    # Convert QR code to an image
    img_qr = qr.make_image(fill='black', back_color='white').convert('RGB')

    photo_path = os.path.join(settings.MEDIA_ROOT, a.photo.name)
    student_photo = Image.open(photo_path)

      # Example size, adjust as necessary


    qr_filename = f"qr_{a.id}.png"
    qr_path = os.path.join(settings.MEDIA_ROOT, qr_filename)
    img_qr.save(qr_path)

    # Store the QR code file path in the student_table model
    a.QrCode = f"{settings.MEDIA_URL}{qr_filename}"
    a.save()

    # Return response
    return HttpResponse('''<script>alert('Added');window.location='/MANAGESTUDENT'</script>''')

#
# def EDIT_STUDENT(request, id):
#     request.session['cid'] = id
#     kk = student_table.objects.get(id=id)
#     ob = busroute_table.objects.all()
#     return render(request, 'admin/EDIT_STUDENT.html', {"val": ob, "value": kk, "selected_route_id": kk.STOP.BUSROUTE.id})

def EDIT_STUDENT(request, id):
    request.session['cid'] = id
    kk = student_table.objects.get(id=id)
    ob = busroute_table.objects.all()

    # Fetch the bus stops for the selected route
    selected_route = kk.STOP.BUSROUTE if kk.STOP else None  # Access the route from the student's associated bus stop
    bus_stops = stop_table.objects.filter(BUSROUTE=selected_route)  # Fetch bus stops based on the route

    selected_route_id = selected_route.id if selected_route else None
    selected_stop_id = kk.STOP.id if kk.STOP else None  # Get the current bus stop ID for the student

    return render(request, 'admin/EDIT_STUDENT.html', {
        "val": ob,
        "value": kk,
        "selected_route_id": selected_route_id,
        "bus_stops": bus_stops,
        "selected_stop_id": selected_stop_id,
    })







def EDIT_STUDENT_post(request):
    NAME = request.POST["textfield"]
    number = request.POST["textfield2"]
    BATCH = request.POST["textfield3"]
    DEPARTMENT = request.POST["textfield4"]
    ROUTE = request.POST["select"]


    PHONE_no = request.POST["textfield7"]
    ADDRESS = request.POST["textarea"]
    EMAIL = request.POST["textfield11"]

    if 'photo' in request.FILES:
        PHOTO = request.FILES["photo"]
        fn = FileSystemStorage()
        fs = fn.save(PHOTO.name, PHOTO)

        a = student_table.objects.get(id=request.session['cid'])
        a.BUSROUTE = busroute_table.objects.get(id=ROUTE)
        a.name = NAME
        a.email = EMAIL
        a.phone = PHONE_no
        a.photo = fs
        a.admissions = number
        a.batch = BATCH
        a.department = DEPARTMENT
        a.address = ADDRESS
        a.save()
        return HttpResponse('''<script>alert('EDITED');window.location='/MANAGESTUDENT'</script>''')
    else:
        a = student_table.objects.get(id=request.session['cid'])
        a.BUSROUTE = busroute_table.objects.get(id=ROUTE)
        a.name = NAME
        a.email = EMAIL
        a.phone = PHONE_no
        a.admissions = number
        a.batch = BATCH
        a.department = DEPARTMENT
        a.address = ADDRESS
        a.save()
        return HttpResponse('''<script>alert('EDITED');window.location='/MANAGESTUDENT'</script>''')


def DELETESTUDENT(request,id):
    ob=student_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('deleted');window.location='/MANAGESTUDENT'</script>''')


def ADDBUSSTAFF(request):
    ob=busroute_table.objects.all()
    return render(request,'admin/ADDSTAFF.html',{"val":ob})


def ADDBUSSTAFF_post(request):
    name=request.POST['textfield']
    email=request.POST['textfield1']
    phone=request.POST['textfield7']
    ROUTE=request.POST['select']
    address=request.POST['textarea']
    username=request.POST['textfield9']
    password=request.POST['textfield10']


    c=login_table()
    c.username=username
    c.password=password
    c.type='busstaff'
    c.save()

    a = bussstaff_table()
    a.BUSROUTE = busroute_table.objects.get(id=ROUTE)
    a.login = c
    a.name = name
    a.email = email
    a.phone = phone
    a.address = address
    a.username = username
    a.password = password
    a.save()
    return HttpResponse('''<script>alert('Added');window.location='/BUSSTAFF'</script>''')


def DELETEBUSSTAFF(request,id):
    ob = bussstaff_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('deleted');window.location='/BUSSTAFF'</script>''')


def EDITBUSSTAFF(request,id):
    request.session['bid']=id
    ob = bussstaff_table.objects.get(id=id)
    kk = busroute_table.objects.all()
    return render(request, 'admin/EDIT_STAFF.html', {"value": ob,"val":kk})


def EDITBUSSTAFF_post(request):
    name=request.POST['textfield']
    email=request.POST['textfield1']
    phone=request.POST['textfield7']
    ROUTE=request.POST['select']
    address=request.POST['textarea']



    a = bussstaff_table.objects.get(id=request.session['bid'])
    a.BUSROUTE = busroute_table.objects.get(id=ROUTE)

    a.name = name
    a.email = email
    a.phone = phone
    a.address = address
    a.save()
    return HttpResponse('''<script>alert('Added');window.location='/BUSSTAFF'</script>''')


def MANAGEBUSSTOP(request):
    ob = busroute_table.objects.filter()
    kk=stop_table.objects.all()
    return render(request, 'admin/MANAGEBUSSTOP.html',{"val":ob,"data":kk})


def DELETE_BUSSTOP(request,id):
    ob = stop_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('Deleted');window.location='/MANAGEBUSSTOP'</script>''')


def MANAGEBUSSTOP_post(request):
    ob = busroute_table.objects.filter()
    busroute=request.POST["select"]
    kk = stop_table.objects.filter(BUSROUTE__id=busroute)
    return render(request, 'admin/MANAGEBUSSTOP.html', {"val": ob,"data":kk})

def ACCEPT(request,id):
    ob=login_table.objects.get(id=id)
    ob.type="students"
    ob.save()
    a=student_table.objects.get(LOGIN__id=ob.id)
    photo_url = f"{settings.MEDIA_URL}{a.photo}"
    print(a.id, "============")

    # Generate the student's details string for the QR code
    student_details = f"""
            Id: {a.id}
            Name: {a.name}
            Email: {a.email}
            Phone: {a.phone}
            Admissions: {a.admissions}
            Batch: {a.batch}
            Department: {a.department}
            Address: {a.address}
            """

    # Create a QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Higher error correction for embedded images
        box_size=10,
        border=4,
    )
    qr.add_data(student_details)
    qr.make(fit=True)

    # Convert QR code to an image
    img_qr = qr.make_image(fill='black', back_color='white').convert('RGB')

    photo_path = os.path.join(settings.MEDIA_ROOT, a.photo.name)
    student_photo = Image.open(photo_path)

    # Example size, adjust as necessary


    qr_filename = f"qr_{a.id}.png"
    qr_path = os.path.join(settings.MEDIA_ROOT, qr_filename)
    img_qr.save(qr_path)

    # Store the QR code file path in the student_table model
    a.QrCode = f"{settings.MEDIA_URL}{qr_filename}"
    a.save()

    return HttpResponse('''<script>alert('accepted');window.location='/VERIFYSTUDENT'</script>''')

def REJECT(request,id):
    ob=login_table.objects.get(id=id)
    ob.type="REJECT"
    ob.save()
    return HttpResponse('''<script>alert('REJECTED');window.location='/VERIFYSTUDENT'</script>''')

def VIEWHOME(request):
    return render(request, 'admin/indexhome.html')


def LOGOUT(request):
    return render(request, 'admin/ADMIN_LOGIN.html')






def android_login(request):
    username = request.POST["username"]
    password = request.POST["password"]

    a = login_table.objects.filter(username=username, password=password)
    if a.exists():
        b = login_table.objects.get(username=username, password=password)
        print("----------",b)
        return JsonResponse({'task':'ok','lid':str(b.id),'type':b.type})

    else:
        return JsonResponse({'task': 'not ok'})



def student_register(request):
    name=request.POST['name']
    email=request.POST['email']
    phone=request.POST['phone']
    photo=request.POST['photo']
    admissions=request.POST['admissions']
    batch=request.POST['batch']
    departmentl=request.POST['department']
    address=request.POST['address']
    username=request.POST['address']
    password=request.POST['address']
    BUSROUTE=request.POST['BUSROUTE']


    a=login_table()
    a.username=username
    a.password=password
    a.type='pending'
    a.save()

    b=student_table()
    b.name=name
    b.email=email
    b.phone=phone
    b.photo=photo
    b.address=address
    b.admissions=admissions
    b.batch=batch
    b.departmentl=departmentl
    b.BUSROUTE=busroute_table.objects.get(BUSROUTE=BUSROUTE)
    b.LOGIN=a
    b.save()
    return JsonResponse({'task': 'ok'})

def student_view_profile(request):
    lid=request.POST['lid']
    a=student_table.objects.get(LOGIN_id=lid)
    print({'status': 'ok','BUSROUTE':a.STOP.BUSROUTE.busnum,'name':a.name,'email':a.email,'phone':a.phone,'photo':a.photo.url,'address':a.address,
                           'admissions': a.admissions,'batch':a.batch,'departmentl':a.department,'qr':a.QrCode})

    return JsonResponse({'status': 'ok','BUSROUTE':a.STOP.BUSROUTE.busnum,'name':a.name,'email':a.email,'phone':a.phone,'photo':a.photo.url,'address':a.address,
                           'admissions': a.admissions,'batch':a.batch,'departmentl':a.department,'qr':a.QrCode})


def student_view_qr(request):
    lid=request.POST['lid']
    a=student_table.objects.get(LOGIN_id=lid)
    print(a.QrCode)
    print(a.photo.url)
    print(a)
    return JsonResponse({'photo':a.photo.url,'qr':a.QrCode})

def student_viewbusroute(request):

    a=busroute_table.objects.all()
    l=[]
    for i in a:
        l.append({'id':i.id,'busnum':i.busnum})
    return JsonResponse({'task': 'ok','data':l})

def student_viewlocation(request):
    lid=request.POST['lid']
    bid=request.POST['bid']

    cc=student_table.objects.get(LOGIN_id=lid,BUSROUTE_id=bid)
    aa=cc.BUSROUTE

    a=location_table.objects.filter(BUSSSTAFF_id=aa)
    l=[]
    for i in a:
        l.append({'id':i.id,'latitude':i.latitude,'longitude':i.longitude})
    return JsonResponse({'task': 'ok', 'data': l})


def student_view_atteandence(request):
    lid=request.POST['lid']
    a=attendence_table.objects.filter(STUDENT__LOGIN_id=lid)
    l=[]
    for i in a:
        l.append({'id':i.id,'date':i.date,'attendence':i.attendence})

    return JsonResponse({'task': 'ok', 'data': l})


from django.http import JsonResponse


def student_view_notification(request):
    lid = request.POST['lid']

    try:
        student = student_table.objects.get(LOGIN=lid)
        student_stop = student.STOP.BUSROUTE_id
        staff = bussstaff_table.objects.get(BUSROUTE=student_stop)
        notification = busnotification.objects.filter(BUSSROUTENUMBER=staff.BUSROUTE_id).order_by('-id')
        a = notification_table.objects.filter(type="to students").order_by('-id')
        l = []
        c = []
        for i in a:
            l.append({
                'id': i.id,
                'date': i.date,
                'notification': i.notification,
                'type': i.type,
                'condition': 'admin'  # Condition for admin notifications
            })
        for i in notification:
            c.append({
                'id': i.id,
                'date': i.date,
                'notification': i.notification,
                'condition': 'staff'  # Condition for staff notifications
            })
        combined_notifications = l + c
        return JsonResponse({
            'status': 'ok',
            'data': combined_notifications
        })

    except student_table.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Student not found'
        })
    except bussstaff_table.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Staff not found for this bus route'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })


# def student_view_busnotification(request):
#     lid = request.POST['lid']
#     a = busnotification.objects.filter(STUDENT__LOGIN_id=lid)
#     l = []
#     for i in a:
#         l.append({'id':i.id,'date':i.date,'notification':i.notification,})
#     return JsonResponse({'task': 'ok', 'data':l})

def update_student(request):
     lid = request.POST['lid']
     name = request.POST['name']
     email = request.POST['email']
     phone = request.POST['phone']
     photo = request.POST['photo']
     admissions = request.POST['admissions']
     batch = request.POST['batch']
     departmentl = request.POST['department']
     address = request.POST['address']
     BUSROUTE = request.POST['BUSROUTE']

     b = student_table.objects.get(LOGIN_id=lid)
     b.name = name
     b.email = email
     b.phone = phone
     b.photo = photo
     b.address = address
     b.admissions = admissions
     b.batch = batch
     b.departmentl = departmentl
     b.BUSROUTE = busroute_table.objects.get(BUSROUTE=BUSROUTE)
     b.save()
     return JsonResponse({'task': 'ok'})

def student_send_complaint(request):
    print(request.POST,"hhhhhhhh")
    complaint = request.POST['complaint']
    lid = request.POST['lid']
    b = complaint_table()
    b.complaint = complaint
    b.LOGIN = login_table.objects.get(id=lid)
    b.type="student"
    b.save()
    return JsonResponse({'task': 'ok'})

def student_view_reply(request):
    lid = request.POST['lid']
    a = complaint_table.objects.filter(LOGIN_id=lid)
    l = []
    for i in a:
        l.append({'id': i.id, 'date': i.date,'complaint': i.complaint, 'reply': i.reply, })
    return JsonResponse({'task': 'ok', 'data':l})


def student_view_payment(request):
    lid = request.POST['lid']
    a = payment_table.objects.filter(STUDENT=lid)
    l = []
    for i in a:
        l.append({'id': i.id, 'date': i.date, 'amount': i.amount, })
    return JsonResponse({'task': 'ok', 'data': l})
def student_add_payment(request):
    lid = request.POST['lid']
    a= student_table.objects.get(LOGIN_id=lid)
    fee=stop_table.objects.get(id=a.STOP.id)
    return JsonResponse({'task': 'ok', 'fee': fee.fee})
def sendpayment(request):
    lid=request.POST["lid"]
    amt=request.POST["amt"]
    print(lid,amt)
    # rout=request.POST["routid"]
    a = student_table.objects.get(LOGIN_id=lid)
    p=balance_table.objects.filter(STUDENT_id=lid)
    if p.exists():
        pl=balance_table.objects.get(STUDENT_id=lid)
        if int(pl.balance)<=3:

            ob=payment_table()
            samt=a.STOP.fee
            tc=int(amt)//samt
            ob.STUDENT_id=lid
            ob.BUSSSTAFF_id=a.STOP.BUSROUTE.id
            ob.date=datetime.now().date()
            ob.amount=amt
            ob.save()
            obp=balance_table.objects.filter(STUDENT__id=lid)
            if len(obp)==0:
                obp=balance_table()
                obp.STUDENT_id=lid
                obp.balance=tc
                obp.date=datetime.today()
                obp.save()

            else:
                obp=obp[0]
                obp.balance += tc
                obp.date = datetime.today()
                obp.save()

            return JsonResponse({'task': 'ok'})
        else:
            return JsonResponse({'task': 'notok'})
    else:
        ob = payment_table()
        samt = a.STOP.fee
        tc = int(amt) // samt
        ob.STUDENT_id = lid
        ob.BUSSSTAFF_id = a.STOP.BUSROUTE.id
        ob.date = datetime.now().date()
        ob.amount = amt
        ob.save()
        obp = balance_table.objects.filter(STUDENT__id=lid)
        if len(obp) == 0:
            obp = balance_table()
            obp.STUDENT_id = lid
            obp.balance = tc
            obp.date = datetime.today()
            obp.save()

        else:
            obp = obp[0]
            obp.balance += tc
            obp.date = datetime.today()
            obp.save()

        return JsonResponse({'task':'ok'})









def staff_view_reply(request):
    lid = request.POST['lid']
    a = complaint_table.objects.filter(LOGIN_id=lid)
    l = []
    for i in a:
        l.append({'id': i.id, 'date': i.date, 'reply': i.reply, })
    return JsonResponse({'task': 'ok', 'data':l})

def staff_send_complaint(request):
    print(request.POST, "hhhhhhhh")
    complaint = request.POST['complaint']
    lid = request.POST['lid']
    b = complaint_table()
    b.complaint = complaint
    b.LOGIN = login_table.objects.get(id=lid)
    b.type = "staff"
    b.reply = "pending"
    b.save()
    return JsonResponse({'task': 'ok'})




def staff_send_notification(request):
    print(request.POST, "hhhhhhhh")
    notification = request.POST['notification']
    lid = request.POST['lid']
    ob=bussstaff_table.objects.get(login_id=lid)
    b = busnotification()
    b.notification = notification
    b.date=datetime.now()
    b.BUSSROUTENUMBER_id=ob.BUSROUTE.id
    b.save()
    return JsonResponse({'task': 'ok'})


def stud_send_complaint(request):
    print(request.POST, "hhhhhhhh")
    complaint = request.POST['complaint']
    lid = request.POST['lid']
    b = complaint_table()
    b.complaint = complaint
    b.LOGIN = login_table.objects.get(id=lid)
    b.type = "student"
    b.reply = "pending"
    b.save()
    return JsonResponse({'task': 'ok'})

def staff_view_complaints(request):
    lid = request.POST['lid']
    print(lid,"-------------------")
    a = complaint_table.objects.filter(LOGIN_id=lid).order_by('-id')
    l = []
    for i in a:
        l.append({'id': i.id, 'date': i.date, 'complaint': i.complaint,'reply':i.reply })

    print(l)

    return JsonResponse({'status': 'ok', 'data': l})



def stud_view_complaints(request):
    lid = request.POST['lid']
    print(lid,"-------------------")
    a = complaint_table.objects.filter(LOGIN_id=lid).order_by('-id')
    l = []
    for i in a:
        l.append({'id': i.id, 'date': i.date, 'complaint': i.complaint,'reply':i.reply })

    print(l)

    return JsonResponse({'status': 'ok', 'data': l})


def staff_view_notification(request):

    a = notification_table.objects.filter(type="to staff")
    l = []
    for i in a:
        l.append({'id':i.id,'date':i.date,'notification':i.notification,'type':i.type,})
    return JsonResponse({'task': 'ok', "data": l})

def staff_view_busnotification(request):
    lid = request.POST['lid']
    a = busnotification.objects.filter(STAFF__LOGIN_id=lid)
    l = []
    for i in a:
        l.append({'id':i.id,'date':i.date,'notification':i.notification,})
    return JsonResponse({'task': 'ok', 'data':l})


# def staff_send_notification(request):
#     notification = request.POST['notification']
#     date= request.POST['date']
#     type=request.POST['type']
#     return JsonResponse({'task': 'ok', 'data':l})


from django.shortcuts import render, get_object_or_404
# from .models import student_table, busroute_table, location_table
#
# def stud_view_map(request):
#     lid = request.POST.get('lid')
#
#     student = get_object_or_404(student_table, LOGIN_id=lid)
#
#     bus_route = student.STOP.BUSROUTE
#
#     locations = location_table.objects.filter(BUSSSTAFF=bus_route).last()
#
#
#     return JsonResponse({'status':'ok','latitude':str(locations.latitude),'longitude':str(locations.longitude),'BUSSSTAFF':locations.BUSSSTAFF.busnum})



def stud_view_map(request):
    lid = request.POST.get('lid')

    student = get_object_or_404(student_table, LOGIN_id=lid)

    bus_route = student.STOP.BUSROUTE

    locations = location_table.objects.filter(BUSSSTAFF=bus_route).last()

    if not locations:
        return JsonResponse({'status': 'error', 'message': 'No location data available for the bus route'})

    # Return the JSON response with location details
    return JsonResponse({
        'status': 'ok',
        'latitude': str(locations.latitude),
        'longitude': str(locations.longitude),
        'BUSSSTAFF': locations.BUSSSTAFF.busnum
    })


def android_view_bus_route(request):
    l=[]
    a=busroute_table.objects.all()
    for i in a:
        l.append({'id':i.id,'from1':i.from1,'to':i.to})
    print("================================")
    print("================================")
    print("================================")
    print(l)
    return JsonResponse({'status': 'ok','data':l})


def android_register(request):
    name = request.POST["name"]
    address = request.POST["address"]
    email = request.POST["email"]
    phone = request.POST["phone"]
    busroute = request.POST["stopid"]
    department = request.POST["department"]
    batch = request.POST["batch"]
    admission = request.POST["admission"]
    photo = request.POST["photo"]
    username = request.POST["username"]
    password = request.POST["password"]

    import datetime
    import base64
    date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    a = base64.b64decode(photo)
    fh = open("C:\\Users\\ALTHAF\\PycharmProjects\\digitalbuspasssystem\\media\\" + date + ".jpg", "wb")
    path =  date + ".jpg"
    fh.write(a)
    fh.close()


    a=login_table()
    a.username=username
    a.password=password
    a.type='pending'
    a.save()

    # fn = FileSystemStorage()
    # fs = fn.save(photo.name, photo)

    ob = student_table()
    ob.name = name
    ob.LOGIN = a
    ob.address = address
    ob.email = email
    ob.phone = phone
    ob.photo = path
    ob.STOP =stop_table.objects.get(id=busroute)
    ob.department = department
    ob.batch = batch
    ob.admissions = admission



    # Generate the student's details string for the QR code
    student_details = f"""
        Id: {ob.id}
        Name: {ob.name}
        Email: {ob.email}
        Phone: {ob.phone}
        Admissions: {ob.admissions}
        Batch: {ob.batch}
        Department: {ob.department}
        Address: {ob.address}
        """

    # Create a QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Higher error correction for embedded images
        box_size=10,
        border=4,
    )
    qr.add_data(student_details)
    qr.make(fit=True)

    # Convert QR code to an image
    img_qr = qr.make_image(fill='black', back_color='white').convert('RGB')

    # photo_path = os.path.join(settings.MEDIA_ROOT, ob.photo.name)
    # student_photo = Image.open(photo_path)

      # Example size, adjust as necessary


    qr_filename = f"qr_{ob.id}.png"
    qr_path = os.path.join(settings.MEDIA_ROOT, qr_filename)
    img_qr.save(qr_path)

    # Store the QR code file path in the student_table model
    ob.QrCode = f"{settings.MEDIA_URL}{qr_filename}"






    ob.save()
    return JsonResponse({'status': 'ok'})




from django.shortcuts import render
from django.http import JsonResponse
from .models import bussstaff_table, student_table, stop_table

def view_students(request, ):
    staff_id=request.POST['lid']

    staff = bussstaff_table.objects.get(login_id=staff_id)
    busroute = staff.BUSROUTE

    stops = stop_table.objects.filter(BUSROUTE=busroute)

    students = student_table.objects.filter(STOP__in=stops)

    student_data = [
        {
            "name": student.name,
           "batch": student.batch,
            "department": student.department,
            "stop": student.STOP.stop,
        }
        for student in students
    ]
    print(student_data)

    return JsonResponse({"status": "ok", "data": student_data})




def android_view_bus_stop(request):
    l=[]
    rid=request.POST['rid']
    a=stop_table.objects.filter(BUSROUTE__id=rid)
    for i in a:
        l.append({'id':i.id,'stop':i.stop})
    print("================================")
    print("================================")
    print("================================")
    print(l)
    return JsonResponse({'status': 'ok','data':l})




# def staff_mark_attendance(request):
#     print(request.POST)
#     lid=request.POST['lid']
#     print(lid)
#     print(request.POST['id'])
#     print(request.POST['id'].split("d: "))
#     id=request.POST['id'].split("d: ")[1].split("\n")[0]
#     print(id,"======================================")
#     print(id,"======================================")
#     print(id,"======================================")
#     print(id,"======================================")
#
#
#     s=student_table.objects.get(id=id)
#     log=s.LOGIN.id
#     print(log,'loggggg')
#     print(s,'sssssss')
#     kk=payment_table.objects.filter(STUDENT__id=log)
#     print(kk)
#     if len(kk) == 0:
#         return JsonResponse({'status': 'no'})
#     else:
#         ob=balance_table.objects.get(STUDENT__id=log)
#         print(ob)
#         if ob.balance==0:
#             return JsonResponse({'status': 'no'})
#
#         a = attendence_table()
#         a.BUSSSTAFF = bussstaff_table.objects.get(LOGIN_id=lid)
#         a.STUDENT = student_table.objects.get(id=id)
#         a.attendence = 1
#         a.date = datetime.now().today()
#         a.save()
#         ob.balance-=1
#         ob.save()
#
#         return JsonResponse({'status': 'ok'})







from datetime import datetime
from django.http import JsonResponse


from datetime import datetime, timedelta

from datetime import datetime, timedelta
import time

def staff_mark_attendance(request):
    print(request.POST)

    # Fetch the bus staff's login ID
    lid = request.POST['lid']
    print(f"Bus staff login ID: {lid}")

    # Fetch and process the student ID
    id_field = request.POST['id']
    print(f"Raw student ID: {id_field}")

    if "d: " not in id_field:
        return JsonResponse({'status': 'error', 'message': 'Invalid ID format'})

    try:
        student_id = id_field.split("d: ")[1].split("\n")[0]
    except IndexError:
        return JsonResponse({'status': 'error', 'message': 'Invalid ID format'})

    print(f"Processed student ID: {student_id}")

    # Validate student existence
    try:
        student_ob = student_table.objects.get(id=student_id)
    except student_table.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Student not found'})

    print(f"Student login: {student_ob.LOGIN}")

    # Check for payment record
    payments = payment_table.objects.filter(STUDENT=student_ob.LOGIN.id)
    print(f"Payments: {payments}")
    if not payments.exists():
        return JsonResponse({'status': 'no', 'message': 'No payment records found'})

    # Check the balance
    print("balance_entry")
    try:
        balance_entry = balance_table.objects.get(STUDENT__id=student_ob.LOGIN.id)
    except balance_table.DoesNotExist:
        return JsonResponse({'status': 'no', 'message': 'No balance record found'})

    print("balance_entry.balance", balance_entry.balance)
    if balance_entry.balance <= 0:
        return JsonResponse({'status': 'no', 'message': 'Insufficient balance'})

    # Check previous attendance record
    attendance_entryy = attendence_table.objects.filter(STUDENT_id=student_ob.LOGIN).order_by('-date', '-time')
    if attendance_entryy.exists():
        last_attendance = attendance_entryy.first()

        # Check if last_attendance.date and last_attendance.time are not None
        if last_attendance.date and last_attendance.time:
            try:
                # Convert last_attendance.time (CharField) to a datetime.time object
                time_str = last_attendance.time
                last_attendance_time = datetime.combine(last_attendance.date,
                                                        datetime.strptime(time_str, '%H:%M:%S').time())
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Error converting time: {e}'})

            current_time = datetime.now()

            # Check if the time difference is greater than 2 hours
            time_difference = current_time - last_attendance_time
            if time_difference <= timedelta(hours=2):
                return JsonResponse({'status': 'error', 'message': 'Attendance already marked within the last 2 hours'})

        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid date or time in last attendance record'})

    # Mark new attendance
    attendance_entry = attendence_table()
    attendance_entry.BUSSSTAFF = bussstaff_table.objects.get(login_id=lid)
    attendance_entry.STUDENT = student_ob.LOGIN
    attendance_entry.attendence = "1"
    attendance_entry.date = datetime.now().date()
    attendance_entry.time = datetime.now().strftime('%H:%M:%S')  # Save current time as a string
    attendance_entry.save()

    # Deduct balance
    balance_entry.balance -= 1
    balance_entry.save()

    return JsonResponse({'status': 'ok'})


# def staff_mark_attendance(request):
#
#     print(request.POST)
#
#     # Fetch the bus staff's login ID
#     lid = request.POST['lid']
#     print(f"Bus staff login ID: {lid}")
#
#     # Fetch and process the student ID
#     id_field = request.POST['id']
#     print(f"Raw student ID: {id_field}")
#
#     if "d: " not in id_field:
#         return JsonResponse({'status': 'error', 'message': 'Invalid ID format'})
#
#     try:
#         student_id = id_field.split("d: ")[1].split("\n")[0]
#     except IndexError:
#         return JsonResponse({'status': 'error', 'message': 'Invalid ID format'})
#
#     print(f"Processed student ID: {student_id}")
#
#     # Validate student existence
#     student_ob=student_table.objects.get(id=student_id)
#
#     print(f"Student login: {student_ob.LOGIN}")
#
#     # Check for payment record
#     payments = payment_table.objects.filter(STUDENT=student_ob.LOGIN.id)
#     print(f"Payments: {payments}")
#     if not payments.exists():
#         return JsonResponse({'status': 'no'})
#
#     # Check the balance
#     print("balance_entry")
#     try:
#         balance_entry = balance_table.objects.get(STUDENT__id=student_ob.LOGIN.id)
#     except balance_table.DoesNotExist:
#         return JsonResponse({'status': 'no', 'message': 'No balance record found'})
#     print("balance_entry.balance",balance_entry.balance)
#     if balance_entry.balance <= 0:
#         return JsonResponse({'status': 'no', 'message': 'Insufficient balance'})
#
#     # Mark attendance
#     attendance_entryy = attendence_table.objects.filter(STUDENT_id=student_ob.LOGIN)
#     if attendance_entryy.exists():
#         p=attendence_table.objects.get(STUDENT_id=student_ob.LOGIN)
#         time=p.time
#         if time>
#
#     else:
#         attendance_entry=attendence_table()
#         attendance_entry.BUSSSTAFF = bussstaff_table.objects.get(login_id=lid)
#         attendance_entry.STUDENT = student_ob.LOGIN
#         attendance_entry.attendence = "1"
#         attendance_entry.date = datetime.now().date()
#         attendance_entry.time=datetime.now().time()
#         attendance_entry.save()
#
#         # Deduct balance
#         balance_entry.balance -= 1
#         balance_entry.save()
#
#         return JsonResponse({'status': 'ok'})





from django.http import JsonResponse
from datetime import datetime
from myapp.models import bussstaff_table, student_table, attendence_table

# def staff_mark_attendance(request):
#
#     lid = request.POST.get('lid')
#     student_id = request.POST.get('id').split("Id: ")[1].split('\n')[0]
#
#     print(f"Received student_id: {student_id}, lid: {lid}")  # Debugging line
#
#
#     staff = bussstaff_table.objects.get(login_id=lid)
#     student = login_table.objects.get(id=lid)
#
#     # Create the attendance entry
#     attendance = attendence_table(
#         BUSSSTAFF=staff,
#         STUDENT=student,
#         attendence='1',  # '1' indicates present
#         date=datetime.now().today()
#     )
#     attendance.save()
#
#     return JsonResponse({'status': 'ok'}, status=200)

def view_bus_stop(request):
    l=[]
    rid=request.GET['rid']
    a=stop_table.objects.filter(BUSROUTE__id=rid)
    for i in a:
        l.append({'id':i.id,'stop':i.stop})
    print("================================")
    print("================================")
    print("================================")
    print(l)
    return JsonResponse({'status': 'ok','data':l})



def displaybalance(request):
    lid = request.POST['lid']
    # lid=request.POST["lid"]
    ob=balance_table.objects.get(STUDENT_id=lid)
    ob1 = student_table.objects.get(LOGIN_id=lid)
    obs=ob1.STOP.fee
    tp=int(ob.balance)*int(obs)
    return  JsonResponse({'status':'ok','balance':ob.balance,"tp":tp})




def staff_view_staffnotification(request):
    lid = request.POST['lid']
    print(lid,"-------------------")
    kk = bussstaff_table.objects.get(login__id=lid)
    print(lid, "-------------------")
    a = busnotification.objects.filter(BUSSROUTENUMBER__id=kk.BUSROUTE.id).order_by('-id')
    l = []
    for i in a:
        l.append({'id': i.id, 'date': i.date, 'notification': i.notification})

    print(l)

    return JsonResponse({'status': 'ok', 'data': l})




# def studwnt_view_attendance(request, student_id):
#     lid = request.POST['lid']
#     print(lid,"-------------------")
#     a = attendence_table.objects.filter(STUDENT_id=student_id).order_by('id')
#     l = []
#     for record in a:
#         l.append({
#             "date": record.date.strftime('%Y-%m-%d'),
#             "attendence": record.attendence,
#         })
#
#     print(l)
#
#     return JsonResponse({'status': 'ok', 'data': l})




from datetime import timedelta, date
from django.db.models import Q

def student_view_attendance(request):
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    student_id = request.POST['student_id']
    ob=attendence_table.objects.filter(STUDENT__id=student_id)
    datelist=[]
    res=[]
    for i in ob:
        if str(i.date) not in datelist:
            datelist.append(str(i.date))
            res.append({"date":str(i.date),"att":1})
        else:
            ind=datelist.index(str(i.date))
            res[ind]['att']+=1
    print(res)
    # for i in res:

    # return JsonResponse({'status': 'ok', 'data': res})
    try:
        print(student_id)
        # Get the range of dates (e.g., last 30 days)
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        print(start_date)
        print(end_date)
        # Fetch all attendance records for the student within the date range
        attendance_records = attendence_table.objects.filter(
            STUDENT_id=student_id,
            date__range=(start_date, end_date)
        ).order_by('date', 'time')
        print(attendance_records,len(attendance_records))
        # Group attendance by date and time slot (AM or PM)
        attendance_by_date = {}

        for record in attendance_records:
            date_str = record.date.strftime('%Y-%m-%d')  # Convert date to string

            # Initialize a date record if not already present
            if date_str not in attendance_by_date:
                attendance_by_date[date_str] = {"am": False, "pm": False}

            # Mark AM or PM as present based on the `time` field
            obd=attendence_table.objects.filter(STUDENT_id=student_id,date=date_str)
            if len(obd)>0:
                attendance_by_date[date_str]["am"] = True
            if len(obd) > 1:
                attendance_by_date[date_str]["pm"] = True

        # Prepare the final attendance response
        final_attendance = []
        for single_date in (start_date + timedelta(n) for n in range((end_date - start_date).days + 1)):
            date_str = single_date.strftime('%Y-%m-%d')
            if date_str in attendance_by_date:
                final_attendance.append({
                    "date": date_str,
                    "amStatus": "Present" if attendance_by_date[date_str]["am"] else "Absent",
                    "pmStatus": "Present" if attendance_by_date[date_str]["pm"] else "Absent",
                })
        print(final_attendance)
        return JsonResponse({'status': 'ok', 'data': final_attendance})

    except Exception as e:
        print(e)
        return JsonResponse({'status': 'error', 'message': str(e)})





# def updatelocation(request):
#     print(request.POST)
#     lid=request.POST['lid']
#     ob=bussstaff_table.objects.filter(login__id=lid)
#     if len(ob)>0:
#         lat=request.POST['lat']
#         lon=request.POST['lon']
#         id=ob[0].BUSROUTE.id
#         ob=location_table.objects.get(BUSSSTAFF__id=id)
#         ob.latitude = lat
#         ob.longitude = lon
#         ob.save()
#         return JsonResponse({'task': 'ok' })
#
#     else:
#         ob=notistatus_table.objects.filter(STUDENT__id=lid)
#         ids=[]
#         for i in ob:
#             ids.append(i.NOTIFICATION.id)
#         ob=notification_table.objects.exclude(id__in=ids)
#         if len(ob)==0:
#             return JsonResponse({'task': 'False'})
#         else:
#             for i in ob:
#                 obn=notistatus_table()
#                 obn.NOTIFICATION=i
#                 obn.STUDENT=login_table.objects.get(id=lid)
#                 obn.save()
#             return JsonResponse({'task': 'True',"msg":ob[0].notification})



def updatelocation(request):
    print(request.POST)
    lid = request.POST['lid']
    ob = bussstaff_table.objects.filter(login__id=lid)
    if len(ob) > 0:
        print(request.POST,"kkkkkkkkkkkkkkkkkk")
        # Update bus staff location
        lat = request.POST['lat']
        lon = request.POST['lon']
        id = ob[0].BUSROUTE.id
        p = location_table.objects.filter(BUSSSTAFF__id=id)
        if p.exists():
            ob = location_table.objects.get(BUSSSTAFF__id=id)
            ob.latitude = lat
            ob.longitude = lon
            ob.save()
            return JsonResponse({'task': 'ok'})
        else:
            ob = location_table()
            ob.BUSSSTAFF_id=id
            ob.latitude = lat
            ob.longitude = lon
            ob.save()
            return JsonResponse({'task': 'ok'})

    else:
        # Handle notifications for students
        ob = notistatus_table.objects.filter(STUDENT__id=lid)
        ids = []
        for i in ob:
            ids.append(i.NOTIFICATION.id)

        # Get student details
        student = student_table.objects.filter(LOGIN__id=lid).first()
        if not student:
            return JsonResponse({'task': 'False', 'msg': 'Student not found'})

        # Process student-specific notifications
        ob = notification_table.objects.exclude(id__in=ids)
        if len(ob) == 0:
            ob = busnotistatus_table.objects.filter(STUDENT__id=lid)
            ids = []
            for i in ob:
                ids.append(i.NOTIFICATION.id)
            # Check for bus notifications for the student's bus route
            bus_route = student.STOP.BUSROUTE
            bus_notifications = busnotification.objects.filter(BUSSROUTENUMBER=bus_route).exclude(id__in=ids)


            if len(bus_notifications) == 0:
                return JsonResponse({'task': 'False'})
            else:
                for notification in bus_notifications:
                    # Add bus notifications to busnotistatus_table
                    bus_status = busnotistatus_table()
                    bus_status.NOTIFICATION = notification
                    bus_status.STUDENT = login_table.objects.get(id=lid)
                    bus_status.save()
                return JsonResponse({'task': 'True', 'msg': bus_notifications[0].notification})
        else:
            # Add general notifications to notistatus_table
            for i in ob:
                obn = notistatus_table()
                obn.NOTIFICATION = i
                obn.STUDENT = login_table.objects.get(id=lid)
                obn.save()
            return JsonResponse({'task': 'True', "msg": ob[0].notification.notification})


from datetime import datetime, timedelta
from django.http import JsonResponse
from .models import attendence_table

def send_refund_request(request):
    lid = request.POST['lid']
    current_time = datetime.now()
    current_date = current_time.date()

    time_threshold = current_time - timedelta(minutes=30)

    attendance_records = attendence_table.objects.filter(STUDENT__id=lid,date=current_date,time__gte=time_threshold.strftime("%H:%M:%S"),)
    print(attendance_records)
    if len(attendance_records) > 0:
        ob = request_table.objects.filter(ATTENDANCE__id=attendance_records[0].id)
        print(ob)
        if len(ob) == 0:
            ob = request_table()
            ob.status = 'pending'
            ob.ATTENDANCE = attendance_records[0]
            ob.date = datetime.today()
            ob.save()
            print("=========================================")
            print("=========================================")
            print("=========================================")
            print("=========================================")
            return JsonResponse({"task": "ok"})
        else:

            return JsonResponse({"task": "not send"})
    return JsonResponse({"task": "na"})


def accept_refund_request(request):
    print("Refund Request ID:", request.POST)
    rid = request.POST['rid']

    ob = request_table.objects.get(id=rid)

    ob.status = 'accepted'
    ob.save()

    uid = ob.ATTENDANCE.STUDENT.id
    oba = ob.ATTENDANCE
    oba.delete()

    obb = balance_table.objects.get(STUDENT__id=uid)
    obb.balance += 1
    obb.save()

    return JsonResponse({"task": "ok"})
def reject_refund_request(request):
    rid=request.POST['rid']

    ob=request_table.objects.get(id=rid)
    ob.status="rejected"
    ob.save()
    return JsonResponse({"task": "ok"})



def view_refund_request(request):
    # Assuming a hardcoded login ID for now
    lid = request.POST['lid']

    try:
        # Get the bus staff's assigned route
        obs = bussstaff_table.objects.get(login_id=lid)
        obb = obs.BUSROUTE.id

        # Get all students associated with the bus route
        ob = student_table.objects.filter(STOP__BUSROUTE__id=obb)

        # Extract student login IDs
        lids = [student.LOGIN.id for student in ob]

        # Filter refund requests with 'pending' status for the students
        refund_requests = request_table.objects.filter(
            ATTENDANCE__STUDENT__id__in=lids, status='pending'
        )

        data = []

        for req in refund_requests:
            # Get student details associated with the request
            student = student_table.objects.get(LOGIN__id=req.ATTENDANCE.STUDENT.id)
            r = {
                "id": req.id,
                "name": student.name,
                "date": req.ATTENDANCE.date
            }
            data.append(r)

        return JsonResponse({"task": "ok", "data": data})

    except Exception as e:
        return JsonResponse({"task": "error", "message": str(e)})

from django.db.models import Prefetch

from django.db.models import Prefetch

def VIEWpaymentall(request):

    payments = payment_table.objects.select_related(
        'STUDENT'  # Access login_table from payment_table
    ).order_by('-id')


    students = student_table.objects.select_related('LOGIN')
    student_map = {student.LOGIN.id: student for student in students}


    for payment in payments:
        payment.student_details = student_map.get(payment.STUDENT.id)

    return render(request, 'admin/ADMIN_VIEW_PAYMENT_ALL.html', {"payments": payments})






def forgot_password(request):
    print(request.POST)
    try:
        username = request.POST['username']
        s = login_table.objects.get(username=username)

        # If user is not found or doesn't exist, return an invalid response
        if s is None:
            return JsonResponse({"status": "Invalid username"})
        else:
            # Fetch the Organization associated with the Login object
            try:
                organization = student_table.objects.get(LOGIN=s)
                email_address = organization.email  # Assuming email is in Organization model
            except student_table.DoesNotExist:
                return JsonResponse({"status": "Email not available in Organization"})

            if not email_address:
                return JsonResponse({"status": "Email not available"})

            # Create the email content
            subject = 'DIGI-PASS password reset'
            message = f"Your password: {s.password}"
            from_email = 'saifullacm2003@gmail.com'

            try:
                # Send the email with the password to the user's email address
                send_mail(subject, message, from_email, [email_address])
                return JsonResponse({"status": "ok"})
            except Exception as e:
                print(f"Error sending email: {str(e)}")
                return JsonResponse({"status": "Email sending failed"})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"status": "Error occurred"})



