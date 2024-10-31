import re


def format_proxy(proxy_str: str) -> dict | None:
    formatted_proxy = {}
    protocol = None
    proxy = proxy_str
    if '//' in proxy:
        protocol = proxy.split('//')[0].strip()
        proxy = proxy.split('//')[1].strip()

    formatted_proxy['protocol'] = protocol
    formatted_proxy['host'] = None

    reg_host_port = r"(^((2[0-4]\d|25[0-5]|1\d{2}|\d{1,2})\.){3}(2[0-4]\d|25[0-5]|1\d{2}|\d{1,2}))\W([0-9]{3,4})"
    match_host_port = re.search(reg_host_port, proxy)
    if match_host_port is not None:
        formatted_proxy['host'] = match_host_port.group(1)
        formatted_proxy['port'] = match_host_port.group(3)

    reg_user_passw = r"\d*[a-zA-Z]\w+\W\d*[a-zA-Z]\w+"

    match_user_password = re.search(reg_user_passw, proxy)
    if match_user_password is not None:
        formatted_proxy['user'] = match_user_password.group(1)
        formatted_proxy['password'] = match_user_password.group(3)

    if formatted_proxy['host'] is None:
        return
    return formatted_proxy
