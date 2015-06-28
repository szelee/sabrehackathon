"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime, date, timedelta
import requests, json
from app.models import HotelES
from django.core import serializers

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Hotel Splitter - Home',
            'year':datetime.now().year,
        })
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'We always care about you',
            'year':datetime.now().year,
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Plan you stay smartly.',
            'year':datetime.now().year,
        })
    )

def result(request):
	"""Get the result"""
	checkin_date = convertdate(request.GET.get('in_date'))
	checkout_date = convertdate(request.GET.get('out_date'))
	days_diff = checkout_date - checkin_date
	day=[]
	url=[]
	response=[]
	day.append(checkin_date)
	country = request.GET.get('location')
	if int(days_diff.days) > 1:
		for i in range(2):
			day_value = i+1
			day.append(checkin_date + timedelta(days=(day_value)))
			url.append("http://dev.jellyfishsurpriseparty.com/polygon/rates/" + country + "/" + '{:%Y-%m-%d}'.format(day[i]) + "/" + '{:%Y-%m-%d}'.format(day[day_value]))
			response.append(requests.get(url[i]).json())
		hotel_list=[]
		j=0;		
		for day1 in response[0]:
			#print day1
			if j > 10:
				break
			j+=1
			data, desc = HotelES().getVenueName(day1['hotelName'])
			if 'images' in data:
				img = data['@giataId'] + ".jpg"
			else:
				img = False
			hotel1 = {'code': day1['hotelCode'], 'name': day1['hotelName'], 'rating':day1['starRating'],'lowrate': day1['minRate'], 'img':img,'desc': desc[0]['para']}
			k=0
			for day2 in response[1]:
				if k >10:
					break
				k+=1
				data, desc = HotelES().getVenueName(day2['hotelName'])
				if 'images' in data:
					img = data['@giataId'] + ".jpg"
				else:
					img = False
				hotel2 = {'code': day2['hotelCode'],'name': day2['hotelName'], 'rating':day2['starRating'],'lowrate': day2['minRate'],'img':img,'desc': desc[0]['para']}
				hotel_permutation = { 'hotel1': hotel1, 'hotel2': hotel2, 'total': day1['minRate'] + day2['minRate']}
				hotel_list.append(hotel_permutation)
		
		hotel_list = sorted(hotel_list, key=lambda k: k['total'])
			
	else:
		url = "http://dev.jellyfishsurpriseparty.com/polygon/rates/" + country + "/" + '{:%Y-%m-%d}'.format(checkin_date) + "/" + '{:%Y-%m-%d}'.format(checkout_date)
		response = requests.get(url).json()

		for day1 in response:
			data, desc = HotelES().getVenueName(day1['hotelName'])
			if 'images' in data:
				img = data['@giataId'] + ".jpg"
			else:
				img = False
			hotel1 = {'code': day1['hotelCode'], 'name': day1['hotelName'], 'rating':day1['starRating'],'lowrate': day1['minRate'],'img':img,'desc': desc[0]['para']}
			hotel_permutation = { 'hotel1': hotel1, 'total': day1['minRate']}
			hotel_list.append(hotel_permutation)

	assert isinstance(request, HttpRequest)
	return render(
		request,
		'app/results.html',
		context_instance = RequestContext(request,
		{
			'title':'Hotel Splitter - Result',
			'year':datetime.now().year,
			'response': hotel_list,
			'checkout': checkout_date,
			'checkin': checkin_date
		})
	)

def convertdate(datestring):
    #if type(datestring) is date:
    #    return datestring
    try:
        dateobj = datetime.strptime(datestring, '%d %B, %Y').date()
        return dateobj
    except:
        pass

    try:
        dateobj = datetime.strptime(fix_dt(datestring), '%B %d, %Y, %H').date()
        return dateobj
    except:
        raise

def book(request):
	booking=""
	combo_num = request.GET.get("combo#")
	hotel1 = request.GET.get("hotel1")
	hotel2 = request.GET.get("hotel2")
	hotel1img= request.GET.get("hotel1img")
	hotel2img = request.GET.get("hotel2img")
	hotel1rate = request.GET.get("hotel1rate")
	hotel2rate = request.GET.get("hotel2rate")
	total = request.GET.get("total")
	
	print type(hotel1)
	print type(hotel2)

	assert isinstance(request, HttpRequest)
	return render(
		request,
		'app/book.html',
		context_instance = RequestContext(request,
		{
			'title':'Hotel Splitter - Booking',
			'message':'We are working on your reservation',
			'year':datetime.now().year,
			'combo_num': combo_num,
			'hotel1': hotel1,
			'hotel2': hotel2,
			'hotel1img': hotel1img,
			'hotel2img': hotel2img,
			'hotel1rate': hotel1rate,
			'hotel2rate': hotel2rate,
			'total': total
		})
	)