# Every file in this folder must follow this structure
- The file must have its APIRouter variable, preferably named as "router"
- The router must have a prefix for its endpoint, preferably in a variable named as "prefix"
- The file must have a function called "setup", which is of the following format
```python
from fastapi import APIRouter

router = APIRouter()
prefix = "/translate"

#
"""Your Code Here"""
#

def setup(app):
    app.include_router(router, prefix=prefix)
```
