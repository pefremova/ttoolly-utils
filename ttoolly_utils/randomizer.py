from datetime import datetime, timedelta
import io
import os
import random
import re
import string
from typing import Literal, IO, Optional
from xml.etree import ElementTree

from ttoolly_utils.utils import convert_size_to_bytes


def get_randname(
    length: int = 10, content_type: str = "a", length_of_chunk: int = 10
) -> str:
    """
    Generate random string of given length and type.

    Args:
        length: Length of the string.
        content_type: Character set type
            a - all
            d - digits
            w - letters
            p - punctuation
            s - whitespace.
        length_of_chunk: Chunk size for repeated patterns.
    Returns:
        Random string.
    """
    if "a" == content_type:
        text = string.printable
    else:
        text = ""
        letters_dict = {
            "d": string.digits,
            "w": string.ascii_letters,
            "p": string.punctuation,
            "s": string.whitespace,
        }
        for t in content_type:
            text += letters_dict.get(t, t)

    count_of_chunks = length // length_of_chunk
    n = "".join(
        [random.choice(text) for _ in range(length_of_chunk)]
    ) * count_of_chunks + "".join(
        [random.choice(text) for _ in range(length % length_of_chunk)]
    )
    return n


def get_random_color(color_type: Literal["rgb", "hex"] = "rgb") -> str:
    """
    Return random color in rgb or hex format.

    Args:
        color_type: 'rgb' or 'hex'.
    Returns:
        Color string.
    """
    if color_type == "rgb":
        return f"rgb({random.randint(1, 255)}, {random.randint(1, 255)}, {random.randint(1, 255)})"
    if color_type == "hex":
        return "#%06x" % random.randint(0, 0xFFFFFF)


def get_random_datetime_value(
    datetime_from: Optional[datetime] = None,
    datetime_to: Optional[datetime] = None,
) -> datetime:
    """
    Return random datetime between given datetimes.

    Args:
        datetime_from: Start datetime.
        datetime_to: End datetime.
    Returns:
        Random datetime.
    """
    datetime_from = datetime_from or (datetime.today() - timedelta(days=30))
    datetime_to = datetime_to or (datetime.today() + timedelta(days=30))
    return datetime.fromtimestamp(
        random.randint(
            int(datetime_from.timestamp() * 10**6),
            int(datetime_to.timestamp() * 10**6),
        )
        / 10**6
    )


def get_random_domain_value(length: int) -> str:
    """
    Generate random domain name of given length.

    Args:
        length: Total length of domain.
    Returns:
        Random domain.
    """
    end_length = random.randint(2, min(length - 2, 6))
    domain_length = random.randint(1, min(length - end_length - 1, 62))
    subdomain_length = length - end_length - 1 - domain_length - 1
    if subdomain_length <= 1:
        subdomain = ""
        if subdomain_length >= 0:
            domain_length += 1 + subdomain_length
    else:
        subdomain = (
            f"{get_randname(1, 'w')}{get_randname(subdomain_length - 1, 'wd.-')}."
        )
        while any([len(el) > 62 for el in subdomain.split(".")]):
            subdomain = ".".join(
                [
                    (el if len(el) <= 62 else el[:61] + "." + el[62:])
                    for el in subdomain.split(".")
                ]
            )
        subdomain = re.sub(r"\.[\.\-]", ".%s" % get_randname(1, "w"), subdomain)
        subdomain = re.sub(r"\-\.", "%s." % get_randname(1, "w"), subdomain)
    if domain_length < 3:
        domain = get_randname(domain_length, "wd")
    else:
        domain = "%s%s%s" % (
            get_randname(1, "w"),
            get_randname(domain_length - 2, "wd-"),
            get_randname(1, "w"),
        )
        domain = re.sub(r"\-\-", "%s-" % get_randname(1, "w"), domain)

    return "%s%s.%s" % (subdomain, domain, get_randname(end_length, "w"))


def get_random_email_value(length: int, safe: bool = False) -> str:
    """
    Generate random email address of given length.
    See info about formats here:
        https://www.ietf.org/rfc/rfc2821.txt
        https://www.ietf.org/rfc/rfc3696.txt

    Args:
        length: Total length of email.
        safe: Use only ascii characters and numbers if True.
    Returns:
        Random email.
    """
    if length < 3:  # a@b
        raise ValueError("Email length cannot be less than 3")
    if length < 6:  # a@b.cd
        username = get_randname(1, "wd")
        domain = get_randname(length - 2, "wd")
        return f"{username}@{domain}".lower()

    MAX_USERNAME_LENGTH = 64
    min_length_without_name = 1 + 1 + 3  # @X.aa
    name_length = random.randint(
        min(2, length - min_length_without_name),
        min(MAX_USERNAME_LENGTH, length - min_length_without_name),
    )

    domain_length = length - name_length - 1  # <name>@<domain>
    symbols_for_generate = "wd"
    symbols_with_escaping = ""
    if not safe and name_length > 1:
        symbols_for_generate += "!#$%&'*+-/=?^_`{|}~."
        symbols_with_escaping = '\\"(),:;<>@[]'
        symbols_for_generate += symbols_with_escaping
    username = get_randname(name_length, symbols_for_generate)
    while ".." in username:
        username = username.replace("..", get_randname(1, "wd") + ".")
    for s in symbols_with_escaping:
        if s in username:
            username = username.replace(s, rf"\{s}")[:name_length]
    username = re.sub(r"(\.$)|(^\.)|(\\$)", get_randname(1, "wd"), username)
    while len(username) < name_length:
        username += get_randname(1, "wd")
    domain = get_random_domain_value(domain_length)
    return f"{username}@{domain}".lower()


