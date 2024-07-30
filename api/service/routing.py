from posixpath import join
from fastapi.responses import RedirectResponse as OldRedirectResponse


def redirect(url: str, root_path: str = None):
    if root_path:
        url = join(root_path, url.lstrip("/"))
    return url


class RedirectResponse(OldRedirectResponse):
    def __init__(self, url: str, root_path: str = None):
        final_url = redirect(url, root_path)
        super().__init__(final_url)
