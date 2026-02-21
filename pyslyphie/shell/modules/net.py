import socket
import subprocess
import csv
import io
import html, requests

def ps_csv_to_html(powershell_code: str) -> str:
    """
    Runs a PowerShell command that outputs CSV data, 
    then converts that CSV into an HTML table string.
    """
    result = subprocess.run(
        ["powershell", "-Command", powershell_code],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    if result.returncode != 0:
        raise RuntimeError(f"PowerShell error:\n{result.stderr.strip()}")

    csv_data = result.stdout.strip()
    if not csv_data:
        return "<p><em>No data returned.</em></p>"

    reader = csv.DictReader(io.StringIO(csv_data))
    rows = list(reader)
    if not rows:
        return "<p><em>No rows found.</em></p>"
    headers = rows[0].keys()
    html_rows = [
        "<table border='1' style='border-collapse:collapse;'>",
        "<thead><tr>" + "".join(f"<th>{html.escape(h)}</th>" for h in headers) + "</tr></thead>",
        "<tbody>"
    ]
    for row in rows:
        html_rows.append("<tr>" + "".join(f"<td>{html.escape(str(row[h]))}</td>" for h in headers) + "</tr>")

    html_rows.append("</tbody></table>")

    return "\n".join(html_rows)

def json_to_html_table(data: dict) -> str:
    """
    Convert a flat JSON/dict into an HTML table.
    
    Args:
        data (dict): Flat dictionary to convert.
        
    Returns:
        str: HTML table as a string.
    """
    html = '<table border="1" cellspacing="0" cellpadding="5">\n'
    html += '  <thead><tr><th>Key</th><th>Value</th></tr></thead>\n<tbody>\n'
    
    for key, value in data.items():
        html += f'  <tr><td>{key}</td><td>{value}</td></tr>\n'
    
    html += '</tbody>\n</table>'
    return html


def verifiy(args) : return len(args) != 0

def sl__net__ping(args, **kwargs) :
    host = args[0] if args else "8.8.8.8"
    return f"PONG: {host}"

def sl__net__domtrace(args, **kwargs) :
    if verifiy(args) :
        host = str(args[0])
        if host.startswith('www.') and not host.startswith('http') :
            try:
                return socket.gethostbyname(host)
            except Exception as e :
                return f"<p>[-] Could not resolve domain information for : {host} due to {e}</p>"
    return '<p style="color : red !important;">[-] Expected atleast 1 argument, got 0</p>'


def sl__net__domrtrace(args, **kwargs) :
    if verifiy(args) :
        host = str(args[0])
        try :
            host_info = socket.gethostbyaddr(host)
            hostname = host_info[0]
            aliases = host_info[1]
            addresses = host_info[2]

            html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Host Info for {host}</title>
                </head>
                <body>
                    <h2>Host Information</h2>
                    <table border="1">
                        <tr>
                            <th>Field</th>
                            <th>Value</th>
                        </tr>
                        <tr>
                            <td>IP Address</td>
                            <td>{host}</td>
                        </tr>
                        <tr>
                            <td>Hostname</td>
                            <td>{hostname}</td>
                        </tr>
                        <tr>
                            <td>Aliases</td>
                            <td>{', '.join(aliases) if aliases else 'None'}</td>
                        </tr>
                        <tr>
                            <td>Resolved Addresses</td>
                            <td>{', '.join(addresses)}</td>
                        </tr>
                    </table>
                </body>
                </html>
                """
            return html.strip()
        except Exception as e :
                return f"<p>[-] Could not resolve domain information for : {host} due to {e}</p>"
    return '<p style="color : red !important;">[-] Expected atleast 1 argument, got 0</p>'
        

def sl__net__lis(args, **kwargs) :
    if verifiy(args) :
        _type = str(args[0])
        if _type == 'run' :
            if len(args) > 1 :
                if args[1] == '--filter' :
                    return ps_csv_to_html('Get-NetTCPConnection | Select LocalAddress, LocalPort, RemoteAddress, RemotePort, State | ConvertTo-Csv -NoTypeInformation')
            return ps_csv_to_html("Get-NetTCPConnection | ConvertTo-Csv -NoTypeInformation")
    return '<p style="color : red !important;">[-] Expected atleast 1 argument, got 0</p>'
    

def sl__net__ip(args, **kwargs) :
    if verifiy(args) :
        ip = str(args[0])
        try :
            parser = requests.get(f'https://ipwhois.app/json/{ip}')
            if parser.status_code == 200 :
                return json_to_html_table(parser.json())
            else :
                return f"<p>[-] UnExpected Error : {parser.text or parser.json()} </p>"
        except Exception as e :
            return f"<p>[-] Could not resolve IP information for : {ip} due to {e}</p>"
    return '<p style="color : red !important;">[-] Expected atleast 1 argument, got 0</p>'
    