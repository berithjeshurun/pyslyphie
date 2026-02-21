import json
import threading
import uuid
from typing import Dict, Any
from webview import Window


from .modules.net import (
    sl__net__domrtrace, sl__net__domtrace, sl__net__ping,
    sl__net__lis, sl__net__ip
)

from .modules.ocam import (
    sl__ocam__upind, sl__ocam__add, sl__ocam__get, sl__ocam__len,
    sl__ocam__list, sl__ocam__rsfeed, sl__ocam__for, 
    CAMS_IP
)

from .modules.sstring import (
    sl__string__h2s, sl__string__s2h, sl__string__fcomb,
)

# In-memory module registry (plugins should call register_module)
MODULES: Dict[str, Dict[str, Any]] = {}
JOBS: Dict[str, Dict[str, Any]] = {}  # jobId -> {status, out, error}

def register_module(name: str, schema: dict, handler_map: dict):
    """
    schema: {desc: str, commands: {cmd: {desc}}}
    handler_map: { "submodule?": { "command": callable(args)->result_or_stream } }
    """
    MODULES[name] = {"schema": schema, "handlers": handler_map}

def list_modules():
    meta = {name: mod["schema"] for name, mod in MODULES.items()}
    return meta

def _run_job(job_id: str, func, *args, **kwargs):
    JOBS[job_id]["status"] = "running"
    try:
        res = func(*args, **kwargs)
        JOBS[job_id]["status"] = "done"
        JOBS[job_id]["out"] = res
    except Exception as e:
        JOBS[job_id]["status"] = "error"
        JOBS[job_id]["error"] = f"{type(e).__name__}: {e}"

def exec_module_cmd(module: str, command: str, args_json: str, js : Window):
    """
    Called synchronously from JS, but we return quickly with job id and spawn thread for heavy tasks.
    args_json is JSON string array of args.
    """
    try:
        args = json.loads(args_json)
    except:
        args = []

    mod = MODULES.get(module)
    if not mod:
        return {"error": f"Module not found: {module}"}

    handler = mod["handlers"].get(command)
    if not handler:
        return {"error": f"Command not found: {command} in {module}"}

    job_id = str(uuid.uuid4())
    JOBS[job_id] = {"status": "queued", "out": None, "error": None, "module": module, "command": command}
    t = threading.Thread(target=_run_job, args=(job_id, handler, args), daemon=True, kwargs={'js' : js})
    t.start()
    return {"job_id": job_id, "status": "queued"}

def get_job(job_id):
    j = JOBS.get(job_id)
    if not j:
        return {"error": "job not found"}
    return j

def ping_handler(args):
    host = args[0] if args else "8.8.8.8"
    return f"PONG: {host}"

register_module(
    "net",
    {   "desc": "Network utilities", 
        "commands": {
            "ping": {"desc": "Ping host"}, 
            "domtrace": {"desc": "Trace Domain route"}, 
            "domrtrace": {"desc": "Reverse-Trace Domain route"},
            "tcp" : {"desc" : "Runs a tcp scan"},
            "ip"  : {"desc" : "Get the details of the IP"}
        }
    },
    {
        "ping": sl__net__ping, 
        "domtrace": sl__net__domtrace, 
        "domrtrace" : sl__net__domrtrace,
        "tcp" : sl__net__lis,
        "ip"  : sl__net__ip,
    }
)

register_module(
    "ocam",
    {   "desc": "Gets Open access to World-wide cameras", 
        "commands": {
            "update": {"desc": "Updates the indexs"}, 
            "add": {"desc": "Adds a OpenCamera-URL"}, 
            "get": {"desc": "Fetches an image from the args"},
            "len" : {"desc" : "Gets the available cams"},
            "list"  : {"desc" : "Lists out the available cams"},
            'feed' : {'desc' : "Feeds Camera to a Monitor"},
            'for' : {'desc' : "Gets Specific list"},

        }
    },
    {
        "update": sl__ocam__upind, 
        "add": sl__ocam__add, 
        "get" : sl__ocam__get,
        "len" : sl__ocam__len,
        "list"  : sl__ocam__list,
        'feed' : sl__ocam__rsfeed,
        'for'  : sl__ocam__for,
    }
)

register_module(
    "string",
    {   "desc": "String utilities", 
        "commands": {
            "h2s": {"desc": "Hex to string"}, 
            "s2h": {"desc": "String to Hex"}, 
            "fco": {"desc" : "All possible Combinations of a word"}
        }
    },
    {
        "h2s": sl__string__h2s, 
        "s2h": sl__string__s2h,
        "fco": sl__string__fcomb
    }
)
