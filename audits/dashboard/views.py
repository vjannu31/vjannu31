from django.shortcuts import render, redirect
from .models import Audits, User, UserManager
from .serializers import AuditsSerializers

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse, HttpResponse

from django.db.models import Count, Sum
import pandas as pd
from django.db.models.functions import Lower, Substr, StrIndex
from django.db.models import Count, F, Value
from datetime import datetime
from django.db.models.functions import Extract


import pandas as pd
from django.shortcuts import render
# from django_chartjs.views import JSONResponseMixin
from pymongo import MongoClient
# Create your views here.
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDay

from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, LoginForm
from datetime import date


@csrf_exempt
def auditsapi(request, id=0):
    if request.method=="GET":
        department=Audits.objects.all()
        print(department)
        department_serializer=AuditsSerializers(department, many=True)
        return JsonResponse(department_serializer.data, safe=False)
    


def hourdate(request):
    start_date = request.GET.get('start_date')  # Get start_date from query parameters
    end_date = request.GET.get('end_date')

    time_interval = request.GET.get('interval')  # Assuming the interval is passed as a query parameter like '?interval=1'
    # try:
    #     time_interval = int(time_interval)
    # except (ValueError, TypeError):
    #     time_interval = 1  # If the interval parameter is not provided or invalid, default to 1 hour

    # # Calculate the start and end time based on the selected time interval
    # end_time1 = datetime(2023, 9,6)
    # start_time1 = end_time1 - timedelta(hours=time_interval)
    # print("&&&&&&&&&&",end_time1, start_time1)
    from datetime import date

    sd1 = date(2023,10,1)
    ed1 = date(2023,10,2)

    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        except ValueError:
            start_date = datetime.now().date()
    else:
        start_date = datetime.now().date()

    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            end_date = datetime.now().date()
    else:
        end_date = datetime.now().date()

    print(start_date, end_date, "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    # Calculate the time range for the selected dates and hours
    start_date = datetime.combine(start_date, datetime.min.time()) - timedelta(days=1)
    end_date = datetime.combine(end_date, datetime.min.time()) 
   

# Calculate the time range for the selected dates and hours
#     start_time = datetime.combine(start_date, datetime.min.time())
#     print(start_date, "start_time, $$$$$$$$$$$$$$$$$$$$$$$")
#     # end_time = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)
#     end_time = datetime(2023, 6,10)
    print(start_date, end_date, "$$$$$$$$$$$$$$$$$$$$$ 12345")


    if time_interval:
        try:
            time_interval = int(time_interval)
        except ValueError:
            time_interval = None

    if time_interval is not None:
        end_date = datetime(2023, 9,5)
        start_date = end_date - timedelta(hours=time_interval)
        # end_time += timedelta(hours=end_hour)


    filtered_data = Audits.objects.all()  # Start with all objects
    filtered_data = filtered_data.filter(date__range=[start_date, end_date])
    filtered_data_overall = filtered_data
    print(len(filtered_data))

    # application data
    filtered_data_app = filtered_data.values('appd_application_name').annotate(count=Count('timestamp')).order_by('appd_application_name')
    print("filtered_data_app")
    print(len(filtered_data))
     
    # houlry based data
    filtered_data_hourly = filtered_data.filter(date__range=[start_date, end_date])
    data_hourly_type = filtered_data_hourly.values('type').annotate(count=Count('timestamp')).order_by('type')
    print("*******************************************************")
    print("data_hourly_type")
    print(len(data_hourly_type))

    # severity data

    filtered_severity = filtered_data.filter(date__range=[start_date, end_date])
    filtered_severity_data = filtered_severity.values('severity').annotate(count=Count('timestamp')).order_by('severity')
    print("*******************************************************")
    print("filtered_severity_data")
    print(len(filtered_severity_data))

    labels1 = [dp.date for dp in filtered_data]
    values1 = [dp.appd_application_name for dp in filtered_data]
    # print(labels1,values1, "362")
    print("#################################################################")

    # Top five application
    top_five_filter = filtered_data.filter(date__range=[start_date, end_date])
    # top_fine_data = top_five_filter.values('appd_application_name').annotate(count=Count('_id')).order_by('type')
    print("************** Top five application*****************************************")
    top_five_data = top_five_filter.values('appd_application_name').annotate(count=Count('appd_application_name')).order_by('-count')[:10]
    print("top_five_data")
    print(len(top_five_data))

    print("************** bottom five application*****************************************")
    # Top five application
    bottom_five_filter = filtered_data.filter(date__range=[start_date, end_date])
    bottom_five_data = bottom_five_filter.values('appd_application_name').annotate(count=Count('appd_application_name')).order_by('count')[:10]
    print("bottom_five_data")
    print(len(bottom_five_data))

    print("************** application and type*****************************************")
    # Top five application
    bottom_five_filter = filtered_data.filter(date__range=[start_date, end_date])
    bottom_five_data = bottom_five_filter.values('appd_application_name').annotate(count=Count('appd_application_name')).order_by('count')[:10]
    print("bottom_five_data")

    print("**************  data point *****************************************")
    data_points_filter = filtered_data.filter(date__range=[start_date, end_date])
    data_audits = data_points_filter.values('type').annotate(type_count=Count('type'))
    
    print("224 data audits", data_audits)

    chart_type = "column"


    context = {
                'overall_data': filtered_data_overall,
                'data': filtered_data_app,
                'selected_hour':data_hourly_type,
                'severity_data': filtered_severity_data,
                'topfive': top_five_data,
                'bottomfive': bottom_five_data,
                # 'selected_date': date.strftime('%Y-%m-%d'),
                'start_d':start_date.strftime("%Y-%m-%d"),
                'end_d':end_date.strftime("%Y-%m-%d"),
                
                'data_points':data_audits,
                "chart_type": chart_type,

                }
                
    # return render(request, 'chartapp/filtered_data_copy.html', context)
    return render(request, 'chartapp/aaaaa.html', context)
    # return render(request, 'temp/examples/dashboard.html', context)
##################################################################################




#####################################################################################################################


def display_app(request):
    start_date = request.GET.get('start_date')  # Get start_date from query parameters
    end_date = request.GET.get('end_date')

    time_interval = request.GET.get('interval')  # Assuming the interval is passed as a query parameter like '?interval=1'
    # try:
    #     time_interval = int(time_interval)
    # except (ValueError, TypeError):
    #     time_interval = 1  # If the interval parameter is not provided or invalid, default to 1 hour

    # # Calculate the start and end time based on the selected time interval
    # end_time1 = datetime(2023, 9,6)
    # start_time1 = end_time1 - timedelta(hours=time_interval)
    # print("&&&&&&&&&&",end_time1, start_time1)
    from datetime import date

    sd1 = date(2023,9,1)
    ed1 = date(2023,9,5)

    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        except ValueError:
            start_date = datetime.now().date()
    else:
        start_date = datetime.now().date()

    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            end_date = datetime.now().date()
    else:
        end_date = datetime.now().date()

    print(start_date, end_date, "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    # Calculate the time range for the selected dates and hours
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)
   

# Calculate the time range for the selected dates and hours
#     start_time = datetime.combine(start_date, datetime.min.time())
#     print(start_date, "start_time, $$$$$$$$$$$$$$$$$$$$$$$")
#     # end_time = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)
#     end_time = datetime(2023, 6,10)
    print(start_date, end_date, "$$$$$$$$$$$$$$$$$$$$$ 12345")

    filtered_data_type = Audits.objects.filter(date__range=[start_date, end_date])
    print(filtered_data_type,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    # Get a list of unique appd_application_name values
    application_names = filtered_data_type.values('appd_application_name').distinct()
    print(application_names,"@@@@@@@@@@@@@@@@@@@@@@@@")

    selected_application = request.GET.get('selected_application','Maas Portal')

    # Filter the data based on the selected application name
    if selected_application:
        print("377111111111111111111111111111111111111111111111111")
        # filtered_data_type = filtered_data.filter(date__range=[start_date, end_date])

        type_data = Audits.objects.filter(appd_application_name=selected_application, date__range=[start_date, end_date])\
            .values('type')\
            .annotate(type_count=Count('type'))
                        
        # type_data = filtered_data.filter(appd_application_name=selected_application).values('type').annotate(type_count=Count('type'))
        print(selected_application,"SSSSSSSSSSSSSSSSSSSSSSs")
        print(type_data,"@@@@@@@@@@@@@@@@@@@@@S")
        # print(group_count,"@@@@@@@@@@@@@@@@@@@@@S")

    else:
        print("3744444444444444444444444444444444444444444444444 ")
        type_data = []

        # Filter the data based on the selected application name
    if selected_application:
        # filtered_data_severity = filtered_data.filter(date__range=[start_date, end_date])
        severity_data = Audits.objects.filter(appd_application_name=selected_application , date__range=[start_date, end_date])\
                            .values('severity').annotate(severity_count=Count('severity'))
        print(selected_application,"SSSSSSSSSSSSSSSSSSSSSSs")
        print(severity_data,"@@@@@@@@@@@@@@@@@@@@@S")
    else:
        print("3744444444444444444444444444444444444444444444444 ")
        severity_data = []

    context = {
                'application_names': application_names,
                'selected_application': selected_application,
                'type_data':type_data,
                'severity_data': severity_data,
                'start_d':start_date.strftime("%Y-%m-%d"),
                'end_d':end_date.strftime("%Y-%m-%d"),
                }
    return render(request, 'chartapp/aaaaa_app.html', context)
    # return render(request, 'chartapp/display_test.html', context)


    # return render(request, 'chartapp/display_test.html', {'application_names': application_names, 'selected_application': selected_application, 'type_data': type_data})



########################################################################################


def display_typedata(request):
    start_date = request.GET.get('start_date')  # Get start_date from query parameters
    end_date = request.GET.get('end_date')

    time_interval = request.GET.get('interval')  # Assuming the interval is passed as a query parameter like '?interval=1'
    # try:
    #     time_interval = int(time_interval)
    # except (ValueError, TypeError):
    #     time_interval = 1  # If the interval parameter is not provided or invalid, default to 1 hour

    # # Calculate the start and end time based on the selected time interval
    # end_time1 = datetime(2023, 9,6)
    # start_time1 = end_time1 - timedelta(hours=time_interval)
    # print("&&&&&&&&&&",end_time1, start_time1)
    from datetime import date

    sd1 = date(2023,9,1)
    ed1 = date(2023,9,5)

    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        except ValueError:
            start_date = datetime.now().date()
    else:
        start_date = datetime.now().date()

    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            end_date = datetime.now().date()
    else:
        end_date = datetime.now().date()

    print(start_date, end_date, "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    # Calculate the time range for the selected dates and hours
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)
   

# Calculate the time range for the selected dates and hours
#     start_time = datetime.combine(start_date, datetime.min.time())
#     print(start_date, "start_time, $$$$$$$$$$$$$$$$$$$$$$$")
#     # end_time = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)
#     end_time = datetime(2023, 6,10)
    print(start_date, end_date, "$$$$$$$$$$$$$$$$$$$$$ 12345")

    filtered_data_type = Audits.objects.filter(date__range=[start_date, end_date])
    print(filtered_data_type,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    # Get a list of unique appd_application_name values
    type_names_dist = Audits.objects.values('type').distinct()
    print(type_names_dist,"@@@@@@@@@@@@@@@@@@@@@@@@")

    selected_type  = request.GET.get('selected_type','POLICY_CLOSE_WARNING')

    # Filter the data based on the selected application name
    if selected_type:
        print("377111111111111111111111111111111111111111111111111")
        # filtered_data_type = filtered_data.filter(date__range=[start_date, end_date])
                
        app_data = Audits.objects.filter(type=selected_type, date__range=[start_date, end_date]).values('appd_application_name').annotate(apps_count=Count('appd_application_name')).order_by('appd_application_name')
        # type_data = filtered_data.filter(appd_application_name=selected_application).values('type').annotate(type_count=Count('type'))
        print(selected_type,"SSSSSSSSSSSSSSSSSSSSSSs")
        print(app_data,"@@@@@@@@@@@@@@@@@@@@@S")
        # print(group_count,"@@@@@@@@@@@@@@@@@@@@@S")

    else:
        print("3744444444444444444444444444444444444444444444444 ")
        app_data = []

    if selected_type:
        print("Top 10 Application")
        # filtered_data_type = filtered_data.filter(date__range=[start_date, end_date])
        # top_five_data = top_five_filter                                                              .values('appd_application_name').annotate(count=Count('appd_application_name')).order_by('-count')[:10]
        app_data_top_10 = Audits.objects.filter(type=selected_type, date__range=[start_date, end_date])\
                .values('appd_application_name').annotate(apps_count_topten=Count('appd_application_name'))\
                .order_by('-apps_count_topten')[:10]
        print(app_data_top_10,"@@@@@@@@@@@@@@@@@@@@@S")
        # print(group_count,"@@@@@@@@@@@@@@@@@@@@@S")

    else:
        print("No application Found")
        app_data_top_10 = []


    if selected_type:
        print("Bottom 10 Application")
        # filtered_data_type = filtered_data.filter(date__range=[start_date, end_date])
        app_data_bottom_10 = Audits.objects.filter(type=selected_type, date__range=[start_date, end_date])\
                .values('appd_application_name').annotate(apps_count_b10=Count('appd_application_name'))\
                .order_by('apps_count_b10')[:10]
        print(app_data_bottom_10,"@@@@@@@@@@@@@@@@@@@@@S")
        # print(group_count,"@@@@@@@@@@@@@@@@@@@@@S")

    else:
        print("No application Found")
        app_data_bottom_10 = []

    context = {
                'type_names': type_names_dist,
                'selected_type': selected_type,
                'app_data':app_data,
                'app_data_bottom_10': app_data_bottom_10,
                'app_data_top_10': app_data_top_10,
                'start_d':start_date.strftime("%Y-%m-%d"),
                'end_d':end_date.strftime("%Y-%m-%d"),
                }
    return render(request, 'chartapp/aaaaa_type.html', context)

########################################################################################

def display_severitydata(request):

    start_date = request.GET.get('start_date')  # Get start_date from query parameters
    end_date = request.GET.get('end_date')
    
    time_interval = request.GET.get('interval')  # Assuming the interval is passed as a query parameter like '?interval=1'
    # try:
    #     time_interval = int(time_interval)
    # except (ValueError, TypeError):
    #     time_interval = 1  # If the interval parameter is not provided or invalid, default to 1 hour

    # # Calculate the start and end time based on the selected time interval
    # end_time1 = datetime(2023, 9,6)
    # start_time1 = end_time1 - timedelta(hours=time_interval)
    # print("&&&&&&&&&&",end_time1, start_time1)
    from datetime import date

    sd1 = date(2023,9,1)
    ed1 = date(2023,9,5)

    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        except ValueError:
            start_date = datetime.now().date()
    else:
        start_date = datetime.now().date()

    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            end_date = datetime.now().date()
    else:
        end_date = datetime.now().date()

    print(start_date, end_date, "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    # Calculate the time range for the selected dates and hours
    # start_date = datetime.combine(start_date, datetime.min.time()) - timedelta(days=1)
    # end_date = datetime.combine(end_date, datetime.min.time()) #+ timedelta(days=-15)

    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)



    print(start_date, end_date, "$$$$$$$$$$$$$$$$$$$$$ 12345")

    filtered_data_type = Audits.objects.filter(date__range=[start_date, end_date])
    print(filtered_data_type,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("642 >>>>>>>>>>>>>>>>>>>")

    my_field_values = filtered_data_type.values('appd_application_name')
    print(my_field_values,"645 >>>>>>>>>>>>>>>>>>")

    # Get a list of unique appd_application_name values
    severity_names_dist = filtered_data_type.values('severity').distinct()
    print(severity_names_dist,"645 &&&&&&&&&&&&&&&&&&&&&")


    
    default_severity = severity_names_dist[0] if severity_names_dist else ''
    selected_severity  = request.GET.get('selected_severity','ERROR')
    selected_apps  = request.GET.get('appd_application_name')

    default_severity = severity_names_dist[0] if severity_names_dist else ''


    # Filter the data based on the selected application name
    if selected_severity:
        print("377111111111111111111111111111111111111111111111111")
        # filtered_data_type = filtered_data.filter(date__range=[start_date, end_date])
        app_data = Audits.objects.filter(severity=selected_severity, date__range=[start_date, end_date])\
                        .values('appd_application_name')\
                        .annotate(apps_count=Count('severity', distinct=True))\
                        .order_by('appd_application_name')

        print(selected_severity,"SSSSSSSSSSSSSSSSSSSSSSs")
        print(app_data,"@@@@@@@@@@@@@@@@@@@@@S")
        # print(group_count,"@@@@@@@@@@@@@@@@@@@@@S")

    else:
        
        print("3744444444444444444444444444444444444444444444444")
        app_data = []

    if selected_severity:
        print("Top 10 Application")
        severity_app_data_top_10 = Audits.objects.filter(type=selected_severity, date__range=[start_date, end_date])\
            .values('appd_application_name').annotate(sevr_apps_count_topten=Count('severity', distinct=True))\
            .order_by('-sevr_apps_count_topten')[:10]
        print(severity_app_data_top_10,"@@@@@@@@@@@@@@@@@@@@@S")
        # print(group_count,"@@@@@@@@@@@@@@@@@@@@@S")

    else:
        print("No application Found")
        severity_app_data_top_10 = []


    if selected_severity:
        print("Bottom 10 Application")
        # filtered_data_type = filtered_data.filter(date__range=[start_date, end_date])
        severity_app_data_bottom_10 = Audits.objects.filter(type=selected_severity, date__range=[start_date, end_date]) \
                .values('appd_application_name').annotate(sevr_apps_count_b10=Count('appd_application_name'))\
                .order_by('sevr_apps_count_b10')[:10]
        print(severity_app_data_bottom_10,"@@@@@@@@@@@@@@@@@@@@@S")
        # print(group_count,"@@@@@@@@@@@@@@@@@@@@@S")

    else:
        print("No application Found")
        severity_app_data_bottom_10 = []

    context = {
                'severity_names': severity_names_dist,
                'selected_severity': selected_severity,
                'app_data':app_data,
                'start_d':start_date.strftime("%Y-%m-%d"),
                'end_d':end_date.strftime("%Y-%m-%d"),
                # 'default_severity': default_severity,
                's_app_data_bottom_10':  severity_app_data_bottom_10,
                's_app_data_top_10': severity_app_data_top_10,
                }
    return render(request, 'chartapp/aaaaa_severity.html', context)

###############################################################################
from django.db.models import Count

import matplotlib.pyplot as plt
from django.shortcuts import render
from django.db.models import Sum
from .models import Audits


# def index(request):
#     applications = Audits.objects.values('appd_application_name').annotate(total_value=Sum('appd_application_name'))
#     print(applications, "varun326")
#     return render(request, 'chartapp/widgets.html', {'applications': applications})

# def application_detail(request, type):
#     application_data = Audits.objects.filter(type=type)
#     return render(request, 'chartapp/widgets.html', {'application_data': application_data})

def app_view1(request):
    unique_applications = Audits.objects.values_list('appd_application_name', flat=True).distinct()
    print(unique_applications, "!!!!!!!!!!!!!!!!!!!!!!! 335")
    return render(request, 'chartapp/apps.html', {'unique_applications': unique_applications})

from .models import Audits

def app_view2(request):
    data = Audits.objects.values('type').annotate(count=Count('_id'))
    print(data, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    return render(request, 'chartapp/apps.html', {'data': data})



#############################################################################################################

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
    else:
        form = RegistrationForm()
    return render(request, 'chartapp/register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # print("!!!!!!!!!@@@@@@@@@@@@@@@", form)
        if form.is_valid():            
            user_email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print("##########", user_email, password)
            user = authenticate(request, email=user_email, password=password)
            print("user.username@@@@@@@@", user)
            print("@@@@@@@@@@@@@@@@@@@@@@@@22", user)
            print(user_email, password, user," epu")
            # user.is_active = True
            print("420 *")
            
            if user and user.is_active:
                print(user)
                print("422 !")
                login(request, user)
                return redirect('hourdate')  # Replace 'home' with your desired homepage URL
            else:
                print("424, user = ", user)
                form.add_error(None, 'Invalid email or password 2')
    else:
        print("428")
        form = LoginForm()
    return render(request, 'chartapp/login.html', {'form': form})


# from django.contrib import messages
# def user_login(request):
#     if request.method == 'POST':
  
#         # AuthenticationForm_can_also_be_used
#         username = request.POST['email']
#         password = request.POST['password']
#         print(username, password, "######################")
#         user = authenticate(request, username = username, password = password)
#         print("&&&&&&&&&&&&&&&&&&&&", user)
#         if user is not None:
#             form = login(request, user)
#             messages.success(request, f' welcome {username} !!')
#             return redirect('hourdate')
#         else:
#             messages.info(request, f'account done not exit plz sign in')
#     form = LoginForm()
#     return render(request, 'chartapp/login.html', {'form':form, 'title':'log in'})
############################################################################################################

def chart_view(request):
    # Retrieve the time interval from the query parameters
    time_interval = request.GET.get('interval')  # Assuming the interval is passed as a query parameter like '?interval=1'

    # Parse the time interval parameter
    try:
        time_interval = int(time_interval)
    except (ValueError, TypeError):
        time_interval = 1  # If the interval parameter is not provided or invalid, default to 1 hour

    # Calculate the start and end time based on the selected time interval
    end_time = datetime(2023, 6,10)
    start_time = end_time - timedelta(hours=time_interval)

    # Retrieve data from the database for the selected time range
    data = Audits.objects.all()
    print(data)
    data = data.filter(date__range=(start_time, end_time))
    data = data.values('appd_application_name').annotate(count=Count('_id')).order_by('appd_application_name')
    print(data)

    # Prepare the data for the chart
    labels = [str(dp.date) for dp in data]
    values = [dp.type for dp in data]
    print(labels)
    print(values)

    # Pass the data and selected interval to the template for rendering
    context = {
        'labels': labels,
        'values': values,
        'selected_interval': time_interval,
    }
    return render(request, 'chartapp/chart.html', context)

################## old code ####################################


@csrf_exempt
def graphapi(request, id=0):
        # result = Audits.objects.all()
        
        # for splitdate in result:
        #      fullnamesplit = splitdate.date.split(', ')
        #      print(fullnamesplit)
        
        # print(result)
        # start_date = start_date.strptime(date, "YYYY_MM_DD HH:MM:SS")
                        
        # result123= Audits.objects.filter(date='date').annotate(slash_pos=StrIndex(F('date'), ' ')
        #                         ).annotate(
        #                         y=Substr(F('id'), F('slash_pos')))
        #result123= Audits.objects.extra(select={'date': 'SUBSTRING_INDEX(symbol, " ")'})
        # print(result)
        # print(result12)

                       
                       
    
        # resultdf=Audits.objects.values('type','severity','summary', 'appd_application_name','timestamp', 'date')
        # print(resultdf)

        # lst=[]
        # for x in resultdf:
        #         lst.append(x)
        
        # print("varun")
        # print(result)
        # import pandas as pd
        # df = pd.DataFrame(lst)
        # print(df)
        # model1 = Audits.objects.bulk_create(df)
        # print(model1)
        # iterate over DataFrame and create your objects
        # from sqlalchemy import create_engine
        # engine = create_engine(result, echo=False)
        # ds = df.to_sql(Audits, con=engine)
        # print(ds)

        result = Audits.objects.values('appd_application_name',)\
                        .annotate(count=Count('_id'))\
                        .annotate(count=Count('severity'))
        varun = Audits.objects.values('severity')\
                                .annotate(count_ser=Count('appd_application_name'))
        
        kumar = Audits.objects.values('type')\
                                .annotate(count_aap=Count('appd_application_name'))

        extradate = Audits.objects.values('date')\
                                .annotate(start_hour=Extract('date',"hour"))
        # added refresh button
        # print(extradate)

        context ={
                "products":result,
                "bar": varun,
                "piechat": kumar,
                
                }
        return render(request,'chartapp/index.html', context)




def showresults(request):
    if request.method =="POST":
          fromdate= request.POST.get('fromdate')
          todate= request.POST.get('todate')
          searchresults = Audits.objects.raw('db.appd_events_audit.find({"date" : {"$gte": "'+fromdate + '", "$lt": "'+todate+'"}})')
          return render(request, 'chartapp/varun.html', {'data': displaydata})
    else:
          displaydata = Audits.objects.all()
          return render(request, 'chartapp/varun.html', {'data': displaydata})
    

@csrf_exempt
def dateapi(request, id=0):
        if request.method =="POST":
          fromdate= request.POST.get('fromdate')
          todate= request.POST.get('todate')
        result = Audits.objects.values('date')\
                                .annotate(count=Count('type'))
        # searchresults = Audits.objects.raw('.find({"date" : {"$gte": "'+fromdate + '", "$lt": "'+todate+'"}})')

        context ={
                  "products":result
                                }
        return render(request,'chartapp/testdatecopy22.html', context)


# def bar_graph(request):
#     start_date = '2023-06-01 00:00:00'  # Replace with your desired start date
#     end_date = '2023-06-30 00:00:00'    # Replace with your desired end date

#     # Connect to the MongoDB database
#     client = MongoClient('mongodb://localhost:27017')
#     db = client['test']  # Replace with your database name
#     collection = db['appd_events_audit']  # Replace with your collection name

#     # Retrieve data from MongoDB and filter based on the date range
#     records = collection.find({'date': {'$gte': start_date, '$lte': end_date}})
#     print(records,"varun")
#     lst=[]

#     for x in records:
#          print(x)
#          lst.append(x)
#     print(lst)
#     # Prepare the data for the chart
#     data = pd.DataFrame(list(records))
#     chart_data = data.groupby('date').sum().reset_index()

#     # Pass the chart data to the template
#     return render(request, 'chartapp/bar_graph.html', {'chart_data': chart_data})
              

##############################################################################################

@csrf_exempt
def timelineapi(request, id=0):
     
        result = Audits.objects.values('date')\
                                .annotate(count=Count('_id'))
        context ={
                "productsdate":result
                        }
        return render(request,'chartapp/testdate2.1.html', context)
###################################################################################################

# def filtered_data_view_1(request):
    
#     start_date = request.GET.get('start_date')  # Get start_date from query parameters
#     end_date = request.GET.get('end_date')  # Get end_date from query parameters
#         # Calculate the datetime range for the last one hour
# #     end_date = datetime(2023, 6,10)
# #     start_date = datetime(2023, 6,1)

#     print("181")
#     print(start_date)
#     print(end_date)

#     # Perform filtering based on start_date and end_date
#     filtered_data = Audits.objects.all()  # Start with all objects

#     # print(filtered_data)
#     if start_date and end_date:
#         filtered_data_1 = filtered_data.filter(date__range=[start_date, end_date])
#         print(filtered_data_1)
#         #filtered_data = Audits.objects.values('appd_application_name').annotate(count=Count('_id'))
#         filtered_data_app = filtered_data_1.values('appd_application_name').annotate(count=Count('_id')).order_by('appd_application_name')
#         print(filtered_data_app)

#         # filtered_data = filtered_data.filter(date__range=[start_date, end_date])
#         filtered_data_type = filtered_data.values('type').annotate(count=Count('_id')).order_by('type')
#         print(filtered_data_type)
        
#     context = {
#                 'data1': filtered_data_app,
#         #        'type': filtered_data_type
#                }
# #     print(context)
#     return render(request, 'chartapp/filtered_data.html', context)

from django.shortcuts import render
from .models import Audits


try:
    def dashboard(request):
        application_names = Audits.objects.values('appd_application_name').distinct().order_by('appd_application_name')
        # print(application_names, "@@@@@@@@@@@@@@@@@@@@@@ 325")
        # print("326","!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return render(request, 'chartapp/dropdown.html', {'application_names': application_names})

    

    def get_type_counts(request):
        print("331-1")
        application_name = request.GET.get('appd_application_name', '')
        type_to_count = request.GET.get('type', '')
        print(application_name,"!!!!!!!!!!!!!!!!!!!! 333")
        
        if application_name:
            print("check 337 ~~~~~~~~~~~~~~~~~~~~~~~~~~")
            data = Audits.objects.filter(appd_application_name=application_name).values('type').annotate(count=Count('type')).order_by('type')
            # data = Audits.objects.filter(application_name=application_name).values('type').distinct().count()

            print(data, "@@@@@@@@@@@@@@@@@@@ 338")
        else:
            print("344")
            data = Audits.objects.values('type').annotate(count=Count('type')) # working
        print(data, "@@@@@@@@@@@@@@@@@@@ 345")

        labels = [entry['type'] for entry in data]
        counts = [entry['count'] for entry in data]
        print(labels, "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(counts, "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

        return JsonResponse({'labels': labels, 'counts': counts})
    
except Exception as e:
    print(e, "error at 3577777777777777777777777777777")



def filtered_data_view(request):
    
    # start_date = datetime.combine(selected_date, datetime.min.time())
    # end_date = datetime(2023, 6,10) #start_time + timedelta(days=1)
    start_date = request.GET.get('start_date')  # Get start_date from query parameters
    end_date = request.GET.get('end_date')   # Get end_date from query parameters
    print(start_date, end_date, "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    # Parse the time interval parameter
    time_interval = request.GET.get('interval')  # Assuming the interval is passed as a query parameter like '?interval=1'
    try:
        time_interval = int(time_interval)
    except (ValueError, TypeError):
        time_interval = 1  # If the interval parameter is not provided or invalid, default to 1 hour

    # Calculate the start and end time based on the selected time interval
    end_time1 = datetime(2023, 6,10)
    start_time1 = end_time1 - timedelta(hours=time_interval)
    print("&&&&&&&&&&",end_time1, start_time1)

    

    try:
        if True:
                # Perform filtering based on start_date and end_date
                filtered_data = Audits.objects.all()  # Start with all objects
                filtered_data = filtered_data.filter(date__range=[start_time1, end_time1])

                filtered_data_app = filtered_data.values('appd_application_name').annotate(count=Count('_id')).order_by('appd_application_name')
                # filtered_data_app = filtered_data.values('appd_application_name').annotate(count=Count('_id')).order_by('appd_application_name')
                print(filtered_data_app)
                filtered_type = filtered_data.values('type').annotate(count=Count('_id')).order_by('type')
                
                # houlry based data
                filtered_data1 = filtered_data.filter(date__range=[start_time1, end_time1])
                data_hourly_type = filtered_data1.values('type').annotate(count=Count('_id')).order_by('type')
                print("*******************************************************")
                print(data_hourly_type)

                # Prepare the data for the bar charts
                #     for x in filtered_data:
                #          print(x.date)
                print("##################### print data from loop ############################################")
                labels1 = [dp.date for dp in filtered_data]
                values1 = [dp.appd_application_name for dp in filtered_data]
                #     print(labels1)
                print("#################################################################")
                context = {
                        'data': filtered_data_app,
                        # 'type': filtered_type,
                        'selected_hour':data_hourly_type,
                        # 'selected_date': date.strftime('%Y-%m-%d'),
                }
        return render(request, 'chartapp/filtered_data.html', context)
    except:
         print("#################################################################")
         pass



def widget_view(request):
    start_date = request.GET.get('start_date')  # Get start_date from query parameters
    end_date = request.GET.get('end_date')

    time_interval = request.GET.get('interval')  # Assuming the interval is passed as a query parameter like '?interval=1'
    # try:
    #     time_interval = int(time_interval)
    # except (ValueError, TypeError):
    #     time_interval = 1  # If the interval parameter is not provided or invalid, default to 1 hour

    # # Calculate the start and end time based on the selected time interval
    # end_time1 = datetime(2023, 9,6)
    # start_time1 = end_time1 - timedelta(hours=time_interval)
    # print("&&&&&&&&&&",end_time1, start_time1)
    from datetime import date

    sd1 = date(2023,9,1)
    ed1 = date(2023,9,5)

    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        except ValueError:
            start_date = datetime.now().date()
    else:
        start_date = datetime.now().date()

    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            end_date = datetime.now().date()
    else:
        end_date = datetime.now().date()

    print(start_date, end_date, "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    # Calculate the time range for the selected dates and hours
    start_date = datetime.combine(start_date, datetime.min.time())
    end_date = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)
   

#     Calculate the time range for the selected dates and hours
#     start_time = datetime.combine(start_date, datetime.min.time())
#     print(start_date, "start_time, $$$$$$$$$$$$$$$$$$$$$$$")
#     # end_time = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)
#     end_time = datetime(2023, 6,10)
    print(start_date, end_date, "$$$$$$$$$$$$$$$$$$$$$ 12345")


    if time_interval:
        try:
            time_interval = int(time_interval)
        except ValueError:
            time_interval = None

    if time_interval is not None:
        end_date = datetime(2023, 9,5)
        start_date = end_date - timedelta(hours=time_interval)
        # end_time += timedelta(hours=end_hour)


    filtered_data = Audits.objects.all()  # Start with all objects
    filtered_data = filtered_data.filter(date__range=[start_date, end_date])
    # filtered_data_overall = filtered_data
    print(len(filtered_data))




    grouped_data = Audits.objects.values('appd_application_name').annotate(count=Count('type')) #annotate

    context = {
                'gb_data': grouped_data,
                'start_d':sd1.strftime("%Y-%m-%d"),
                'end_d':ed1.strftime("%Y-%m-%d"),
                }
                
    return render(request, 'chartapp/widgets.html', context)

#################################################################################


# views.py