def get_random_image(
    path: str = "",
    filename: str = "",
    size: int | str | None = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
) -> IO[bytes]:
    """
    Generate image file with given size and return file object.

    Args:
        path: Directory to save file.
        filename: Name of the file.
        size: File size in bytes or string.
        width: Image width.
        height: Image height.
    Returns:
        File-like object with image data.
    """
    width = width or random.randint(1, 1000)
    height = height or random.randint(1, 1000)

    filename = filename or get_randname(10, "wrd ").strip()
    if os.path.splitext(filename)[1] in (".bmp",):
        content = get_random_bmp_content(convert_size_to_bytes(size or 10))
    else:
        if size is not None:
            size = convert_size_to_bytes(size)
            _size = max(1, size - 800)
            width = min(_size, width)
            height = min(int(_size / width), height)
        else:
            size = 10
        content = {
            ".gif": get_random_gif_content,
            ".svg": get_random_svg_content,
            ".png": get_random_png_content,
        }.get(os.path.splitext(filename)[1].lower(), get_random_jpg_content)(
            size, width, height
        )
    if path:
        if os.path.exists(os.path.join(path, filename)):
            os.remove(os.path.join(path, filename))
        with open(os.path.join(path, filename), "ab") as f:
            f.write(content)
    else:
        f = io.BytesIO()
        f.write(content)
    return f


def get_random_img_content(
    img_format: str, size: int = 10, width: int = 1, height: int = 1
) -> bytes:
    """
    Generate image content in given format.

    Args:
        img_format: Image format (e.g. 'PNG').
        size: File size in bytes.
        width: Image width.
        height: Image height.
    Returns:
        Image content as bytes.
    """
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        raise ImportError("Pillow required. Install ttoolly as ttoolly[images]")
    size = convert_size_to_bytes(size)
    image = Image.new("RGB", (width, height), get_random_color("hex"))
    draw = ImageDraw.Draw(image)
    draw.rectangle(
        (0, 0, width - 1, height - 1),
        fill=None,
        outline=get_random_color("hex"),
        width=3,
    )
    circle_r = int(min(width, height) / 2 - 1)
    draw.circle(
        (width / 2, height / 2),
        radius=circle_r,
        fill=get_random_color("hex"),
        outline=get_random_color("hex"),
        width=3,
    )

    output = io.BytesIO()
    image.save(output, format=img_format)
    content = output.getvalue()
    size -= len(content)
    if size > 0:
        content += bytearray(size)
    del draw
    return content


def get_random_bmp_content(size: int = 10, width: int = 1, height: int = 1) -> bytes:
    """
    Generate BMP image content.

    Args:
        size: File size in bytes.
        width: Image width.
        height: Image height.
    Returns:
        BMP image content as bytes.
    """
    return get_random_img_content("BMP", size, width, height)


def get_random_gif_content(size: int = 10, width: int = 1, height: int = 1) -> bytes:
    """
    Generate GIF image content.

    Args:
        size: File size in bytes.
        width: Image width.
        height: Image height.
    Returns:
        GIF image content as bytes.
    """
    return get_random_img_content("GIF", size, width, height)


def get_random_jpg_content(size: int = 10, width: int = 1, height: int = 1) -> bytes:
    """
    Generate JPEG image content.

    Args:
        size: File size in bytes.
        width: Image width.
        height: Image height.
    Returns:
        JPEG image content as bytes.
    """
    return get_random_img_content("JPEG", size, width, height)


def get_random_png_content(size: int = 10, width: int = 1, height: int = 1) -> bytes:
    """
    Generate PNG image content.

    Args:
        size: File size in bytes.
        width: Image width.
        height: Image height.
    Returns:
        PNG image content as bytes.
    """
    return get_random_img_content("PNG", size, width, height)


def get_random_svg_content(size: int = 10, width: int = 1, height: int = 1) -> bytes:
    """
    Generate SVG image content.

    Args:
        size: File size in bytes.
        width: Image width.
        height: Image height.
    Returns:
        SVG image content as bytes.
    """

    size = convert_size_to_bytes(size)
    doc = ElementTree.Element(
        "svg",
        width=str(width),
        height=str(height),
        version="1.1",
        xmlns="http://www.w3.org/2000/svg",
    )
    ElementTree.SubElement(
        doc,
        "rect",
        width=str(width),
        height=str(height),
        style=f"fill:{get_random_color()};stroke-width:3;stroke:{get_random_color()}",
    )

    circle_r = int(min(width, height) / 2 - 1)
    ElementTree.SubElement(
        doc,
        "circle",
        r=str(circle_r),
        cx=str(int(width / 2)),
        cy=str(int(height / 2)),
        style=f"fill:{get_random_color()};stroke-width:3;stroke:{get_random_color()}",
    )

    output = io.StringIO()
    header = (
        '<?xml version="1.0" standalone="no"?>\n'
        '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
    )
    output.write(header)
    output.write(ElementTree.tostring(doc).decode())
    content = output.getvalue()
    size -= len(content)
    if size > 0:
        filler = "a" * (size - 9)
        content = f"{content}<!-- {filler} -->"
    output.close()
    return content.encode()
