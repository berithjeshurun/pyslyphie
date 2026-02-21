import requests
import base64, random
from typing import Literal
from bs4 import BeautifulSoup
import os
import sys
import io
import contextlib
import traceback
from typing import Union, List, Optional


def encode_image(file_path : str) -> str | bool :
    try :
        with open("image.png", "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_image
    except :
        return False
    
class ContextUpdater:
    def __init__(self, url, _type='sender'):
        self.url = url
        self.session = requests.Session()
        self._type = _type 

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._type == 'sender':
            self.update({'mode': 'SYLPH.END'})

    def update(self, data: dict):
        if self.url is None:
            return
        try:
            self.session.post(self.url, json=data, timeout=1)
        except Exception as e:
            print(f"[ContextUpdater] Failed to send log: {e}")

    def receive(self):
        if self.url is None:
            return
        try:
            response = self.session.get(self.url, timeout=1)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[ContextUpdater] Failed to receive log: {e}")
            return None

    def terminate(self):
        self.update({'mode': 'SYLPH.GEN'})



class Streamer :
    def __init__(self, addr : str, mode : Literal['get', 'post'], **kwargs):
        super().__init__()

        self.__adr = addr
        self.__headers : list[str] = list()
        self.__kwargs = kwargs
        self.__parser = None

    def __enter__(self) : 
        if self.__kwargs.get('skip_prev', None) != None :
            return
        try :
            r = requests.get(self.__adr)
            print(r.status_code)
        except Exception as e :
            print ('[ERROR] : ', e)
        return self
    
    def __exit__(self, *args, **kwargs) : 
        pass

    def pushHeader(self, header) :
        if isinstance(header, list) :
            self.__headers.extend(header)
        else :
            if isinstance(header, str) :
                self.__headers.append(header)

    def post(self, data : dict = dict()) :
        try :
            self.__parser = requests.post(self.__adr, data=data, headers=self.__headers if len(self.__headers) != 0 else None)
        except Exception as e :
            print (e)

    @property
    def r(self) :
        return self.__parser

    @r.setter
    def r(self, parser : requests.Response) :
        try :self.__parser = parser
        except : pass





class WebScraper:
    def __init__(self):
        self.soup = None

    def fetch(self, url: str):
        """
        Fetches the HTML content of the specified URL.
        """
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.soup = BeautifulSoup(response.text, 'html.parser')
            else:
                print(f"Failed to retrieve content. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching the URL: {e}")


    @property
    def s(self) : return self.soup


    @s.setter
    def s(self, html : str) :
        self.soup = BeautifulSoup(html, 'html.parser')

    # --- 22 Functions ---

    def getLinks(self) -> list:
        """Returns all URLs from the page's <a> tags."""
        return [link['href'] for link in self.soup.find_all('a', href=True)] if self.soup else []

    def getScripts(self) -> list:
        """Returns all the script sources from the page."""
        return [script['src'] for script in self.soup.find_all('script', src=True)] if self.soup else []

    def getCss(self) -> list:
        """Returns all the CSS link sources from the page."""
        return [link['href'] for link in self.soup.find_all('link', rel='stylesheet', href=True)] if self.soup else []

    def getImages(self) -> list:
        """Returns all the image sources from the page."""
        return [img['src'] for img in self.soup.find_all('img', src=True)] if self.soup else []

    def getIframes(self) -> list:
        """Returns all iframe sources from the page."""
        return [iframe['src'] for iframe in self.soup.find_all('iframe', src=True)] if self.soup else []

    def getVideos(self) -> list:
        """Returns all video sources (video and iframe) from the page."""
        video_sources = [video['src'] for video in self.soup.find_all('video', src=True)] if self.soup else []
        iframe_videos = [iframe['src'] for iframe in self.soup.find_all('iframe', src=True) if 'youtube' in iframe['src'] or 'vimeo' in iframe['src']]
        return video_sources + iframe_videos

    def getMetaTags(self) -> dict:
        """Returns all meta tags from the page."""
        return {meta['name']: meta.get('content', '') for meta in self.soup.find_all('meta', attrs={'name': True})} if self.soup else {}

    def getHeaders(self) -> dict:
        """Returns all header tags (h1-h6) from the page."""
        headers = {}
        if self.soup:
            for i in range(1, 7):
                headers[f"h{i}"] = [header.get_text() for header in self.soup.find_all(f"h{i}")]
        return headers

    def getForms(self) -> list:
        """Returns all form action URLs from the page."""
        return [form['action'] for form in self.soup.find_all('form', action=True)] if self.soup else []

    def getParagraphs(self) -> list:
        """Returns all paragraphs from the page."""
        return [p.get_text() for p in self.soup.find_all('p')] if self.soup else []

    def getTables(self) -> list:
        """Returns all tables from the page."""
        return [str(table) for table in self.soup.find_all('table')] if self.soup else []

    def getInternalLinks(self, base_url: str) -> list:
        """Returns internal links relative to the base URL."""
        return [link['href'] for link in self.soup.find_all('a', href=True) if link['href'].startswith(base_url)] if self.soup else []

    def getExternalLinks(self, base_url: str) -> list:
        """Returns external links not related to the base URL."""
        return [link['href'] for link in self.soup.find_all('a', href=True) if not link['href'].startswith(base_url)] if self.soup else []

    def getKeywords(self) -> str:
        """Returns the keywords meta tag content."""
        keywords = self.soup.find('meta', attrs={'name': 'keywords'}) if self.soup else None
        return keywords['content'] if keywords else 'No keywords meta tag'

    def getDescription(self) -> str:
        """Returns the description meta tag content."""
        description = self.soup.find('meta', attrs={'name': 'description'}) if self.soup else None
        return description['content'] if description else 'No description meta tag'

    def getElementsByClass(self, class_name: str) -> list:
        """Finds and returns all elements with the specified class name."""
        return self.soup.find_all(class_=class_name) if self.soup else []

    def getElementById(self, element_id: str):
        """Finds and returns the element with the specified id."""
        return self.soup.find(id=element_id) if self.soup else None

    def getElementsByTag(self, tag_name: str) -> list:
        """Finds and returns all elements with the specified tag name."""
        return self.soup.find_all(tag_name) if self.soup else []

    def getFormInputs(self) -> list:
        """Returns all input fields from forms on the page."""
        return [(input_tag.get('name'), input_tag.get('type')) for input_tag in self.soup.find_all('input')] if self.soup else []

    def getLinksWithText(self) -> dict:
        """Returns a dictionary with link URLs as keys and their text as values."""
        return {link['href']: link.get_text() for link in self.soup.find_all('a', href=True)} if self.soup else {}

    def getInlineStyles(self) -> list:
        """Returns all inline style tags on the page."""
        return [style.get_text() for style in self.soup.find_all('style')] if self.soup else []

    def getClasses(self) -> dict:
        """Returns a dictionary of class names and their occurrence counts."""
        classes = {}
        if self.soup:
            for tag in self.soup.find_all(class_=True):
                for class_name in tag.get('class', []):
                    classes[class_name] = classes.get(class_name, 0) + 1
        return classes

    # --- 15 Properties ---

    @property
    def title(self) -> str:
        """Returns the title of the page."""
        return self.soup.title.string if self.soup and self.soup.title else 'No title'

    @property
    def favicon(self) -> str:
        """Returns the favicon URL if available."""
        icon_link = self.soup.find('link', rel='icon') if self.soup else None
        return icon_link['href'] if icon_link else 'No favicon'

    @property
    def charset(self) -> str:
        """Returns the charset meta tag of the page."""
        charset = self.soup.find('meta', charset=True) if self.soup else None
        return charset['charset'] if charset else 'Charset not defined'

    @property
    def doctype(self) -> str:
        """Returns the doctype of the page."""
        return next((item for item in self.soup.contents if isinstance(item, BeautifulSoup.Doctype)), 'No doctype') if self.soup else 'No doctype'

    @property
    def links(self) -> list:
        """Returns all links from the page."""
        return self.getLinks()

    @property
    def scripts(self) -> list:
        """Returns all script tags."""
        return self.getScripts()

    @property
    def css(self) -> list:
        """Returns all CSS links."""
        return self.getCss()

    @property
    def images(self) -> list:
        """Returns all image tags."""
        return self.getImages()

    @property
    def iframes(self) -> list:
        """Returns all iframe tags."""
        return self.getIframes()

    @property
    def videos(self) -> list:
        """Returns all video tags."""
        return self.getVideos()

    @property
    def metaTags(self) -> dict:
        """Returns all meta tags."""
        return self.getMetaTags()

    @property
    def headers(self) -> dict:
        """Returns all headers."""
        return self.getHeaders()

    @property
    def forms(self) -> list:
        """Returns all form actions."""
        return self.getForms()

    @property
    def paragraphs(self) -> list:
        """Returns all paragraph tags."""
        return self.getParagraphs()

    @property
    def tables(self) -> list:
        """Returns all tables."""
        return self.getTables()

    @property
    def internalLinks(self) -> list:
        """Returns all internal links."""
        return self.getInternalLinks(self.soup.find('base')['href'] if self.soup and self.soup.find('base') else '')

    @property
    def externalLinks(self) -> list:
        """Returns all external links."""
        return self.getExternalLinks(self.soup.find('base')['href'] if self.soup and self.soup.find('base') else '')

    @property
    def keywords(self) -> str:
        """Returns the keywords meta tag content."""
        return self.getKeywords()

    @property
    def description(self) -> str:
        """Returns the description meta tag content."""
        return self.getDescription()




import inspect
from typing import Any, Dict
import json

def convert_function_to_tool_manual(func: callable) -> Dict[str, Any]:
    """
    Converts a Python function with Google-style docstring
    into a JSON schema representation for tool calling.
    """
    # Get function signature
    sig = inspect.signature(func)
    params_schema = {}

    # Extract docstring
    doc = inspect.getdoc(func) or ""
    doc_lines = doc.splitlines()
    
    # Attempt to parse arg descriptions from Google-style docstring
    arg_docs = {}
    for line in doc_lines:
        line = line.strip()
        if line.startswith("Args:"):
            # Parse lines like "a: first number"
            for arg_line in doc_lines[doc_lines.index(line)+1:]:
                if not arg_line.strip():
                    break
                if ':' in arg_line:
                    name, desc = arg_line.strip().split(':', 1)
                    arg_docs[name.strip()] = desc.strip()
            break

    # Build parameters schema
    for name, param in sig.parameters.items():
        annotation = str(param.annotation) if param.annotation != inspect._empty else "string"
        param_desc = arg_docs.get(name, "")
        params_schema[name] = {
            "type": annotation,
            "description": param_desc
        }

    # Build final tool JSON
    tool_json = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": doc_lines[0] if doc_lines else "",
            "parameters": {
                "type": "object",
                "properties": params_schema,
                "required": list(sig.parameters.keys())
            }
        }
    }

    return tool_json

