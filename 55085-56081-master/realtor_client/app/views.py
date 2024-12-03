from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.

from . import forms
from django.http import HttpResponseRedirect
from django.urls import reverse


from . import xmlrpc

def login (request):

    if 'name' in request.session and 'key' in request.session and 'id' in request.session:
        return HttpResponseRedirect(reverse('app:appartements'))
    
    if request.method == 'POST' and 'name' in request.POST:
        name = request.POST['name']

        [id, key] = xmlrpc.authentificate(name)

        if key != False and id != False:
            request.session['name'] = name
            request.session['key'] = key
            request.session['id'] = id
            return HttpResponseRedirect(reverse('app:appartements'))
        else:
            context = {
                'error': 'Wrong name',
                'form': forms.LoginForm()
            }
            return render(request, 'app/index.html', context)
    
    context = {
        'error': '',
        'form': forms.LoginForm()
    }
    return render(request, 'app/index.html', context)

    

def register (request):
    if 'key' in request.session and 'name' in request.session and 'id' in request.session:
        return HttpResponseRedirect(reverse('app:appartements'))

    if request.method == 'POST' and 'name' in request.POST:
        name = request.POST['name']

        key = xmlrpc.register(name)
        if key != False:
           

            return HttpResponseRedirect(reverse('app:login'))

        else:
            context = {
                'error': 'Wrong name',
                'form': forms.RegisterForm()
            }
            return render(request, 'app/register.html', context)


    return render(request, 'app/register.html', {'form': forms.RegisterForm()})


def logout (request):
    if 'key' in request.session and 'name' in request.session and 'id' in request.session:
        del request.session['key']
        del request.session['id']
        del request.session['name']
    return HttpResponseRedirect(reverse('app:login'))


def appartements (request):

    if 'name' not in request.session or 'key' not in request.session or 'id' not in request.session:
        return HttpResponseRedirect(reverse('app:login'))


    # check if the user is logged in
    if 'name' in request.session and 'key' in request.session and 'id' in request.session:
        context = {
            'title': 'Appartements',
            'appartements': xmlrpc.searchAppartement(request.session['key']),

        }
        return render(request, 'app/appartements.html', context)
    else:
        context = {
            'error': 'You are not logged in'
        }
        return redirect(request, 'app/index.html', context)


    

def offer (request, appartment_id):

    if 'name' not in request.session or 'key' not in request.session or 'id' not in request.session:
        return HttpResponseRedirect(reverse('app:login'))
   
    context = {
        'title': 'Offer',
        'form': forms.OfferForm(),
        'appartement': xmlrpc.search(appartment_id, request.session['key'])
    }

    return render(request, 'app/offer.html', context)



def make_offer (request, appartment_id):
    
        if request.method == 'POST' and 'price' in request.POST:
            price = request.POST['price']
            res = xmlrpc.makeOffer(appartment_id, request.session['id'], price, request.session['key'] )

            if res == True:
                return HttpResponseRedirect(reverse('app:appartements'))
            else:
                context = {
                    'error': 'The price muste at least 90% of the price of the appartement',
                    'form': forms.OfferForm(),
                    'appartement': xmlrpc.search(appartment_id, request.session['key'])
                }
                return render(request, 'app/offer.html', context)
        else:
            return HttpResponseRedirect(reverse('app:appartements'))

def page404(request, exception):
    return render(request, 'app/404.html')