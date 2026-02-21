import requests
from webview import Window

CAMS_IP : dict[str, str] = {
    'Tokyo, Japan (0)' : 'http://220.254.72.200/cgi-bin/camera?resolution=640&quality=1&page=1762458770015&Language=0',
    'Tokyo, Japan (1)' : 'http://115.179.100.76:8080/SnapshotJPEG?Resolution=640x480&Quality=Standard&View=Normal&Count=1056729669',
    'Tokyo, Japan (2)' : 'http://210.248.127.20/SnapshotJPEG?Resolution=640x480&Quality=Standard&View=Normal&Count=1323000406',
    'Tokyo, Japan (3)' : 'http://210.248.127.21/SnapshotJPEG?Resolution=640x480&Quality=Standard&View=Normal&Count=1323123051',
    "Tokyo, Japan (4)" : "http://220.254.72.199:80/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;1762464013",
    "Tokyo, Japan (5)" : "http://219.127.113.137:80/SnapshotJPEG?Resolution=640x480&amp;Quality=Clarity&amp;1762464062",
    'Unknown, Japan (0)' : 'http://219.121.33.21/SnapshotJPEG?Resolution=640x480&amp;Quality=Clarity&amp;1762459810',
    'Tsu, Japan (0)' : 'http://113.20.245.211:8080/SnapshotJPEG?Resolution=640x480&amp;Quality=Clarity&amp;1762460401',
    'Machida, Japan (0)' : 'http://221.189.0.181:80/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER',
    'Kasugai, Japan (0)' : 'http://183.77.121.171:8081/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;1762460576',
    'Liyama, Japan (0)' : 'http://220.254.144.230:50000/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;1762460638',
    'Nakatsugawa, Japan (0)' : 'http://124.143.25.100:80/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000',
    'Kumamoto, Japan (0)' : 'http://210.226.45.57:8082/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER',
    'Kashima, Japan (0)' : "http://125.206.12.113:80/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;1762461726",
    "Saga, Japan (0)" : "http://114.179.127.11:8001/mjpg/video.mjpg",
    "Fukuoka, Japan (0)" : 'http://61.115.73.231:80/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000',
    "Oita, Japan (0)" : 'http://110.5.28.210:82/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;1762461828',
    "Takedamachi, Japan (0)" : "http://202.183.63.202:80/SnapshotJPEG?Resolution=640x480&amp;Quality=Clarity&amp;1762461860",
    "Hofu, Japan (0)" : "http://122.250.5.56:80/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000",
    "Osaka, Japan (0)" : "http://60.33.230.11:80/SnapshotJPEG?Resolution=640x480&amp;Quality=Clarity&amp;1762461934",
    "Okayama, Japan (0)" : "http://119.47.96.204:8001/SnapshotJPEG?Resolution=640x480&amp;Quality=Clarity&amp;1762462011",
    "Yonago, Japan (0)" : "http://14.14.96.175:80/webcapture.jpg?command=snap&channel=1?1762462041",
    "Tanabe, Japan (0)" : "http://218.45.5.89:80/SnapshotJPEG?Resolution=640x480&amp;Quality=Clarity&amp;1762462066",
    "Wakayama, Japan (0)" : "http://27.116.24.154:80/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000",
    "Amagasaki, Japan (0)" : "http://128.22.30.18:80/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;1762462342",
    "Matsubara, Japan (0)" : "http://218.42.253.97:80/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000",
    "Nara, Japan (0)" : "http://220.96.208.216:8082/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;1762462389",
    "Otsu, Japan (0)" : "http://118.22.53.84:50000/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;1762462413",
    "Matsusaka, Japan (0)" : "http://211.125.148.249:81/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;1762462478",
    "Suzuka, Japan (0)" : "http://202.211.86.177:80/SnapshotJPEG?Resolution=640x480&amp;Quality=Clarity&amp;1762462518",
    "Yokkaichi, Japan (0)" : "http://220.157.230.36:80/SnapshotJPEG?Resolution=640x480&amp;Quality=Clarity&amp;1762462569",
    "Nisshin, Japan (0)" : "http://60.45.200.119:80/SnapshotJPEG?Resolution=640x480&amp;Quality=Clarity&amp;1762462635",
    "Toyohashi, Japan (0)" : "http://121.1.176.117:80/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;1762462671",
    "Fukui, Japan (0)" : "http://124.241.28.23:84/SnapshotJPEG?Resolution=640x480&amp;Quality=Clarity&amp;1762462720",
    "Nonoichi, Japan (0)" : "http://180.43.97.69:8080/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000",
    "Kanazawa, Japan (0)" : "http://220.108.89.119:50001/SnapshotJPEG?Resolution=640x480&amp;Quality=Clarity&amp;1762462774",
    "Nanao, Japan (0)" : "http://202.229.254.186:8080/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000",
    "Shizuoka, Japan (0)" : "http://218.40.214.200:50000/SnapshotJPEG?Resolution=640x480&amp;Quality=Clarity&amp;1762462825",
    "Matsumoto, Japan (0)" : "http://219.111.32.220:80/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000",
    "Azumino, Japan (0)" : "http://202.84.49.209:8001/mjpg/video.mjpg",
    "Nagano, Japan (0)" : "http://203.181.0.118:6003/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;1762462950",
    "Kofu, Japan (0)" : "http://106.157.4.56:80/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER",
    "Yamanashi, Japan (0)" : "http://202.174.60.121:80/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000",
    "Fujiyoshida, Japan (0)" : "http://121.58.129.215:80/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000",
    "Hakone, Japan (0)" : "http://153.142.220.112:80/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER",
    "Higashimatsuyama, Japan (0)" : "http://110.4.179.61:80/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000",
    "Oyama, Japan (0)" : "http://61.213.89.122:8084/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000",
    "Utsunomiya, Japan (0)" : "http://183.77.206.186:10000/SnapshotJPEG?Resolution=640x480&amp;Quality=Clarity&amp;1762463282",
    "Tsukuba, Japan (0)" : "http://61.213.123.156:50001/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;1762463308",
    "Koriyama, Japan (0)" : "http://133.43.28.115:80/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000",
    "Shiogama, Japan (0)" : "http://61.115.115.49:8082/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000",
    "Sendai, Japan (0)" : "http://202.208.150.52:50001/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;1762463398",
    "Yamagata, Japan (0)" : "http://153.156.10.95:80/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000",
    "Shibata, Japan (0)" : "http://203.79.59.84:81/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;1762463458",
    "Shirone, Japan (0)" : "http://218.223.38.14:80/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000",
    "Niigata, Japan (0)" : "http://211.12.199.187:86/SnapshotJPEG?Resolution=640x480&amp;Quality=Clarity&amp;1762463507",
    "Meguro-Ku, Japan (0)" : "http://115.179.36.89:80/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000",
    "Shinagawa-Ku, Japan (0)" : "http://153.142.236.94:8080/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000",
    "Kawaguchi, Japan (0)" : "http://110.3.251.62:80/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000",
    "Saga, Japan (0)" : "http://114.179.127.11:8010/mjpg/video.mjpg",
    "Saga, Japan (1)" : "http://114.179.127.11:8001/mjpg/video.mjpg",
    
    
    "Brighton, UK (0)" : "http://82.8.176.137:8081/cgi-bin/viewer/video.jpg",
    
    "Umea, Sweden (0)" : "http://31.12.82.136:80/mjpg/video.mjpg",
    "Mala, Sweden (0)" : "http://80.88.123.97:80/mjpg/video.mjpg",
    "Soderhamn, Sweden (0)" : "http://80.245.224.153:80/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER",
    "Tyreso, Sweden (0)" : "http://194.71.159.8:80/mjpg/video.mjpg",
    "Degerfors, Sweden (0)" : "http://88.84.253.60:80/mjpg/video.mjpg",
    "Stockholm, Sweden (0)" : "http://194.237.150.19:80/mjpg/video.mjpg",
    "Uddevalla, Sweden (0)" : "http://91.195.155.180:80/mjpg/video.mjpg",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    # "" : "",
    "Sydney, Australia (0)" : "http://220.233.144.165:8888/mjpg/video.mjpg",

    'The Hague, Netherlands (0)' : 'http://62.133.72.177:80/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER',
    "Heiloo, Netherlands (0)" : "http://213.124.95.98:8082/mjpg/video.mjpg",
    "Zwolle, Netherlands (0)" : "http://217.100.243.178:10000/mjpg/video.mjpg",
    "Renesse, Netherlands (0)" : "http://217.63.79.153:8081/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER",
    "Heiloo, Netherlands (0)" : "http://213.124.95.98:8080/mjpg/video.mjpg",
    
    
    
    'Saliste, Romania (0)' : 'http://82.77.203.219:8080/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER',
    "Bucharest, Romania (0)" : "http://109.166.169.204:9000/mjpg/video.mjpg",
    "Sibiu, Romania (0)" : "http://86.123.146.146:81/webcapture.jpg?command=snap&channel=1?1762518786",
    "Sibiu, Romania (1)" : "http://86.123.146.147:81/webcapture.jpg?command=snap&channel=1?0",
    "Braila, Romania (0)" : "http://109.97.46.219:8080/cgi-bin/viewer/video.jpg?r=1762519199",
    "Bucharest, Romania (1)" : "http://109.99.208.157:8080/cgi-bin/viewer/video.jpg?r=1762519299",



    "Sai-Noi, Thailand (0)" : "http://182.52.50.152:82/webcapture.jpg?command=snap&channel=1?1762518105",
    "Sai Noi, Thailand (1)" : "http://182.52.50.152:81/webcapture.jpg?command=snap&channel=1?1762518179",


    "Mumbai, India (0)" : "http://125.17.248.94:80/cgi-bin/viewer/video.jpg?r=1762518055",


    'New York, USA (0)' : 'http://166.143.227.69:8000/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000',
    'New York, USA  (1)' : "http://108.41.24.124:80/mjpg/video.mjpg",
    'Mount Laurel, USA (0)' : "http://96.91.239.26:1024/mjpg/video.mjpg",
    'Doylestown, USA (0)' : "http://166.247.77.253:82/mjpg/video.mjpg",
    "Charlotte, USA (0)" : "http://70.60.107.118/jpg/image.jpg?1707779624",
    "Louisville, USA (0)" : "http://74.142.49.38:8001/jpg/image.jpg",


    'Koserow, Germany (0)' : 'http://87.139.153.80:80/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER',
    'Wandlitz, Germany (0)' : 'http://80.153.65.223:80/mjpg/video.mjpg',
    'Berlin, Germany (0)' : 'http://93.241.200.98:83/mjpg/video.mjpg',


    'Barcelona, Spain (0)' : 'http://88.28.202.117:8084/cgi-bin/viewer/video.jpg?r=1762460937',


    
    'Targovishte, Bulgaria (0)' : 'http://109.120.228.129:80/webcapture.jpg?command=snap&channel=1?1762461196',

    'Brienza, Italy (0)' : 'http://185.139.50.106:8080/oneshotimage1?1762461216',

    'Taipei, Taiwan (0)' : 'http://220.135.56.68:83/webcapture.jpg?command=snap&channel=1?1762461259',


    'Meudon, France (0)' : 'http://62.35.32.100:83/jpgmulreq/1/image.jpg?key=1516975535684&lq=1&1762461352',

    'La Chaux-De-Fonds, Switzerland (0)' : 'http://80.83.62.89:80/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER'
}