# ------------------------------
# Example usage
def add_two_numbers(a: int, b: int) -> int:
    """
    Add two numbers together.

    Args:
        a: First number to add
        b: Second number to add

    Returns:
        int: Sum of a and b
    """
    return a + b



class PythonSandbox:
    """
    A sandbox environment to execute Python code (str or list of str)
    with output capture, export capabilities, and a shared directory 
    'mnt/data' for saving or running code files.
    """

    def __init__(self, data_dir: str = "mnt/data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.shared_globals = {
            "__builtins__": {
                "print": print,
                "range": range,
                "len": len,
                "int": int,
                "float": float,
                "str": str,
                "list": list,
                "dict": dict,
                "set": set,
                "abs": abs,
                "__import__": __import__,               
            }
        }
        self.last_output = ""
        self.last_result = None

    @contextlib.contextmanager
    def capture_output(self):
        """Context manager to capture stdout and stderr."""
        new_out, new_err = io.StringIO(), io.StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = new_out, new_err
        try:
            yield new_out, new_err
        finally:
            sys.stdout, sys.stderr = old_out, old_err

    def execute(
        self, 
        code: Union[str, List[str]], 
        filename: Optional[str] = None,
        export: bool = False
    ) -> dict:
        """
        Executes the given Python code in the sandbox environment.

        Parameters:
        - code: str or list of str - Python code to execute.
        - filename: Optional[str] - save the code to this file inside the shared directory.
        - export: bool - if True, saves the code to a .py file in the shared directory.

        Returns:
        - dict with keys:
          - "success": bool - if execution succeeded,
          - "output": str - captured stdout and stderr,
          - "result": any - last expression result or None,
          - "error": str or None - error traceback if exception raised,
          - "filepath": str or None - path of saved file if export is True or filename given,
        """
        if isinstance(code, list):
            code_str = "\n".join(code)
        else:
            code_str = code

        filepath = None
        if filename:
            filepath = os.path.join(self.data_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code_str)
        elif export:
            filepath = os.path.join(self.data_dir, "exported_code.py")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code_str)

        # Prepare execution environment
        local_env = {}

        with self.capture_output() as (out, err):
            try:
                # Compile the code first to check syntax and get code object
                code_obj = compile(code_str, filename or "<string>", "exec")
                exec(code_obj, self.shared_globals, local_env)

                # Optionally capture last expression value if code is single expression
                # Here just None as exec does not return value
                self.last_result = None

                # Success
                output = out.getvalue() + err.getvalue()
                self.last_output = output
                return {
                    "success": True,
                    "output": output,
                    "result": self.last_result,
                    "error": None,
                    "filepath": filepath,
                }
            except Exception as e:
                tb = traceback.format_exc()
                output = out.getvalue() + err.getvalue()
                self.last_output = output
                return {
                    "success": False,
                    "output": output,
                    "result": None,
                    "error": tb,
                    "filepath": filepath,
                }

    def get_last_output(self) -> str:
        """Returns the last captured output from executed code."""
        return self.last_output

    def save_code(self, code: Union[str, List[str]], filename: str) -> str:
        """
        Saves given code to a file in the shared directory.

        Returns saved file path.
        """
        if isinstance(code, list):
            code_str = "\n".join(code)
        else:
            code_str = code

        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code_str)
        return filepath


# sandbox = PythonSandbox()
# sandbox.shared_globals["__builtins__"]["__import__"] = __import__  # Allow imports
