import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if req.method != 'POST':
        return func.HttpResponse("Use Http Post", status_code=405)
    try:
        for uploadKey, uploadFile in req.files.items():
            logging.info('\n=====\n')
            logging.info('Start processing upload file: %s' % (uploadFile.filename))
            logging.info('file object type: %s' % type(uploadFile))
            logging.info('file extension = %s' % uploadFile.mimetype)
            logging.info('file content:')
            content = uploadFile.stream.read()
            logging.info(content)
        return func.HttpResponse('done')
    except Exception as e:
        print(e) 
        return func.HttpResponse('Process file failed, exception= [%s]' % e, status_code=400)  
