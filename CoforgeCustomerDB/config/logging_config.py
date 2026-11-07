import logging
import os 

#Step 1:create logs directory
os.makedirs("logs",exist_ok=True)

#step2:Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s| %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

#step3:create logger
logger=logging.getLogger("CoforgeCustomerAPI")