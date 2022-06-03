from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login as auth_log
from django.contrib.auth.decorators import login_required

import sqlite3
import urllib.request


#--------------------------------------------------------------------------------------
@login_required
@csrf_exempt #Flaw 1: A01:2021 - Broken access control. This wrapper should be removed for CSRF to work and protect properly.
def mainpage(request):

#Flaw 2: A03:2021 - Injection. You can try SQL insert, for example http://127.0.0.1:8000/poracleX/index/?id=%22Robocod%22%20--
#which will comment out the secrecy=0 required to reveal non-secret agent
    try:
        id = request.GET.get("id")
        conn = sqlite3.connect('agents.sqlite')
        cursor = conn.cursor()
        agent=list(cursor.execute("select name from Agent where id="+str(id)+" and secrecy=0"))
        return HttpResponse(agent)
    
#Prepared statement to fix the injection flaw
        #id = request.GET.get("id")
        #id=id.replace("'","").replace('"','')
        #conn = sqlite3.connect('agents.sqlite')
        #cursor = conn.cursor()
        #query = "select name from Agent where id=? and secrecy=0"
        #agent=list(cursor.execute(query,(id,)))
        #return HttpResponse(agent)
  
    except: 
        
        return render(request,'poracleX/index.html',{})

#---------------------------------------------------------------------------------------
# Flaw 3: A10:2021 - Server Side Request Forgery (SSRF)
# You can for example make secret.txt file to c:/Users/Public and use 
# #http://127.0.0.1:8000/poracleX/index/ssrf/?url=%22file:c:/Users/Public/secret.txt%22
# to access this file
@login_required
def get_ssrf(request):
    url = str(request.GET.get("url")).replace('"',"")
    page = urllib.request.urlopen(url).read()
# Fix for SSRF in this case is to allow only certain sites and/or domains. In this fix only wikipedia is allowed.
    #if url[0:25]!="https://en.wikipedia.org/":
    #    return HttpResponse("Nope")
    #else:
    #    return HttpResponse(page)
    return HttpResponse(page)

#-----------------------------------------------------------------------------------------
#Flaw 4: A04:2021 – Insecure design
#Uses knowledge based answers which needs to be avoided. Anyone can know the answers.

@login_required
def get_identification(request):

    #def make_a_phone_call():
    #    pass
    
    bond = request.POST.get('bond','')
    pentagon=request.POST.get('pentagon')
    phone=request.POST.get('phone')
    if bond=="007" and pentagon=="5" and phone=="020202":
        password_of_the_day="KernelTrap"
    else:
        password_of_the_day="Sorry. You have provided insufficient information."
    return render(request,"poracleX/password.html", {"password":password_of_the_day})

# Can be fixed by stronger authentication. In this case questions can be changed to less general ones and a phone call is
# made. The code for phone call is not written but by some googling this is possible.
    #if bond=="007" and pentagon=="5" and phone=="020202":
    #    password_of_the_day="We will call you to reveal the password. Please answer after agreed time of seconds."
    #    make_a_phone_call()
    #else:
    #    password_of_the_day="Sorry. You have provided insufficient information."

    #return HttpResponse(password_of_the_day)

#--------------------------------------------------------------------------------------------------------
def login(request):
# Flaw 5: A05:2021 - Security Misconfiguration
# There is a test phase account username=tester, password=testertester still enabled with full priviledges. This should be disabled by the administrator.
  
    username=request.POST.get('username','')
    password=request.POST.get('password','')
    user=authenticate(username=username,password=password)
    if user is not None:
        auth_log(request,user)
        return redirect('mainpage',permanent=True)
    else:
        return render(request,'poracleX/login.html',{})

            



    