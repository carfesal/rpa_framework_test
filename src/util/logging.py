import logging

logging.basicConfig(format='%(asctime)s %(message)s')  # Create and configure logger
logger = logging.getLogger()  # Creating an object
logger.setLevel(logging.INFO)  # Setting the threshold of logger to DEBUG