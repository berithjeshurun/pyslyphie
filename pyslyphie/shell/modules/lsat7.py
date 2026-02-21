from typing import Literal, Dict, Any, Optional, Union
import requests
import json

MongoOperator = Literal["$lt", "$lte", "$gt", "$gte", "$eq", "$ne"]

KeplerField = Literal[
    "KOI", "A", "RPLANET", "RSTAR", "TSTAR", "KMAG",
    "TPLANET", "T0", "UT0", "PER", "UPER", "DEC",
    "RA", "MSTAR", "ROW"
]

def query_kepler(
    query: Optional[Dict[KeplerField, Dict[MongoOperator, Union[int, float]]]] = None,
    limit: int = 10,
    base_url: str = "https://asterank.com/api/kepler"
) -> list[Dict[str, Any]]:
    """
    Query the NASA Kepler Project dataset via the Asterank API.

    Args:
        query (Optional[Dict[KeplerField, Dict[MongoOperator, Union[int, float]]]]):
            A MongoDB-style query dict.
            Example:
                {
                    "TPLANET": {"$gt": 290, "$lt": 320},
                    "RPLANET": {"$lt": 5}
                }
        limit (int): Number of results to return (default: 10)
        base_url (str): Base API endpoint for the Kepler dataset.

    Returns:
        list[Dict[str, Any]]: List of exoplanet objects matching the query.
    """
    try:
        query_str = json.dumps(query or {})
        url = f"{base_url}?query={query_str}&limit={limit}"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            return data
        else:
            raise ValueError("Unexpected response format from Kepler API.")

    except requests.RequestException as e:
        print(f"[!] HTTP Error: {e}")
    except Exception as e:
        print(f"[!] Error: {e}")

    return []