COU_AVAIL : list[str] = list()
CIT_AVAIL : list[str] = list()

def verifiy(args) : return len(args) != 0


def sl__ocam__upind(args = None, **kwargs):
    """
    Update COU_AVAIL and CIT_AVAIL based on current CAMS_IP keys.
    This rebuilds the lists from CAMS_IP to ensure they are in sync.
    """
    global COU_AVAIL, CIT_AVAIL
    COU_AVAIL = []
    CIT_AVAIL = []

    for key in CAMS_IP:
        try:
            city_part, country_part = key.split(",", 1)
            city = city_part.strip()
            country = country_part.strip().split()[0]

            if country not in COU_AVAIL:
                COU_AVAIL.append(country)
            if city not in CIT_AVAIL:
                CIT_AVAIL.append(city)
        except Exception as e:
            continue

    return f'<p style="color:green !important;">[+] COU_AVAIL and CIT_AVAIL updated. Countries: {len(COU_AVAIL)}, Cities: {len(CIT_AVAIL)}</p>'

def sl__ocam__add(args, **kwargs):
    """Add a new camera to the CAMS_IP dictionary."""
    if verifiy(args) and len(args) >= 4:
        try:
            country = str(args[0]).capitalize()
            city = str(args[1]).capitalize()
            index = f'({args[2]})'
            url = str(args[3])
            key = f"{city}, {country} {index}"
            CAMS_IP[key] = url

            if country not in COU_AVAIL:
                COU_AVAIL.append(country)
            if city not in CIT_AVAIL:
                CIT_AVAIL.append(city)

            return f'<p style="color:green !important;">[+] Camera added: {key}</p>'
        except Exception as e:
            return f'<p style="color:red !important;">[-] Error: {e}</p>'
    return '<p style="color:red !important;">[-] Expected 4 arguments: country, city, index, URL</p>'


