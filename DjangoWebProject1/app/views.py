"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime, date, timedelta
import requests

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
		for day1 in response[0]:
			#print day1
			hotel1 = {'code': day1['hotelCode'], 'lowrate': day1['minRate']}
			for day2 in response[1]:
				hotel2 = {'code': day2['hotelCode'], 'lowrate': day2['minRate']}
				hotel_permutation = { 'hotel1': hotel1, 'hotel2': hotel2, 'total': day1['minRate'] + day2['minRate']}
				hotel_list.append(hotel_permutation)
			
	else:
		url = "http://dev.jellyfishsurpriseparty.com/polygon/rates/" + country + "/" + '{:%Y-%m-%d}'.format(checkin_date) + "/" + '{:%Y-%m-%d}'.format(checkout_date)
		response = requests.get(url).json()

		for day1 in response:
			hotel1 = {'code': day1['hotelCode'], 'lowrate': day1['minRate']}
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