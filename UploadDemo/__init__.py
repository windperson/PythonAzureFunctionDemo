import logging
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler())

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logger.info('Python HTTP trigger function processed a request.')

    if req.method != 'POST':
        return func.HttpResponse("Use Http Post", status_code=405)
    try:
        for uploadKey, uploadFile in req.files.items():
            logger.info('\n=====\n')
            logger.info('Start processing upload file: %s' % (uploadFile.filename))
            logger.info('file object type: %s' % type(uploadFile))
            logger.info('file extension = %s' % uploadFile.mimetype)
            logger.info('file content:')
            content = uploadFile.stream.read()
            logger.info(content)
        return func.HttpResponse('done')
    except Exception as e:
        logger.exception(e) 
        return func.HttpResponse('Process file failed, exception= [%s]' % e, status_code=400)  
