
from pathlib import Path
print(Path('.').absolute())

import extract, transform, load
if __name__ == "__main__":
    print(Path('.').absolute())
    extract.main()
    transform.main()
    load.main()