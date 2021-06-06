import logging
import os
def logger_initiation():
    logging.basicConfig(format='%(asctime)s %(message)s',filename='wikigenerator.log', encoding='utf-8', level=logging.DEBUG)
    logging.debug('Initiating Server Instance')
    return