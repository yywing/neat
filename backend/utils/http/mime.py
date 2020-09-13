from mitmproxy.net.http.headers import parse_content_type


def check_other(content_type, content) -> bool:
    return True


# https://mimesniff.spec.whatwg.org/#json-mime-type
def check_json(content_type, content) -> bool:
    content_type = parse_content_type(content_type)
    if content_type[1].endwith("json"):
        return True
    return False


# multipart/form-data, application/x-www-form-urlencoded
def check_form(content_type, content) -> bool:
    content_type = parse_content_type(content_type)
    t = "{}/{}".format(content_type[0], content[1])
    form_list = [
        'multipart/form-data',
        'application/x-www-form-urlencoded',
    ]
    if t in form_list:
        return True
    return False


# https://mimesniff.spec.whatwg.org/#html-mime-type
def check_html(content_type, content) -> bool:
    content_type = parse_content_type(content_type)
    t = "{}/{}".format(content_type[0], content[1])
    html_list = [
        'text/html',
    ]
    if t in html_list:
        return True
    return False


# https://mimesniff.spec.whatwg.org/#xml-mime-type
def check_xml(content_type, content) -> bool:
    content_type = parse_content_type(content_type)
    if content_type[1].endwith("xml"):
        return True
    return False


# https://mimesniff.spec.whatwg.org/#image-mime-type
def check_image(content_type, content) -> bool:
    content_type = parse_content_type(content_type)
    if content_type[0].endwith("image"):
        return True
    return False


# https://mimesniff.spec.whatwg.org/#font-mime-type
def check_font(content_type, content) -> bool:
    content_type = parse_content_type(content_type)
    if content_type[0].endwith("font"):
        return True
    font_list = [
        'application/font-cff',
        'application/font-off',
        'application/font-sfnt',
        'application/font-ttf',
        'application/font-woff',
        'application/vnd.ms-fontobject',
        'application/vnd.ms-opentype',
    ]
    t = "{}/{}".format(content_type[0], content[1])
    if t in font_list:
        return True
    return False


def check_css(content_type, content) -> bool:
    content_type = parse_content_type(content_type)
    t = "{}/{}".format(content_type[0], content[1])
    css_list = [
        "text/css",
    ]
    if t in css_list:
        return True
    return False


def check_js(content_type, content) -> bool:
    content_type = parse_content_type(content_type)
    t = "{}/{}".format(content_type[0], content[1])
    js_list = [
        "application/ecmascript",
        "application/javascript",
        "application/x-ecmascript",
        "application/x-javascript",
        "text/ecmascript",
        "text/javascript",
        "text/javascript1.0",
        "text/javascript1.1",
        "text/javascript1.2",
        "text/javascript1.3",
        "text/javascript1.4",
        "text/javascript1.5",
        "text/jscript",
        "text/livescript",
        "text/x-ecmascript",
        "text/x-javascript",
    ]
    if t in js_list:
        return True
    return False


def check_empty(content_type, content) -> bool:
    if content_type == "":
        return True
    return False
