import json

'''
Multithreaded SimpleHTTPServer with logging.

@author: bkindley
'''
import BaseHTTPServer
import SimpleHTTPServer
import SocketServer
import logging.handlers
import os
import socket
import urlparse


# Make it multithreaded
class ThreadedHTTPD(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass


address = socket.getfqdn()
port = 8000
path = '.'
os.chdir(path)
LOGFILE = './HTTPServer.log'

# setup logging
logger = logging.getLogger('server_logger')
logger.setLevel(logging.INFO)

# create file handler which logs even info messages
'''
fh = logging.FileHandler(LOGFILE)
fh.setLevel(logging.INFO)
'''

# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Add the log message rotating handler to the logger
rh = logging.handlers.TimedRotatingFileHandler(
    LOGFILE, when='midnight', backupCount=5)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
ch.setFormatter(formatter)
'''
fh.setFormatter(formatter)
'''
rh.setFormatter(formatter)

# add the handlers to logger
logger.addHandler(ch)
'''
logger.addHandler(fh)
'''
logger.addHandler(rh)


# Override class to customize
class RequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        message = "%s" % (format % args)
        logger.info(message)

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        if 'json' in parsed_path.path:
            fullpath = os.path.join(os.path.abspath(os.path.join(os.path.curdir, os.pardir)), 'resources',
                                    'finance_sale_part_response.json')

            logger.info('Opening file at %s', fullpath)

            json_file = open(fullpath, 'rb')
            self.send_response(200)
            # copying the header I really received during working on the PLAT-1995
            self.send_header('Content-type', 'application/vnd.api+json;charset=utf-8')
            if 'negative_content_length' in parsed_path.path:
                self.send_header('Content-Length', '-1')

            self.end_headers()
            self.wfile.write(json_file.read())

            json_file.close()

        elif 'pdf' in parsed_path.path:
            fullpath = os.path.join(os.path.abspath(os.path.join(os.path.curdir, os.pardir)), 'resources',
                                    'extension_pdf_response.pdf')

            logger.info('Opening file at %s', fullpath)

            pdf_file = open(fullpath, 'rb')
            self.send_response(200)
            self.send_header('Content-type', 'application/pdf')
            self.send_header('custom', 'check_that_headers_are_preserved')
            self.end_headers()
            self.wfile.write(pdf_file.read())

            pdf_file.close()

        else:
            headers_received = {}
            for name, value in sorted(self.headers.items()):
                headers_received.update({name: value.rstrip()})
            json_message = {
                'CLIENT VALUES:': {'client_address': '%s (%s)' % (self.client_address, self.address_string()),
                                   'command': self.command, 'path': self.path,
                                   'real path': parsed_path.path, 'query': parsed_path.query,
                                   'request_version': self.request_version},
                'SERVER VALUES:': {'server_version': self.server_version, 'sys_version': self.sys_version,
                                   'protocol_version': self.protocol_version},
                'HEADERS RECEIVED:': headers_received}
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(json_message))

        return


if __name__ == '__main__':
    try:
        httpd = ThreadedHTTPD((address, port), RequestHandler)
        print 'Starting server, use <Ctrl-C> to stop'
        httpd.serve_forever()
    except KeyboardInterrupt:
        print 'Stopping server...'
        httpd.socket.close()
