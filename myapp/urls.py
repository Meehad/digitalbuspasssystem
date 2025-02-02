from django.urls import path

from myapp import views

urlpatterns=[

    path('',views.login,name='login'),
    path('login_post',views.login_post,name='login_post'),

    path('BUSROUTE',views.BUSROUTE,name='BUSROUTE'),
    path('BUSROUTE_post',views.BUSROUTE_post,name='BUSROUTE_post'),
    path('DELETE_BUSROUTE/<id>',views.DELETE_BUSROUTE,name='DELETE_BUSROUTE'),
    path('EDIT_BUSROUTE/<id>',views.EDIT_BUSROUTE,name='EDIT_BUSROUTE'),
    path('EDIT_BUSROUTE_post', views.EDIT_BUSROUTE_post, name='EDIT_BUSROUTE_post'),

    path('ADDBUSSTAFF', views.ADDBUSSTAFF, name='ADDBUSSTAFF'),
    path('ADDBUSSTAFF_post', views.ADDBUSSTAFF_post, name='ADDBUSSTAFF_post'),
    path('EDITBUSSTAFF/<id>', views.EDITBUSSTAFF, name='EDITBUSSTAFF'),
    path('EDITBUSSTAFF_post', views.EDITBUSSTAFF_post, name='EDITBUSSTAFF_post'),
    path('DELETEBUSSTAFF/<id>', views.DELETEBUSSTAFF, name='DELETEBUSSTAFF'),



    path('VERIFYSTUDENT', views.VERIFYSTUDENT, name='VERIFYSTUDENT'),
    path('VERIFYSTUDENT_post', views.VERIFYSTUDENT_post, name='VERIFYSTUDENT_post'),

    path('MANAGEBUSROUTE', views.MANAGEBUSROUTE, name='MANAGEBUSROUTE'),
    path('MANAGEBUSROUTE_post', views.MANAGEBUSROUTE_post, name='MANAGEBUSROUTE_post'),

    path('BUSSTAFF',views.BUSSTAFF,name='BUSSTAFF'),
    path('BUSSTAFF_post',views.BUSSTAFF_post,name='BUSSTAFF_post'),


    path('MANAGEBUSSTOP',views.MANAGEBUSSTOP,name='MANAGEBUSSTOP'),
    path('MANAGEBUSSTOP_post',views.MANAGEBUSSTOP_post,name='MANAGEBUSSTOP_post'),
    path('DELETE_BUSSTOP/<id>',views.DELETE_BUSSTOP,name='DELETE_BUSSTOP'),
    path('EDITbusstop/<id>',views.EDITbusstop,name='EDITbusstop'),
    path('editbusstop_post',views.editbusstop_post,name='editbusstop_post'),
    path('addbusstop',views.addbusstop,name='addbusstop'),
    path('addbusstop_post',views.addbusstop_post,name='addbusstop_post'),

    path('BLOCKSTUDENT',views.BLOCKSTUDENT,name='BLOCKSTUDENT'),
    path('BLOCKSTUDENT_post/<id>',views.BLOCKSTUDENT_post,name='BLOCKSTUDENT_post'),
    path('UNBLOCK/<id>',views.UNBLOCK,name='UNBLOCK'),

    path('add_payment',views.add_payment,name='add_payment'),
    path('VIEWPAYMENT/<id>',views.VIEWPAYMENT,name='VIEWPAYMENT'),
    path('ACCEPT/<id>', views.ACCEPT, name='ACCEPT'),
    path('REJECT/<id>', views.REJECT, name='REJECT'),

    path('SENDNOTIFICATION',views.SENDNOTIFICATION,name='SENDNOTIFICATION'),
    path('SENDNOTIFICATION_post',views.SENDNOTIFICATION_POST,name='SENDNOTIFICATION_post'),

    path('VIEWCOMPLAINTS',views.VIEWCOMPLAINTS,name='VIEWCOMPLAINTS'),
    path('VIEWCOMPLAINTS_post',views.VIEWCOMPLAINTS_post,name='VIEWCOMPLAINTS_post'),


    path('REPLY/<id>',views.REPLY,name='REPLY'),
    path('REPLY_post',views.REPLY_post,name='REPLY_post'),

    path('HOME',views.HOME,name='HOME'),
    path('VIEWHOME',views.VIEWHOME,name='VIEWHOME'),

    path('NOTIFICATIONTOBUS',views.NOTIFICATIONTOBUS,name='NOTIFICATIONTOBUS'),
    path('NOTIFICATIONTOBUS_post',views.NOTIFICATIONTOBUS_post,name='NOTIFICATIONTOBUS_post'),

    path('MANAGESTUDENT',views.MANAGESTUDENT,name='MANAGESTUDENT'),
    path('MANAGESTUDENT_post',views.MANAGESTUDENT_post,name='MANAGESTUDENT_post'),
    path('ADDSTUDENT',views.ADDSTUDENT,name='ADDSTUDENT'),
    path('ADDSTUDENT_post',views.ADDSTUDENT_post,name='ADDSTUDENT_post'),
    path('EDIT_STUDENT/<id>',views.EDIT_STUDENT,name='EDIT_STUDENT'),
    path('EDIT_STUDENT_post',views.EDIT_STUDENT_post,name='EDIT_STUDENT_post'),
    path('DELETESTUDENT/<id>',views.DELETESTUDENT,name='DELETESTUDENT'),
    path('BLOCKSTUDENT_search',views.BLOCKSTUDENT_search,name='BLOCKSTUDENT_search'),
    path('view_bus_stop',views.view_bus_stop,name='BLOCKSTUDENT_search'),
    path('VIEWpaymentall',views.VIEWpaymentall,name='VIEWpaymentall'),
    path('insert_payment',views.insert_payment,name='insert_payment'),



    path('LOGOUT',views.LOGOUT,name='LOGOUT'),



    #-------------------and

    path("android_login",views.android_login),
    path("student_view_notification",views.student_view_notification),
    path("student_send_complaint",views.student_send_complaint),
    path("student_view_profile",views.student_view_profile),
    path("student_view_qr",views.student_view_qr),
    path("stud_send_complaint",views.stud_send_complaint),
    path("stud_view_map",views.stud_view_map),
    path("student_add_payment",views.student_add_payment),
    path("student_view_payment",views.student_view_payment),
    path("sendpayment",views.sendpayment),
    path("android_view_bus_stop",views.android_view_bus_stop),
    path("displaybalance",views.displaybalance),
    path("student_view_attendance",views.student_view_attendance),
    path("updatelocation",views.updatelocation),
    path("student_view_reply",views.student_view_reply),
    path("stud_view_complaints",views.stud_view_complaints),
    path("forgot_password",views.forgot_password),
    # path("displayattendence",views.displayattendence),




#--------------------------staff
    path("staff_view_reply", views.staff_view_reply),
    path("staff_view_complaints", views.staff_view_complaints),
    path("staff_send_complaint", views.staff_send_complaint),



    path("android_view_bus_route", views.android_view_bus_route),
    path("android_register", views.android_register),
    path("view_students", views.view_students),
    path("staff_mark_attendance", views.staff_mark_attendance),
    path("staff_send_notification", views.staff_send_notification),
    path("staff_view_staffnotification", views.staff_view_staffnotification),
    path("send_refund_request", views.send_refund_request),
    path("staff_view_notification", views.staff_view_notification),
    path("view_refund_request", views.view_refund_request),
    path("accept_refund_request", views.accept_refund_request),
    path("reject_refund_request", views.reject_refund_request),
]