import requests
from typing import Optional, List, Dict, Any, Union, Literal

def query_crossref_works(
    query: str,
    filter: Optional[str] = None,
    select: Optional[List[str]] = None,
    rows: int = 20,
    cursor: Optional[str] = None,
    mailto: Optional[str] = None
) -> Dict[str, Any]:
    """
    Query the Crossref REST API /works endpoint.

    Args:
        query: Free text search term.
        filter: Optional filter string, e.g. "type:journal-article,has-orcid:1".
        select: Optional list of fields to return, e.g. ["DOI", "title", "author"].
        rows: Number of results to return (default 20; max up to ~1000 according to docs) :contentReference[oaicite:6]{index=6}
        cursor: Optional cursor string for paging (e.g., "*").
        mailto: Optional email address appended as parameter (for polite usage).

    Returns:
        Parsed JSON response (dict) from the Crossref API.

    Usage :
        >>> if __name__ == "__main__":
        >>> result = query_crossref_works(
        >>>     query="machine learning in physics",
        >>>     filter="type:journal-article,has-orcid:1",
        >>>     select=["DOI", "title", "author", "is-referenced-by-count"],
        >>>     rows=10,
        >>>     mailto="your_email@example.com"
        >>> )
        >>> # Print first item
        >>> items = result.get("message", {}).get("items", [])
        >>> if items:
        >>>     print(items[0])
        >>> else:
        >>>     print("No results found.")
    """
    base_url = "https://api.crossref.org/works"
    params: Dict[str, Any] = {
        "query": query,
        "rows": rows
    }
    if filter:
        params["filter"] = filter
    if select:
        params["select"] = ",".join(select)
    if cursor:
        params["cursor"] = cursor
    if mailto:
        params["mailto"] = mailto

    resp = requests.get(base_url, params=params)
    resp.raise_for_status()
    return resp.json()


