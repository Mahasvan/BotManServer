from fastapi.responses import RedirectResponse
from fastapi import FastAPI

from posixpath import join


class App(FastAPI):
    def __init__(self, *args, **kwargs):
        self.root_path = None
        super().__init__(*args, **kwargs)

    def redirect(self, url: str):
        prefix = self.root_path
        if prefix:
            url = join(prefix.lstrip("/"), url)
        return RedirectResponse(url=url)
