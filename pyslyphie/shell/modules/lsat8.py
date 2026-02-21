from typing import Literal, Dict, Any, Optional, Union
import requests


SkyMorphField = Literal[
    "target", "epoch", "ecc", "per", "per_date", "om",
    "w", "i", "H", "ra", "dec", "time"
]

SearchType = Literal["target", "orbit", "position"]


def query_skymorph(
    search_type: SearchType,
    params: Dict[str, Union[str, float]],
    base_url: str = "http://asterank.com/api/skymorph"
) -> list[Dict[str, Any]]:
    """
    Query NASA's SkyMorph / NEAT archive via the Asterank REST API.

    Args:
        search_type (SearchType):
            Type of search to perform: "target", "orbit", or "position".
        params (Dict[str, Union[str, float]]):
            Parameters for the query.
            - target: Target name (for 'target' searches)
            - epoch, ecc, per, per_date, om, w, i, H (for 'orbit' searches)
            - ra, dec, time (for 'position' searches)
        base_url (str):
            Base API URL for SkyMorph (default: Asterank endpoint).

    Returns:
        list[Dict[str, Any]]: List of observations or positions from NEAT survey.
    """
    endpoints = {
        "target": "search",
        "orbit": "search_orbit",
        "position": "search_position"
    }

    if search_type not in endpoints:
        raise ValueError(f"Invalid search type: {search_type}")

    url = f"{base_url}/{endpoints[search_type]}"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and "results" in data:
            return data["results"]
        elif isinstance(data, list):
            return data
        else:
            raise ValueError("Unexpected response format from SkyMorph API.")

    except requests.RequestException as e:
        print(f"[!] HTTP Error: {e}")
    except Exception as e:
        print(f"[!] Error: {e}")

    return []


def get_skymorph_image(
    key: str,
    fast: bool = False,
    base_url: str = "http://asterank.com/api/skymorph",
    save_path: Optional[str] = None
) -> Optional[str]:
    """
    Retrieve an observation image from the SkyMorph archive.

    Args:
        key (str): Encoded key string from a SkyMorph observation result.
        fast (bool): If True, use the faster (less detailed) /fast_image endpoint.
        base_url (str): Base API URL for SkyMorph imagery.
        save_path (Optional[str]): If provided, saves the image locally.

    Returns:
        Optional[str]: File path if saved, otherwise None.
    """
    endpoint = "fast_image" if fast else "image"
    url = f"{base_url}/{endpoint}"
    params = {"key": key}

    try:
        r = requests.get(url, params=params)
        r.raise_for_status()

        if save_path:
            with open(save_path, "wb") as f:
                f.write(r.content)
            return save_path
        else:
            print("[~] Image data retrieved (use save_path to store locally).")

    except requests.RequestException as e:
        print(f"[!] HTTP Error: {e}")
    except Exception as e:
        print(f"[!] Error: {e}")

    return None
