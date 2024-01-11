from django.shortcuts import render, HttpResponse
from .models import rbi_log
import json

from django.http import JsonResponse,request
from django.core.serializers import serialize
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponseBadRequest

from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from datetime import date,datetime, timedelta
from django.shortcuts import get_object_or_404
from .forms import DateRangeFilterForm
from django.http import HttpResponseNotAllowed
from django.db.models import Min, Max
from calendar import monthrange
from django.db.models import Q
from datetime import datetime, timedelta

from .forms import DateRangeForm
from django.core.exceptions import ObjectDoesNotExist








def rbinewhome(request):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)

    fema_data = rbi_log.objects.using('rbi').filter(source_name='rbi_fema', date_of_scraping__date__range=[start_date, end_date]).order_by('-date_of_scraping')
    ecb_data = rbi_log.objects.using('rbi').filter(source_name='rbi_ecb', date_of_scraping__date__range=[start_date, end_date]).order_by('-date_of_scraping')
    odi_data = rbi_log.objects.using('rbi').filter(source_name='rbi_odi', date_of_scraping__date__range=[start_date, end_date]).order_by('-date_of_scraping')
   
    try:
        fema_latest_entry = rbi_log.objects.using('rbi').filter(source_name='rbi_fema').latest('date_of_scraping')
        fema_latest_count = fema_latest_entry.total_record_count if fema_latest_entry.total_record_count is not None else "0" if fema_latest_entry.script_status == 'Success' else "-"
    except ObjectDoesNotExist:
        fema_latest_count = "-"

    try:
        ecb_latest_entry = rbi_log.objects.using('rbi').filter(source_name='rbi_ecb').latest('date_of_scraping')
        ecb_latest_count = ecb_latest_entry.total_record_count if ecb_latest_entry.total_record_count is not None else "0" if ecb_latest_entry.script_status == 'Success' else "-"
    except ObjectDoesNotExist:
        ecb_latest_count = "-"
        
    try:
        odi_latest_entry = rbi_log.objects.using('rbi').filter(source_name='rbi_odi').latest('date_of_scraping')
        odi_latest_count = odi_latest_entry.total_record_count if odi_latest_entry.total_record_count is not None else "0" if odi_latest_entry.script_status == 'Success' else "-"
    except ObjectDoesNotExist:
        odi_latest_count = "-"


        
    data_list = []

    for date in (end_date - timedelta(days=i) for i in range(7)):
        fema_entry = fema_data.filter(date_of_scraping__date=date).first()
        ecb_entry = ecb_data.filter(date_of_scraping__date=date).first()
        odi_entry = odi_data.filter(date_of_scraping__date=date).first()
        
        fema_data_available = fema_entry.data_available if fema_entry is not None and fema_entry.data_available is not None else "0" if fema_entry is not None and fema_entry.script_status == 'Success' else "NA" if fema_entry is not None and fema_entry.script_status == 'Failure' else "-"
        fema_data_scraped = fema_entry.data_scraped if fema_entry is not None and fema_entry.data_scraped is not None else "0" if fema_entry is not None and fema_entry.script_status == 'Success' else "NA" if fema_entry is not None and fema_entry.script_status == 'Failure' else "-"
        fema_total_count = fema_entry.total_record_count if fema_entry else "-"
        
        ecb_data_available = ecb_entry.data_available if ecb_entry is not None and ecb_entry.data_available is not None else "0" if ecb_entry is not None and ecb_entry.script_status == 'Success' else "NA" if ecb_entry is not None and ecb_entry.script_status == 'Failure' else "-"
        ecb_data_scraped = ecb_entry.data_scraped if ecb_entry is not None and ecb_entry.data_scraped is not None else "0" if ecb_entry is not None and ecb_entry.script_status == 'Success' else "NA" if ecb_entry is not None and ecb_entry.script_status == 'Failure' else "-"
        ecb_total_count = ecb_entry.total_record_count if ecb_entry else "-"
        
        odi_data_available = odi_entry.data_available if odi_entry is not None and odi_entry.data_available is not None else "0" if odi_entry is not None and odi_entry.script_status == 'Success' else "NA" if odi_entry is not None and odi_entry.script_status == 'Failure' else "-"
        odi_data_scraped = odi_entry.data_scraped if odi_entry is not None and odi_entry.data_scraped is not None else "0" if odi_entry is not None and odi_entry.script_status == 'Success' else "NA" if odi_entry is not None and odi_entry.script_status == 'Failure' else "-"
        odi_total_count = odi_entry.total_record_count if odi_entry else "-"
         
        fema_status = fema_entry.script_status if fema_entry is not None else 'N/A'
        ecb_status = ecb_entry.script_status if ecb_entry is not None else 'N/A'
        odi_status = odi_entry.script_status if odi_entry is not None else 'N/A'
        
        fema_reason = fema_entry.failure_reason if fema_entry is not None else None
        ecb_reason = ecb_entry.failure_reason if ecb_entry is not None else None
        odi_reason = odi_entry.failure_reason if odi_entry is not None else None
        
        

        # Determine the color based on status and reason
        fema_color = (
            'green' if fema_status == 'Success' else
            'orange' if fema_status == 'Failure' and '204' in str(fema_reason) else
            'red' if fema_status == 'Failure' else
            'black'
        )
  
        ecb_color = (
            'green' if ecb_status == 'Success' else
            'orange' if ecb_status == 'Failure' and '204' in str(ecb_reason) else
            'red' if ecb_status == 'Failure' else
            'black'
        )  
        
        odi_color = (
            'green' if odi_status == 'Success' else
            'orange' if odi_status == 'Failure' and '204' in str(odi_reason) else
            'red' if odi_status == 'Failure' else
            'black'
        )
  
        data_list.append({
            'Date': date.strftime('%d-%m-%Y'),
            'FEMA_Data_Available': fema_data_available,
            'FEMA_Data_Scraped': fema_data_scraped,
            'FEMA_Color': fema_color,
            'ECB_Data_Available': ecb_data_available,
            'ECB_Data_Scraped': ecb_data_scraped,
            'ECB_Color': ecb_color,
            'ODI_Data_Available': odi_data_available,
            'ODI_Data_Scraped': odi_data_scraped,
            'ODI_Color': odi_color,
    
        })

    context = {
        'data_list': data_list,  'fema_latest_count': fema_latest_count, 'ecb_latest_count': ecb_latest_count,  'odi_latest_count': odi_latest_count}

    return render(request, 'fema/rbinewhome.html', context)



