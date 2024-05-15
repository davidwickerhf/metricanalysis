import logging

def setup_logger():
    # Configure the logger
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.StreamHandler(),  # Console output
                            logging.FileHandler("analysis.log")  # File output
                        ])
    logger = logging.getLogger(__name__)
    return logger