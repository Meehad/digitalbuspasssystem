from django.db import models

# Create your models here.

class login_table(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

class busroute_table(models.Model):
    from1=models.CharField(max_length=100)
    to=models.CharField(max_length=100)
    busnum=models.CharField(max_length=100)

class stop_table(models.Model):
    BUSROUTE=models.ForeignKey(busroute_table,on_delete=models.CASCADE)
    stop=models.CharField(max_length=100)
    latitude=models.CharField(max_length=100)
    longitude=models.CharField(max_length=100)
    fee=models.IntegerField()

class bussstaff_table(models.Model):
    login=models.ForeignKey(login_table,on_delete=models.CASCADE)
    BUSROUTE=models.ForeignKey(busroute_table,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    # proof=models.FileField()

class student_table(models.Model):
    LOGIN = models.ForeignKey(login_table, on_delete=models.CASCADE)
    STOP = models.ForeignKey(stop_table, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    photo = models.FileField()
    admissions = models.CharField(max_length=100)
    batch = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    QrCode = models.CharField(max_length=300)



class complaint_table(models.Model):
    LOGIN = models.ForeignKey(login_table, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=100)
    complaint = models.CharField(max_length=1000)
    reply= models.CharField(max_length=100)

class notification_table(models.Model):
    type = models.CharField(max_length=100)
    notification = models.CharField(max_length=1000)
    date = models.DateField()

class payment_table(models.Model):
    STUDENT = models.ForeignKey(login_table, on_delete=models.CASCADE)
    BUSSSTAFF = models.ForeignKey(busroute_table, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.BigIntegerField()

class attendence_table(models.Model):
    STUDENT = models.ForeignKey(login_table, on_delete=models.CASCADE)
    BUSSSTAFF = models.ForeignKey(bussstaff_table, on_delete=models.CASCADE)
    date = models.DateField()
    time=models.CharField(max_length=100)
    attendence=models.CharField(max_length=30)

class location_table(models.Model):
    BUSSSTAFF = models.ForeignKey(busroute_table, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

class busnotification(models.Model):
    BUSSROUTENUMBER = models.ForeignKey(busroute_table, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    notification = models.CharField(max_length=1000)

# class bussstop_table(models.Model):
#     date = models.IntegerField()
#     notification = models.CharField(max_length=1000)

class balance_table(models.Model):
       STUDENT = models.ForeignKey(login_table, on_delete=models.CASCADE)
       balance = models.BigIntegerField()
       date = models.DateField()


class notistatus_table(models.Model):
      STUDENT = models.ForeignKey(login_table, on_delete=models.CASCADE)
      NOTIFICATION=models.ForeignKey(notification_table, on_delete=models.CASCADE)


class busnotistatus_table(models.Model):
    STUDENT = models.ForeignKey(login_table, on_delete=models.CASCADE)
    NOTIFICATION = models.ForeignKey(busnotification, on_delete=models.CASCADE)





class request_table(models.Model):
       status = models.CharField(max_length=1000)
       ATTENDANCE = models.ForeignKey(attendence_table, on_delete=models.CASCADE)
       date=models.DateField()
