apis = {"PRIMARY":'', "SECONDARY":'', 
        "BACK-UP":'', "SERVER-ONE":'',
        "BOT":'DEMO_KEY', "EXTERNAL":None}



import requests
from ._utils import generateHeaders, VAR_HEADER_TYPE, VAR_USRAGNT_TYPE

SERVER : str = ''

def sl__lsat4__server(args, **kwargs) :
    if args[0] in apis :
        SERVER = apis[args[0]]
        return '<p> [+] Server Changed </p>'
    return '<p color="red"> [-] No Specific Server Found ! </p>'

def sl__lsat4__lisserve(args, **kwargs) :
    s = 'Servers Available\n'
    _ = len(s)
    s = s+'='*_
    for key in apis :
        s = s + key + "\n"
    
    s = s + "="*_
    s = s + f"Total Server Count : {len(apis)}"
    return s

def sl__lsat4__neoR(args, **kwargs):
    """
    Get details of a specific Near Earth Object (NEO) by neo reference id.
    args: [neo_reference_id]
    kwargs: api_key="your_key"
    """
    api_key = kwargs.get("api_key")
    neo_reference_id = args[0]
    URL = f"https://api.nasa.gov/neo/rest/v1/neo/{neo_reference_id}?api_key={api_key}"
    resp = requests.get(URL)
    resp.raise_for_status()
    return resp.json()

def sl__lsat4__lsat4__neoR_feed(args, **kwargs):
    """
    Get NEO feed for a date range.
    args: [start_date, end_date]
    kwargs: api_key="your_key"
    """
    api_key = kwargs.get("api_key")
    start_date, end_date = args
    URL = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}"
    resp = requests.get(URL)
    resp.raise_for_status()
    return resp.json()

def sl__lsat4__cmenor(args, **kwargs):
    """
    Get Coronal Mass Ejection (CME) events.
    args: [startDate, endDate]
    kwargs: api_key="your_key"
    """
    api_key = kwargs.get("api_key")
    start_date, end_date = args
    URL = f"https://api.nasa.gov/DONKI/CME?startDate={start_date}&endDate={end_date}&api_key={api_key}"
    resp = requests.get(URL)
    resp.raise_for_status()
    return resp.json()

def sl__lsat4__gst(args, **kwargs):
    api_key = kwargs.get("api_key")
    start_date, end_date = args
    URL = f"https://api.nasa.gov/DONKI/GST?startDate={start_date}&endDate={end_date}&api_key={api_key}"
    resp = requests.get(URL)
    resp.raise_for_status()
    return resp.json()

def sl__lsat4__ips(args, **kwargs):
    api_key = kwargs.get("api_key")
    start_date, end_date = args
    URL = f"https://api.nasa.gov/DONKI/IPS?startDate={start_date}&endDate={end_date}&api_key={api_key}"
    resp = requests.get(URL)
    resp.raise_for_status()
    return resp.json()

def sl__lsat4__flr(args, **kwargs):
    api_key = kwargs.get("api_key")
    start_date, end_date = args
    URL = f"https://api.nasa.gov/DONKI/FLR?startDate={start_date}&endDate={end_date}&api_key={api_key}"
    resp = requests.get(URL)
    resp.raise_for_status()
    return resp.json()

def sl__lsat4__sep(args, **kwargs):
    api_key = kwargs.get("api_key")
    start_date, end_date = args
    URL = f"https://api.nasa.gov/DONKI/SEP?startDate={start_date}&endDate={end_date}&api_key={api_key}"
    resp = requests.get(URL)
    resp.raise_for_status()
    return resp.json()

def sl__lsat4__mpc(args, **kwargs):
    api_key = kwargs.get("api_key")
    start_date, end_date = args
    URL = f"https://api.nasa.gov/DONKI/MPC?startDate={start_date}&endDate={end_date}&api_key={api_key}"
    resp = requests.get(URL)
    resp.raise_for_status()
    return resp.json()

def sl__lsat4__rbe(args, **kwargs):
    api_key = kwargs.get("api_key")
    start_date, end_date = args
    URL = f"https://api.nasa.gov/DONKI/RBE?startDate={start_date}&endDate={end_date}&api_key={api_key}"
    resp = requests.get(URL)
    resp.raise_for_status()
    return resp.json()

def sl__lsat4__hss(args, **kwargs):
    api_key = kwargs.get("api_key")
    start_date, end_date = args
    URL = f"https://api.nasa.gov/DONKI/HSS?startDate={start_date}&endDate={end_date}&api_key={api_key}"
    resp = requests.get(URL)
    resp.raise_for_status()
    return resp.json()

def sl__lsat4__wse(args, **kwargs):
    api_key = kwargs.get("api_key")
    start_date, end_date = args
    URL = f"https://api.nasa.gov/DONKI/WSAEnlilSimulations?startDate={start_date}&endDate={end_date}&api_key={api_key}"
    resp = requests.get(URL)
    resp.raise_for_status()
    return resp.json()

def sl__lsat4__epic(args, **kwargs):
    """
    Get EPIC natural color images from date.
    args: [date]
    kwargs: api_key="your_key"
    """
    api_key = kwargs.get("api_key")
    date = args[0]
    URL = f"https://api.nasa.gov/EPIC/api/natural/date/{date}?api_key={api_key}"
    resp = requests.get(URL, headers=generateHeaders())
    resp.raise_for_status()
    return resp.json()