def rbi_tab(request):
    rbi_data= rbi_log.objects.using('rbi').all()
    return render(request,'fema/index.html', {'rbi_data':rbi_data}) 






def rbinewhome123(request):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)

    fema_data = rbi_log.objects.using('rbi').filter(source_name='rbi_fema', date_of_scraping__date__range=[start_date, end_date]).order_by('-date_of_scraping')
    ecb_data = rbi_log.objects.using('rbi').filter(source_name='rbi_ecb', date_of_scraping__date__range=[start_date, end_date]).order_by('-date_of_scraping')
    odi_data = rbi_log.objects.using('rbi').filter(source_name='rbi_odi', date_of_scraping__date__range=[start_date, end_date]).order_by('-date_of_scraping')
    
    data_list = []

    for date in (end_date - timedelta(days=i) for i in range(7)):
        fema_entry = fema_data.filter(date_of_scraping__date=date).first()
        ecb_entry = ecb_data.filter(date_of_scraping__date=date).first()
        odi_entry = odi_data.filter(date_of_scraping__date=date).first()
        
        fema_data_available = fema_entry.data_available if fema_entry is not None and fema_entry.data_available is not None else "0" if fema_entry is not None and fema_entry.script_status == 'Success' else "NA" if fema_entry is not None and fema_entry.script_status == 'Failure' else "-"
        fema_data_scraped = fema_entry.data_scraped if fema_entry is not None and fema_entry.data_scraped is not None else "0" if fema_entry is not None and fema_entry.script_status == 'Success' else "NA" if fema_entry is not None and fema_entry.script_status == 'Failure' else "-"
        ecb_data_available = ecb_entry.data_available if ecb_entry is not None and ecb_entry.data_available is not None else "0" if ecb_entry is not None and ecb_entry.script_status == 'Success' else "NA" if ecb_entry is not None and ecb_entry.script_status == 'Failure' else "-"
        ecb_data_scraped = ecb_entry.data_scraped if ecb_entry is not None and ecb_entry.data_scraped is not None else "0" if ecb_entry is not None and ecb_entry.script_status == 'Success' else "NA" if ecb_entry is not None and ecb_entry.script_status == 'Failure' else "-"
        
        odi_data_available = odi_entry.data_available if odi_entry is not None and odi_entry.data_available is not None else "0" if odi_entry is not None and odi_entry.script_status == 'Success' else "NA" if odi_entry is not None and odi_entry.script_status == 'Failure' else "-"
        odi_data_scraped = odi_entry.data_scraped if odi_entry is not None and odi_entry.data_scraped is not None else "0" if odi_entry is not None and odi_entry.script_status == 'Success' else "NA" if odi_entry is not None and odi_entry.script_status == 'Failure' else "-"
        
        fema_status = fema_entry.script_status if fema_entry is not None else 'N/A'
        ecb_status = ecb_entry.script_status if ecb_entry is not None else 'N/A'
        odi_status = odi_entry.script_status if odi_entry is not None else 'N/A'
        
        fema_reason = fema_entry.failure_reason if fema_entry is not None else None
        ecb_reason = ecb_entry.failure_reason if ecb_entry is not None else None
        odi_reason = odi_entry.failure_reason if odi_entry is not None else None
        
        

        # Determine the color based on status and reason
        fema_color = (
            'green' if fema_status == 'Success' else
            'orange' if fema_status == 'Failure' and '204' in str(fema_reason) else
            'red' if fema_status == 'Failure' else
            'black'
        )
  
        ecb_color = (
            'green' if ecb_status == 'Success' else
            'orange' if ecb_status == 'Failure' and '204' in str(ecb_reason) else
            'red' if ecb_status == 'Failure' else
            'black'
        )  
        
        odi_color = (
            'green' if odi_status == 'Success' else
            'orange' if odi_status == 'Failure' and '204' in str(odi_reason) else
            'red' if odi_status == 'Failure' else
            'black'
        )
  
        data_list.append({
            'Date': date.strftime('%d-%m-%Y'),
            'FEMA_Data_Available': fema_data_available,
            'FEMA_Data_Scraped': fema_data_scraped,
            'FEMA_Color': fema_color,
            'ECB_Data_Available': ecb_data_available,
            'ECB_Data_Scraped': ecb_data_scraped,
            'ECB_Color': ecb_color,
            'ODI_Data_Available': odi_data_available,
            'ODI_Data_Scraped': odi_data_scraped,
            'ODI_Color': odi_color,
        })

    context = {
        'data_list': data_list
    }

    return render(request, 'fema/grid.html', context)




  