def sl__ocam__len(args, **kwargs) :
    return f'<p> Total Cameras : {len(CAMS_IP)}</p>'


def sl__ocam__get(args, **kwargs):
    """Get camera content by key, country, or city."""
    if verifiy(args):
        key_input = str(args[0]).strip()
        
        if ' '.join(args).strip() in CAMS_IP:
            try:
                return str(requests.get(CAMS_IP[' '.join(args).strip()]).content)
            except Exception as e:
                return f'<p style="color:red !important;">[-] Error: {e}</p>'

        elif key_input.capitalize() in COU_AVAIL:
            result = {}
            country = key_input.capitalize()
            for k, url in CAMS_IP.items():
                if k.split(",")[1].strip().split()[0] == country:
                    try:
                        result[k] = str(requests.get(url).content)
                    except:
                        result[k] = None
            return result

        elif key_input.capitalize() in CIT_AVAIL:
            result = {}
            city = key_input.capitalize()
            for k, url in CAMS_IP.items():
                if k.split(",")[0] == city:
                    try:
                        result[k] = str(requests.get(url).content)
                    except:
                        result[k] = None
            return result

        else:
            return f'<p style="color:red !important;">[-] Key/Country/City "{key_input}" not found</p>'
    
    return '<p style="color:red !important;">[-] Expected at least 1 argument, got 0</p>'

