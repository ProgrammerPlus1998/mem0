from typing import Dict, Optional, Union

import httpx2


def build_http_client(http_client_proxies: Optional[Union[Dict, str]]) -> Optional[httpx2.Client]:
    if not http_client_proxies:
        return None
    if isinstance(http_client_proxies, dict):
        return httpx2.Client(
            mounts={scheme: httpx2.HTTPTransport(proxy=url) for scheme, url in http_client_proxies.items()}
        )
    return httpx2.Client(proxy=http_client_proxies)