def rbiget_data_for_popup1(request, source_name):
    today_date = timezone.now().date()
    data = rbi_log.objects.using('rbi').filter(source_name=source_name, date_of_scraping__date=today_date).first()

    if data:
        
         # Replace None values with hyphen
        data_scraped = data.data_scraped if data.data_scraped is not None else "0"
        failure_reason = data.failure_reason if data.failure_reason is not None else "-"

        response_data = {
            'source_name': data.source_name,
            'script_status': data.script_status,
         
            'data_scraped': data_scraped,
          
          
            'failure_reason': failure_reason,
            
            'date_of_scraping': data.date_of_scraping.strftime('%d-%m-%Y'),
        }
        print(f"Today's Date: {today_date}")
        print(f"Source Name: {source_name}")

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponse(status=404)
    





from datetime import datetime, timedelta
from django.shortcuts import render
from .forms import DateRangeForm
from .models import rbi_log
from django.core.exceptions import ValidationError
from django import forms

def format_date(date):
    return date.strftime('%d-%m-%Y') if date else ''

def get_default_start_end_dates():
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=6)  # Default to past 7 days
    return start_date, end_date

def get_past_15_days():
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=14)
    return start_date, end_date

def get_last_month():
    today = datetime.now().date()
    end_date = today.replace(day=1) - timedelta(days=1)
    start_date = end_date.replace(day=1)
    return start_date, end_date

