import requests, json
from typing import Literal


def get_trek_tile_url(
    body: Literal["moon", "mars", "vesta"],
    mosaic: str,
    style: str,
    tile_matrix_set: str,
    zoom: int,
    row: int,
    col: int,
    filetype: Literal["png", "jpg"] = "jpg"
) -> str:
    """
    Generate a NASA Trek WMTS tile URL.

    Args:
        body: Celestial body, one of "moon", "mars", "vesta".
        mosaic: The mosaic name (e.g., 'LRO_WAC_Mosaic_Global_303ppd_v02').
        style: The style identifier (from WMTS Capabilities XML).
        tile_matrix_set: The TileMatrixSet identifier.
        zoom: Zoom level (TileMatrix identifier).
        row: Tile row index.
        col: Tile column index.
        filetype: File extension, usually 'png' or 'jpg'.

    Returns:
        A formatted WMTS tile URL.
    """
    base_urls = {
        "moon": "https://trek.nasa.gov/tiles/Moon/EQ",
        "mars": "https://trek.nasa.gov/tiles/Mars/EQ",
        "vesta": "https://trek.nasa.gov/tiles/Vesta/EQ"
    }

    base_url = base_urls[body]
    return f"{base_url}/{mosaic}/1.0.0/{style}/{tile_matrix_set}/{zoom}/{row}/{col}.{filetype}"


def sl__lsat5__trkti(args, **kwargs) :
    if len(args) != 8 :
        return '<p style="color:red !important;">[-] Expected 8 arguments: body, mosaic, style, matrix_set, zoom, row, col, filetype</p>'
    return f'<p>Trek tile -> {get_trek_tile_url(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7])}</p>'