class CrossrefAPI:
    """
    `Python wrapper for the Crossref REST API.`

    #### Usage : 
    >>> if __name__ == "__main__":
    >>>     api = CrossrefAPI(mailto="your_email@example.com")

    >>>     # Query works
    >>>     result = api.works(
    >>>         query="machine learning in physics",
    >>>         filter="type:journal-article,has-orcid:1",
    >>>         select=["DOI", "title", "author", "is-referenced-by-count"],
    >>>         rows=5
    >>>     )
    >>>     for item in result.get("message", {}).get("items", []):
    >>>         print(item.get("title", [""])[0], "-", item.get("DOI"))

    >>>     # Query works by journal
    >>>     journal_result = api.works_by_journal(
    >>>         issn="1234-5678",
    >>>         rows=3,
    >>>         select=["DOI", "title"]
    >>>     )
    >>>     print(journal_result)

    >>>     # Query works by member
    >>>     member_result = api.works_by_member(
    >>>         member_id="297",
    >>>         rows=3,
    >>>         select=["DOI", "title"]
    >>>     )
    >>>     print(member_result)
    """

    BASE_URL = "https://api.crossref.org"

    def __init__(self, mailto: Optional[str] = None):
        """
        Initialize the API wrapper.

        Args:
            mailto: Optional email address to identify the client (recommended by Crossref).
        """
        self.mailto = mailto

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Internal method to make a GET request to the API.
        """
        if params is None:
            params = {}
        if self.mailto:
            params["mailto"] = self.mailto
        resp = requests.get(f"{self.BASE_URL}{endpoint}", params=params)
        resp.raise_for_status()
        return resp.json()

    def works(
        self,
        query: str,
        filter: Optional[str] = None,
        select: Optional[List[str]] = None,
        rows: int = 20,
        cursor: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Query /works endpoint.

        Args:
            query: Free-text search term.
            filter: Optional filter string (e.g., "type:journal-article,has-orcid:1").
            select: Optional list of fields to return (e.g., ["DOI","title"]).
            rows: Number of results per page (max 1000).
            cursor: Cursor string for deep paging ("*" for initial request).

        Returns:
            JSON response as dict.
        """
        params: Dict[str, Any] = {"query": query, "rows": rows}
        if filter:
            params["filter"] = filter
        if select:
            params["select"] = ",".join(select)
        if cursor:
            params["cursor"] = cursor
        return self._get("/works", params)

    def works_by_journal(
        self,
        issn: str,
        filter: Optional[str] = None,
        select: Optional[List[str]] = None,
        rows: int = 20,
        cursor: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Query /journals/{issn}/works endpoint.

        Args:
            issn: ISSN of the journal.
            filter: Optional filter string.
            select: Optional list of fields to return.
            rows: Number of results per page.
            cursor: Cursor string for paging.

        Returns:
            JSON response as dict.
        """
        params: Dict[str, Any] = {"rows": rows}
        if filter:
            params["filter"] = filter
        if select:
            params["select"] = ",".join(select)
        if cursor:
            params["cursor"] = cursor
        return self._get(f"/journals/{issn}/works", params)

    def works_by_member(
        self,
        member_id: str,
        filter: Optional[str] = None,
        select: Optional[List[str]] = None,
        rows: int = 20,
        cursor: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Query /members/{member_id}/works endpoint.

        Args:
            member_id: Crossref member ID.
            filter: Optional filter string.
            select: Optional list of fields to return.
            rows: Number of results per page.
            cursor: Cursor string for paging.

        Returns:
            JSON response as dict.
        """
        params: Dict[str, Any] = {"rows": rows}
        if filter:
            params["filter"] = filter
        if select:
            params["select"] = ",".join(select)
        if cursor:
            params["cursor"] = cursor
        return self._get(f"/members/{member_id}/works", params)


class GutendexAPI:
    """
    `Wrapper for the Gutendex API (https://gutendex.com/).`

    #### Usage :
    >>> if __name__ == "__main__":
    >>>     api = GutendexAPI()

    >>>     # Search for English books by Jane Austen
    >>>     resp = api.list_books(search="Jane Austen", languages=["en"], page=1, sort="popular")
    >>>     for b in resp.get("results", [])[:5]:
    >>>         print(b["id"], b["title"], b["download_count"])

    >>>     # Fetch details for a specific book
    >>>     book_id = resp.get("results", [])[0]["id"]
    >>>     book_details = api.get_book(book_id)
    >>>     print(book_details["title"], book_details["authors"], book_details["formats"])
    """

    BASE_URL = "https://gutendex.com"

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{endpoint}"
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def list_books(
        self,
        page: int = 1,
        search: Optional[str] = None,
        languages: Optional[List[str]] = None,
        copyright: Optional[Union[bool, None]] = None,
        mime_type: Optional[str] = None,
        topic: Optional[str] = None,
        sort: Optional[Literal["ascending", "descending", "popular"]] = None,
    ) -> Dict[str, Any]:
        """
        List or search books with optional filters.

        Args:
            page: Page number (1‑based).
            search: Free text to search titles/authors.
            languages: List of language codes to filter (e.g., ["en","fr"]).
            copyright: True/False/None to filter copyright status.
            mime_type: MIME type prefix (e.g., "text/" or "application/epub+zip").
            topic: Topic or subject keyword.
            sort: Sort order ("ascending", "descending", "popular").

        Returns:
            JSON response with keys: count, next, previous, results (list of book objects).
        """
        params: Dict[str, Any] = {"page": page}
        if search is not None:
            params["search"] = search
        if languages is not None:
            params["languages"] = ",".join(languages)
        if copyright is not None:
            # can pass "true","false", or "null" equivalent
            params["copyright"] = str(copyright).lower()
        if mime_type is not None:
            params["mime_type"] = mime_type
        if topic is not None:
            params["topic"] = topic
        if sort is not None:
            params["sort"] = sort
        return self._get("/books", params)

    def get_book(
        self,
        book_id: int
    ) -> Dict[str, Any]:
        """
        Get detailed metadata for a single book by its Project Gutenberg ID.

        Args:
            book_id: The numeric ID of the book.

        Returns:
            JSON object representing the book.
        """
        return self._get(f"/books/{book_id}")
    
class OpenLibraryAPI:
    """
    Python wrapper for the Open Library REST API (https://openlibrary.org/developers/api)
    #### Usage : 
    >>>        if __name__ == "__main__":
    >>>        api = OpenLibraryAPI()

    >>>        # Search for books by "Isaac Asimov"
    >>>        search_results = api.search("Isaac Asimov", fields=["title", "author_name"], limit=5)
    >>>        for doc in search_results.get("docs", []):
    >>>            print(doc.get("title"), "-", doc.get("author_name"))

    >>>        # Get a specific book by OLID
    >>>        book = api.get_book("OL7353617M")
    >>>        print("Book title:", book.get("title"))

    >>>        # Get a work by Work ID
    >>>        work = api.get_work("OL45883W")
    >>>        print("Work title:", work.get("title"))

    >>>        # Get an author by Author ID
    >>>        author = api.get_author("OL23919A")
    >>>        print("Author name:", author.get("name"))

    >>>        # Get works by subject
    >>>        subject = api.get_subject("science_fiction")
    >>>        print("Subject works count:", len(subject.get("works", [])))
    """

    BASE_URL = "https://openlibrary.org"

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "User-Agent": "PySeedService/1.0 (tempuser0717@gmail.com) # Thankyou <3.!"
        }
        resp = requests.get(url, params=params, headers=headers)
        resp.raise_for_status()
        return resp.json()

    # -----------------------
    # Search endpoints
    # -----------------------
    def search(
        self,
        query: str,
        fields: Optional[List[str]] = None,
        limit: int = 100,
        page: int = 1
    ) -> Dict[str, Any]:
        """
        Search books/works with a free-text query.

        Args:
            query: Search query string (title, author, subject, etc.).
            fields: Optional list of fields to return (e.g., ['title', 'author_name']).
            limit: Number of results per page (max 100).
            page: Page number (1-based).

        Returns:
            JSON response from Open Library search API.
        """
        params = {
            "q": query,
            "limit": limit,
            "page": page
        }
        if fields:
            params["fields"] = ",".join(fields)
        return self._get("/search.json", params)

    # -----------------------
    # Book endpoints
    # -----------------------
    def get_book(self, olid: str) -> Dict[str, Any]:
        """
        Fetch a book by OLID (Open Library ID for edition).

        Args:
            olid: Open Library Edition ID (e.g., 'OL7353617M').

        Returns:
            JSON object with book metadata.
        """
        return self._get(f"/books/{olid}.json")

    # -----------------------
    # Work endpoints
    # -----------------------
    def get_work(self, work_id: str) -> Dict[str, Any]:
        """
        Fetch a work by its Open Library Work ID.

        Args:
            work_id: Open Library Work ID (e.g., 'OL45883W').

        Returns:
            JSON object with work metadata.
        """
        return self._get(f"/works/{work_id}.json")

    # -----------------------
    # Author endpoints
    # -----------------------
    def get_author(self, author_id: str) -> Dict[str, Any]:
        """
        Fetch an author by Open Library Author ID.

        Args:
            author_id: Open Library Author ID (e.g., 'OL23919A').

        Returns:
            JSON object with author metadata.
        """
        return self._get(f"/authors/{author_id}.json")

    # -----------------------
    # Subject endpoints
    # -----------------------
    def get_subject(self, subject: str) -> Dict[str, Any]:
        """
        Fetch works under a subject.

        Args:
            subject: Subject name (e.g., 'science_fiction').

        Returns:
            JSON object with subject metadata and works.
        """
        return self._get(f"/subjects/{subject}.json")