def get_status_color(script_status, failure_reason):
    if script_status == 'Success':
        return 'green'
    elif script_status == 'Failure' and '204' in str(failure_reason):
        return 'orange'
    else:
        return 'red'
    
    
def rbinewfema_datefilter(request):
    form = DateRangeForm(request.GET)
    
     # Default values for start_date and end_date
    start_date, end_date = get_default_start_end_dates()
    
    if form.is_valid():
        date_range = form.cleaned_data.get('date_range')
        if date_range == 'past_7_days':
            start_date, end_date = get_default_start_end_dates()
        elif date_range == 'past_15_days':
            start_date, end_date = get_past_15_days()
        elif date_range == 'last_month':
            start_date, end_date = get_last_month()
        elif date_range == 'custom':
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            if start_date and end_date:
                date_difference = end_date - start_date
                if date_difference.days > 60:
                    # Adjust end_date if it's more than 60 days from start_date
                    end_date = start_date + timedelta(days=60)
        else:
            start_date, end_date = get_default_start_end_dates()

    # Adjust end_date to cover the entire day
    # end_date = end_date + timedelta(days=1)

    data = rbi_log.objects.using('rbi').filter(
         date_of_scraping__date__range=[start_date, end_date],
        source_name='rbi_fema'
    )

    formatted_data = []
    for item in data:
        formatted_date = format_date(item.date_of_scraping)
        status_color = get_status_color(item.script_status, item.failure_reason)
        
         # Replace None values with hyphen
        data_available= item.data_available if item.data_available is not None else "0"
        data_scraped = item.data_scraped if item.data_scraped is not None else "0"
        failure_reason = item.failure_reason if item.failure_reason is not None else "-"
        
        formatted_data.append({
            'source_name': item.source_name,
            'script_status': item.script_status,
            'failure_reason': failure_reason,
            'data_available': data_available,
            'data_scraped': data_scraped,
            'date_of_scraping': formatted_date,
            'status_color': status_color,
        })

    context = {
        'form': form,
        'data': formatted_data,
        'start_date': format_date(start_date),
        'end_date': format_date(end_date),
        'past_15_days': (format_date(get_past_15_days()[0]), format_date(get_past_15_days()[1])),
        'last_month': (format_date(get_last_month()[0]), format_date(get_last_month()[1])),
        'table_name_filter': 'rbi_fema',
    }

    return render(request, 'fema/rbinewdatefilter.html', context)



