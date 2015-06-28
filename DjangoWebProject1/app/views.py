"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime, date, timedelta
import requests
from app.models import HotelES

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
            'message':'Your contact page.',
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
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )

def book(request):
    """Renders the booking page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/book.html',
        context_instance = RequestContext(request,
        {
            'title':'Reservation',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )

def result(request):
	"""Get the result"""
	es = HotelES()
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
		print len(response[0])
		print len(response[1])
		i = 0
		for day1 in response[0]:
			if i == 10:
				break
			i+=1
			data, desc = es.queryName(day1['hotelName'])
			if "images" in data:
				img = data["@giataId"] + ".jpg"
			else:
				img = False
			hotel1 = {'id': day1['hotelCode'],'name': day1['hotelName'].lower().title(), 'lowrate': day1['minRate'], 'rating': day1['starRating'], 'img': img, 'desc': desc[0]['para']}
			j=0
			for day2 in response[1]:
				if j==10:
					break
				j+=1
				data, desc = es.queryName(day2['hotelName'])
				if "images" in data:
					img = data["@giataId"] + ".jpg"
				else:
					img = False
				hotel2 = {'id': day2['hotelCode'], 'name': day2['hotelName'].lower().title(), 'lowrate': day2['minRate'], 'rating': day1['starRating'], 'img': img, 'desc': desc[0]['para']}
				hotel_permutation = { 'hotel1': hotel1, 'hotel2': hotel2, 'total': day1['minRate'] + day2['minRate']}
				hotel_list.append(hotel_permutation)
			
	else:
		url = "http://dev.jellyfishsurpriseparty.com/polygon/rates/" + country + "/" + '{:%Y-%m-%d}'.format(checkin_date) + "/" + '{:%Y-%m-%d}'.format(checkout_date)
		response = requests.get(url).json()

		for day1 in response:
			data, desc = es.queryName(day2['hotelName'])
			if "images" in data:
				img = data["@giataId"] + ".jpg"
			else:
				img = False
			hotel1 = {'id': day1['hotelCode'],'name': day1['hotelName'].lower().title(), 'lowrate': day1['minRate'], 'rating': day1['starRating'], 'img': img, 'desc': desc[0]['para']}
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
			'response': hotel_list
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