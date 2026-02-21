import subprocess, os, ctypes, sys
from typing import Optional, Literal, Union, List

def showError(title : str, message : str) -> None :
    ctypes.windll.user32.MessageBoxW(
            0, 
            f"{message}", 
            f"{title}", 
            0x10  # 0x10 = MB_ICONERROR
        )


MAIN_EXE = os.environ['wkhtmltopdf_path']


def html_to_pdf(
    input_files: Union[str, List[str]],
    output_file: str,
    *,
    # --- Global Options ---
    page_size: Literal["A4", "Letter", "Legal", "A3", "A5"] = "A4",
    orientation: Literal["Portrait", "Landscape"] = "Portrait",
    dpi: int = 300,
    image_dpi: int = 300,
    image_quality: int = 95,
    grayscale: bool = False,
    low_quality: bool = False,
    title: Optional[str] = None,
    quiet: bool = True,

    # --- Margins ---
    margin_top: str = "15mm",
    margin_bottom: str = "15mm",
    margin_left: str = "10mm",
    margin_right: str = "10mm",

    # --- Header & Footer ---
    header_left: Optional[str] = None,
    header_center: Optional[str] = None,
    header_right: Optional[str] = None,
    footer_left: Optional[str] = None,
    footer_center: Optional[str] = None,
    footer_right: Optional[str] = None,
    header_font_size: Optional[int] = 10,
    footer_font_size: Optional[int] = 8,

    # --- Page & Render Options ---
    zoom: float = 1.0,
    enable_javascript: bool = True,
    javascript_delay: int = 1000,
    no_stop_slow_scripts: bool = True,
    encoding: str = "UTF-8",

    # --- Security ---
    username: Optional[str] = None,
    password: Optional[str] = None,
    cookies: Optional[dict] = None,

    # --- Table of Contents ---
    add_toc: bool = False,
    toc_header_text: str = "Table of Contents",
    disable_toc_links: bool = False,

    # --- Advanced ---
    cover: Optional[str] = None,
    custom_headers: Optional[dict] = None,
    log_level: Literal["none", "error", "warn", "info"] = "none",

    # --- Executable Path ---
    wkhtmltopdf_path: str = f"{MAIN_EXE}"
) -> bool:
    """
    Convert HTML files or URLs into a single PDF using wkhtmltopdf.

    Automatically handles headers, footers, margins, and basic rendering options.
    """

    if isinstance(input_files, str):
        input_files = [input_files]

    cmd = [wkhtmltopdf_path]

    cmd += ["--page-size", page_size]
    cmd += ["--orientation", orientation]
    cmd += ["--dpi", str(dpi)]
    cmd += ["--image-dpi", str(image_dpi)]
    cmd += ["--image-quality", str(image_quality)]
    cmd += ["--log-level", log_level]

    if title:
        cmd += ["--title", title]
    if grayscale:
        cmd.append("--grayscale")
    if low_quality:
        cmd.append("--lowquality")
    if quiet:
        cmd.append("--quiet")

    cmd += [
        "--margin-top", margin_top,
        "--margin-bottom", margin_bottom,
        "--margin-left", margin_left,
        "--margin-right", margin_right
    ]

    if header_left: cmd += ["--header-left", header_left]
    if header_center: cmd += ["--header-center", header_center]
    if header_right: cmd += ["--header-right", header_right]
    if footer_left: cmd += ["--footer-left", footer_left]
    if footer_center: cmd += ["--footer-center", footer_center]
    if footer_right: cmd += ["--footer-right", footer_right]
    if header_font_size: cmd += ["--header-font-size", str(header_font_size)]
    if footer_font_size: cmd += ["--footer-font-size", str(footer_font_size)]

    cmd += ["--zoom", str(zoom)]
    cmd += ["--encoding", encoding]
    if enable_javascript: cmd.append("--enable-javascript")
    else: cmd.append("--disable-javascript")
    if javascript_delay > 0:
        cmd += ["--javascript-delay", str(javascript_delay)]
    if no_stop_slow_scripts:
        cmd.append("--no-stop-slow-scripts")

    if username and password:
        cmd += ["--username", username, "--password", password]
    if cookies:
        for k, v in cookies.items():
            cmd += ["--cookie", k, v]
    if custom_headers:
        for k, v in custom_headers.items():
            cmd += ["--custom-header", k, v]

    if add_toc:
        cmd.append("toc")
        cmd += ["--toc-header-text", toc_header_text]
        if disable_toc_links:
            cmd.append("--disable-toc-links")

    if cover:
        cmd += ["cover", cover]

    for file in input_files:
        cmd.append(file)

    cmd.append(output_file)

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"[OK] PDF generated => {output_file}")
            return True
        else:
            print("[ERROR] wkhtmltopdf failed:")
            print(result.stderr.decode(errors="ignore"))
            return False
    except Exception as e:
        print(f"[EXCEPTION] {e}")
        return False