def rbinewecb_datefilter(request):
    form = DateRangeForm(request.GET)
    
    
    # Default values for start_date and end_date
    start_date, end_date = get_default_start_end_dates()
    
    if form.is_valid():
        date_range = form.cleaned_data.get('date_range')
        if date_range == 'past_7_days':
            start_date, end_date = get_default_start_end_dates()
        elif date_range == 'past_15_days':
            start_date, end_date = get_past_15_days()
        elif date_range == 'last_month':
            start_date, end_date = get_last_month()
        elif date_range == 'custom':
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            if start_date and end_date:
                date_difference = end_date - start_date
                if date_difference.days > 60:
                    # Adjust end_date if it's more than 60 days from start_date
                    end_date = start_date + timedelta(days=60)
        else:
            start_date, end_date = get_default_start_end_dates()

    # Adjust end_date to cover the entire day
    # end_date = end_date + timedelta(days=1)

    data = rbi_log.objects.using('rbi').filter(
         date_of_scraping__date__range=[start_date, end_date],
        source_name='rbi_ecb'
    )

    formatted_data = []
    for item in data:
        formatted_date = format_date(item.date_of_scraping)
        status_color = get_status_color(item.script_status, item.failure_reason)
        
        # Replace None values with hyphen
        data_available= item.data_available if item.data_available is not None else "0"
        data_scraped = item.data_scraped if item.data_scraped is not None else "0"
        failure_reason = item.failure_reason if item.failure_reason is not None else "-"
        
        formatted_data.append({
            'source_name': item.source_name,
            'script_status': item.script_status,
            'failure_reason':failure_reason,
            'data_available':data_available,
            'data_scraped': data_scraped,
            'date_of_scraping': formatted_date,
            'status_color': status_color,
        })

    context = {
        'form': form,
        'data': formatted_data,
        'start_date': format_date(start_date),
        'end_date': format_date(end_date),
        'past_15_days': (format_date(get_past_15_days()[0]), format_date(get_past_15_days()[1])),
        'last_month': (format_date(get_last_month()[0]), format_date(get_last_month()[1])),
        'table_name_filter': 'rbi_ecb',
    }

    return render(request, 'fema/rbinewdatefilter.html', context)



def rbinewodi_datefilter(request):
    form = DateRangeForm(request.GET)
    
    
    # Default values for start_date and end_date
    start_date, end_date = get_default_start_end_dates()
    
    if form.is_valid():
        date_range = form.cleaned_data.get('date_range')
        if date_range == 'past_7_days':
            start_date, end_date = get_default_start_end_dates()
        elif date_range == 'past_15_days':
            start_date, end_date = get_past_15_days()
        elif date_range == 'last_month':
            start_date, end_date = get_last_month()
        elif date_range == 'custom':
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            if start_date and end_date:
                date_difference = end_date - start_date
                if date_difference.days > 60:
                    # Adjust end_date if it's more than 60 days from start_date
                    end_date = start_date + timedelta(days=60)
        else:
            start_date, end_date = get_default_start_end_dates()

    # Adjust end_date to cover the entire day
    # end_date = end_date + timedelta(days=1)

    data = rbi_log.objects.using('rbi').filter(
         date_of_scraping__date__range=[start_date, end_date],
        source_name='rbi_odi'
    )

    formatted_data = []
    for item in data:
        formatted_date = format_date(item.date_of_scraping)
        status_color = get_status_color(item.script_status, item.failure_reason)
        
        # Replace None values with hyphen
        data_available= item.data_available if item.data_available is not None else "0"
        data_scraped = item.data_scraped if item.data_scraped is not None else "0"
        failure_reason = item.failure_reason if item.failure_reason is not None else "-"
        
        formatted_data.append({
            'source_name': item.source_name,
            'script_status': item.script_status,
            'failure_reason':failure_reason,
            'data_available':data_available,
            'data_scraped': data_scraped,
            'date_of_scraping': formatted_date,
            'status_color': status_color,
        })

    context = {
        'form': form,
        'data': formatted_data,
        'start_date': format_date(start_date),
        'end_date': format_date(end_date),
        'past_15_days': (format_date(get_past_15_days()[0]), format_date(get_past_15_days()[1])),
        'last_month': (format_date(get_last_month()[0]), format_date(get_last_month()[1])),
        'table_name_filter': 'rbi_odi',
    }

    return render(request, 'fema/rbinewdatefilter.html', context)







