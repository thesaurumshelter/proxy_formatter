import re


class Proxy:
    """
    Usage examples
    proxy_str = "http://user:password@178.157.102.61:8122"
    Proxy(proxy_str).to_playwright_proxy()
    Proxy(proxy_str).to_cffi_proxy()
    """

    def __init__(self, proxy_str: str):
        self.proxy_str = proxy_str
        self.formatted_proxy = self.format_proxy()

    def format_proxy(self) -> dict | None:
        """
        Format the proxy string into a structured dictionary or string.
        :return: dict | str
        """
        formatted_proxy = {}
        protocol = 'http://'
        proxy = self.proxy_str

        if '//' in proxy:
            protocol = proxy.split('//')[0].strip()
            proxy = proxy.split('//')[1].strip()

        formatted_proxy['protocol'] = protocol
        formatted_proxy['host'] = None

        reg_host_port = r"(^((2[0-4]\d|25[0-5]|1\d{2}|\d{1,2})\.){3}(2[0-4]\d|25[0-5]|1\d{2}|\d{1,2}))\W([0-9]{3,4})"
        match_host_port = re.search(reg_host_port, proxy)
        if match_host_port:
            formatted_proxy['host'] = match_host_port.group(1)
            formatted_proxy['port'] = match_host_port.group(5)

        reg_user_passw = r"(\d*[a-zA-Z]\w+)\W(\d*[a-zA-Z]\w+)"
        match_user_password = re.search(reg_user_passw, proxy)
        if match_user_password:
            formatted_proxy['user'] = match_user_password.group(1)
            formatted_proxy['password'] = match_user_password.group(2)

        if formatted_proxy['host'] is None:
            return None
        return formatted_proxy

    def to_playwright_proxy(self) -> dict:
        """Format the proxy to Playwright dict format."""
        if not self.formatted_proxy:
            return {}
        return {
            "server": f"{self.formatted_proxy['protocol']}{self.formatted_proxy['host']}:{self.formatted_proxy['port']}",
            "username": self.formatted_proxy.get('user'),
            "password": self.formatted_proxy.get('password'),
        }

    def to_cffi_proxy(self) -> str:
        """Format the proxy to curl_cffi str format."""
        if not self.formatted_proxy:
            return ""
        return (f"{self.formatted_proxy['user']}:{self.formatted_proxy['password']}"
                f"@{self.formatted_proxy['host']}:{self.formatted_proxy['port']}")

    def to_ip(self) -> str:
        """Format the proxy to ip str format."""
        if not self.formatted_proxy:
            return ""
        return f"{self.formatted_proxy['host']}"