class PoetryDBAPI:
    """
    Python wrapper for the PoetryDB API (https://poetrydb.org/).
    #### Usage :    
    >>>    if __name__ == "__main__":
    >>>        api = PoetryDBAPI()
    >>>        # Random poem
    >>>        poem_list = api.random_poem()
    >>>        print("Random poem:", poem_list[0])

    >>>        # By author
    >>>        poems_by_shakespeare = api.poems_by_author("William Shakespeare")
    >>>        print("Shakespeare first poem title:", poems_by_shakespeare[0]["title"])

    >>>        # By title
    >>>        specific = api.poems_by_title("Ozymandias")
    >>>        print("Ozymandias:", specific)

    >>>        # By line keyword
    >>>        by_keyword = api.poems_by_line_keyword("Death")
    >>>        print("Poems with line containing 'Death':", len(by_keyword))
    """

    BASE_URL = "https://poetrydb.org/"

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.BASE_URL.rstrip('/')}/{path.lstrip('/')}"
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def random_poem(self) -> List[Dict[str, Any]]:
        """
        Fetch a random poem (or multiple, if the API returns multiple).
        Returns a list of poems.
        """
        return self._get("random")

    def poems_by_author(self, author: str) -> List[Dict[str, Any]]:
        """
        Fetch poems by a given author.
        Args:
            author: Name of the author (spaces may need encoding).
        Returns:
            List of poem objects.
        """
        safe_author = author.replace(" ", "%20")
        return self._get(f"author/{safe_author}")

    def poems_by_title(self, title: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Fetch poem(s) by title.
        Args:
            title: Title of the poem.
        Returns:
            Either a dict if single, or list of poem objects.
        """
        safe_title = title.replace(" ", "%20")
        return self._get(f"title/{safe_title}")

    def poems_by_line_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Search poems by a line keyword.
        Args:
            keyword: Keyword that might appear in a line.
        Returns:
            List of poem objects containing that keyword.
        """
        safe_keyword = keyword.replace(" ", "%20")
        return self._get(f"lines/{safe_keyword}")
    
class WiktionaryAPI:
    """
    Wrapper for the English Wiktionary API (MediaWiki action + REST endpoints).
    #### Usage :
    >>>    if __name__ == "__main__":
    >>>        api = WiktionaryAPI(user_agent="GliTCHBot/1.0 (mailto:giltch@example.com)")

    >>>        # Query page content for "test"
    >>>        resp1 = api.query_page("test", prop="extracts")
    >>>        print(resp1)

    >>>        # Get definitions via REST endpoint
    >>>        defs = api.get_definitions("apple", language="en")
    >>>        for d in defs:
    >>>            print(d.get("partOfSpeech"), d.get("definitions"))
    
    """

    BASE_ACTION = "https://en.wiktionary.org/w/api.php"
    BASE_REST  = "https://en.wiktionary.org/api/rest_v1"

    def __init__(self, user_agent: Optional[str] = None):
        """
        Args:
            user_agent: Optional custom User‑Agent header (recommended for Wikimedia APIs).
        """
        self.session = requests.Session()
        if user_agent:
            self.session.headers.update({"User‑Agent": user_agent})

    def query_page(
        self,
        title: str,
        format: Literal["json", "xml"] = "json",
        prop: Optional[str] = None,
        pageids: Optional[Union[int, str]] = None,
        revisions: bool = False
    ) -> Dict[str, Any]:
        """
        Use the Action API to query a page.

        Args:
            title: The page title (term) to query.
            format: Response format.
            prop: Which page property to include (e.g., "extracts", "revisions", "info").
            pageids: If you prefer specifying pageids.
            revisions: Whether to include revision history.

        Returns:
            Parsed JSON (or raw if xml).
        """
        params: Dict[str, Any] = {
            "action": "query",
            "format": format,
            "utf8": 1,
        }
        if title:
            params["titles"] = title
        if prop:
            params["prop"] = prop
        if pageids is not None:
            params["pageids"] = pageids
        if revisions:
            params["rvprop"] = "timestamp|user|comment|content"
        resp = self.session.get(self.BASE_ACTION, params=params)
        resp.raise_for_status()
        if format == "json":
            return resp.json()
        else:
            return {"raw": resp.text}

    def get_definitions(
        self,
        term: str,
        language: Optional[str] = "en"
    ) -> List[Dict[str, Any]]:
        """
        Use the REST API to get definitions for a given term.
        (Experimental endpoint)
        
        Args:
          term: Term to look up.
          language: Language code (e.g., "en").
        
        Returns:
          A list of definition objects.
        """
        url = f"{self.BASE_REST}/page/definition/{term}"
        resp = self.session.get(url)
        resp.raise_for_status()
        data = resp.json()
        # The structure: e.g. data["en"] for English definitions
        return data.get(language, [])
    
class DisifyAPI:
    """
    Wrapper for the Disify email/domain validation API.
    Documentation: https://docs.disify.com/ :contentReference[oaicite:1]{index=1}

    #### Usage :
    >>> if __name__ == "__main__":
    >>>     api = DisifyAPI()

    >>>     # Single email check
    >>>     result = api.validate_email("example@gmail.com")
    >>>     print("Single check:", result)

    >>>     # Bulk email check
    >>>     bulk = api.validate_bulk_emails(["test1@yahoo.com","temp@disposablemail.com"])
    >>>     print("Bulk overview:", bulk)
    >>>     session_id = bulk.get("session")
    >>>     if session_id:
    >>>         valid_list = api.view_bulk_results(session_id, separator=",")
    >>>         print("Valid emails:", valid_list)
    """

    BASE_URL = "https://disify.com/api"

    def __init__(self, timeout: float = 10.0):
        """
        Args:
            timeout: Request timeout in seconds.
        """
        self.session = requests.Session()
        self.timeout = timeout

    def validate_email(
        self,
        email: str,
    ) -> Dict[str, Any]:
        """
        Validate a single email address.

        Args:
            email: The email address to check.

        Returns:
            JSON response with keys like 'format', 'alias', 'domain', 'disposable', 'dns'.
        """
        url = f"{self.BASE_URL}/email/{email}"
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def validate_email_post(
        self,
        email: str
    ) -> Dict[str, Any]:
        """
        Alternative POST request for single email (in case you prefer POST).
        Args:
            email: The email address to check.
        """
        url = f"{self.BASE_URL}/email"
        resp = self.session.post(url, data={'email': email}, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def validate_bulk_emails(
        self,
        emails: List[str]
    ) -> Dict[str, Any]:
        """
        Validate multiple emails in bulk.

        Args:
            emails: List of email addresses (comma/new‑line separated list accepted).

        Returns:
            JSON response with keys: total, invalid_format, invalid_dns, disposable, unique, valid, session.
        """
        email_list = ",".join(emails)
        url = f"{self.BASE_URL}/email/{email_list}/mass"
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def view_bulk_results(
        self,
        session_id: str,
        separator: Optional[str] = None,
        force_download: bool = False
    ) -> Union[str, List[str]]:
        """
        Retrieve the valid emails list from a previously initiated bulk session.

        Args:
            session_id: The session ID returned by validate_bulk_emails.
            separator: If you want results separated by comma instead of newline.
            force_download: If true, trigger download.
        
        Returns:
            Either plain text list of emails (newline or comma separated) or a list of strings.
        """
        url = f"{self.BASE_URL}/view/{session_id}"
        params: Dict[str, Any] = {}
        if separator:
            params['separator'] = separator
        if force_download:
            params['download'] = 'true'
        resp = self.session.get(url, params=params, timeout=self.timeout)
        resp.raise_for_status()
        text = resp.text
        if separator:
            return text.split(separator)
        else:
            return text.split("\n")
        

class FreeDictionaryAPI:
    """
    Wrapper for the Free Dictionary API (https://dictionaryapi.dev/)
    
    #### Usage :
    >>>    if __name__ == "__main__":
    >>>        api = FreeDictionaryAPI(user_agent="GliTCHBot/1.0 (mailto:example@domain.com)")
    >>>        result = api.lookup_word("hello", language="en")
    >>>        # inspect
    >>>        print(result)
    >>>        # Check if it's an error:
    >>>        if isinstance(result, dict) and result.get("title") == "No Definitions Found":
    >>>            print("Word not found:", result.get("message"))
    >>>        else:
    >>>            # example access
    >>>            first = result[0]
    >>>            print("Word:", first.get("word"))
    >>>            print("Phonetic:", first.get("phonetic"))
    >>>            for meaning in first.get("meanings", []):
    >>>                print("Part of speech:", meaning.get("partOfSpeech"))
    >>>                for defn in meaning.get("definitions", []):
    >>>                    print(" - Definition:", defn.get("definition"))
    >>>                    if defn.get("example"):
    >>>                        print("   Example:", defn.get("example"))
    """

    BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries"

    def __init__(self, timeout: float = 10.0, user_agent: Optional[str] = None):
        """
        Args:
            timeout: Request timeout in seconds.
            user_agent: Optional custom User‑Agent header.
        """
        self.session = requests.Session()
        self.timeout = timeout
        if user_agent:
            self.session.headers.update({"User‑Agent": user_agent})

    def lookup_word(
        self,
        word: str,
        language: str = "en"
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Look up definitions and other lexical data for a word.

        Args:
            word: The word to look up.
            language: The language code (default "en" for English).

        Returns:
            If successful: a list of result objects (each dict includes 'word', 'phonetic', 'meanings', etc.).
            If not found/error: a dict with error keys (e.g., 'title', 'message', 'resolution').
        """
        url = f"{self.BASE_URL}/{language}/{word}"
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()