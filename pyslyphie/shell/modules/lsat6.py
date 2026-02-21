from typing import Literal, Dict, Any, Optional, Union
import requests
import json

MongoOperator = Literal["$lt", "$lte", "$gt", "$gte", "$eq", "$ne"]

AsteroidField = Literal[
    "e", "i", "a", "dv", "moid", "H", "per", "class", "neo", "spec", "price", "profit", "score"
]

def query_asterank(
    field: Optional[AsteroidField] = None,
    operator: Optional[MongoOperator] = None,
    value: Optional[Union[int, float, str]] = None,
    limit: int = 1,
    base_url: str = "https://asterank.com/api/asterank"
) -> list[Dict[str, Any]]:
    """
    Query the Asterank API for asteroid data.

    Args:
        field (Optional[AsteroidField]): The parameter to query, e.g. 'e' or 'a'.
        operator (Optional[MongoOperator]): MongoDB-style comparison operator (e.g. "$lt", "$gt").
        value (Optional[Union[int, float, str]]): The threshold or matching value.
        limit (int): Maximum number of asteroid results to return.
        base_url (str): Asterank API endpoint URL.

    Returns:
        list[Dict[str, Any]]: A list of asteroid data dictionaries.
    """

    query: Dict[str, Any] = {}
    if field and operator and value is not None:
        query[field] = {operator: value}

    try:
        url = f"{base_url}?query={json.dumps(query)}&limit={limit}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            return data
        else:
            raise ValueError("Unexpected response format from Asterank API.")

    except requests.RequestException as e:
        print(f"[!] HTTP Error: {e}")
    except Exception as e:
        print(f"[!] Error: {e}")

    return []





_MongoOperator = Literal["$lt", "$lte", "$gt", "$gte", "$eq", "$ne"]

MPCField = Literal[
    "e", "i", "a", "H", "G", "M", "om", "w", "rms", "num_obs",
    "num_opp", "epoch", "last_obs", "pert_p", "pert_c"
]

def query_mpc(
    query: Optional[Dict[str, Dict[_MongoOperator, Union[int, float, str]]]] = None,
    limit: int = 10,
    base_url: str = "https://asterank.com/api/mpc"
) -> list[Dict[str, Any]]:
    """
    Query the Minor Planet Center (MPC) dataset via the Asterank API.

    Args:
        query (Optional[Dict[str, Dict[MongoOperator, Union[int, float, str]]]]): 
            A MongoDB-style query. Example:
            {
                "e": {"$lt": 0.1},
                "i": {"$lt": 4},
                "a": {"$lt": 1.5}
            }
        limit (int): Number of results to return.
        base_url (str): Asterank MPC API endpoint.

    Returns:
        list[Dict[str, Any]]: List of asteroid records matching the query.
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
            raise ValueError("Unexpected response format from MPC API.")

    except requests.RequestException as e:
        print(f"[!] HTTP Error: {e}")
    except Exception as e:
        print(f"[!] Error: {e}")

    return []