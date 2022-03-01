import logging
log = logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger()
#logger.disabled = True
#logging.debug('This message should go to the log file')
#logging.info('So should this')
#logging.warning('And this, too')
#logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
