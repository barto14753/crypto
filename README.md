# Crypto

[![](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)]()
[![](https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white)]()
[![](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)]()

Not optimized hash and encryption algorithms written in numpy


## Algorithms

- SHA1
- MD5
- BASE64

## Usage
```python
from crypto.sha1 import SHA1
from crypto.md5 import MD5
from crypto.base64 import Base64

SHA1("abc").data # 'abc'
SHA1("abc").hash() # 'a9993e364706816aba3e25717850c26c9cd0d89d'

MD5("abc").data # 'abc'
MD5("abc").hash() # '900150983cd24fb0d6963f7d28e17f72'

Base64("abc").data # 'abc'
Base64("abc").encoded_data # 'YWJj'

```