def sl__ocam__list(args, **kwargs) :
    s = ''
    for i in CAMS_IP :
        s = s + f'<p>{i}</p>\n'
    return s

def sl__ocam__rsfeed(args, **kwargs):
    if not verifiy(args):
        return '<p style="color:red;">[-] Expected at least 1 argument, got 0</p>'
    
    viewer_name_js = ' '.join(args).strip()

    js_window = kwargs.get('js', None)
    if js_window is None:
        return '<p style="color:red;">[-] Window not provided</p>'


    try:
        js_window.evaluate_js(f'_api_spawn_hooked_viewer("Live RS Feed :: {viewer_name_js}", "{viewer_name_js}")')
        return f'<p style="color:green;">[+] Spawned viewer: {viewer_name_js}</p>'
    except Exception as e:
        return f'<p style="color:red;">[-] Execution error: {e}</p>'

def sl__ocam__for(args, **kwargs) :
    args = list(args)
    if not verifiy(args):
        return '<p style="color:red;">[-] Expected at least 1 argument, got 0</p>'
    s : list[str] = list()
    args = [str(i).lower().strip() for i in args]
    for key in CAMS_IP :
        try :
            cou = key.split(',')[1].strip().split(' ')[0].strip().lower()
            if cou in args :
                s.append(key)
        except : pass

    if len(s) == 0 :
        return f'<p style="color:red;">[-] Nothing found for : {",".join(args)}</p>'
    
    html = f'<h5> Available ({len(s)}) : </h5>'
    _ = len(html)
    html = html + '\n' + "="*_
    for p in s :
        html = html + f'<p> {p} </p>'
    return html

sl__ocam__upind()