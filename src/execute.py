from pathlib import Path
from src.db import create

import extract, transform, load
if __name__ == "__main__":
    # set up database
    create.main()
    
    # start etl
    e = extract.extract_data()
    #transform.main()
    load.store_data_in_postgresql(e, "market_trends")