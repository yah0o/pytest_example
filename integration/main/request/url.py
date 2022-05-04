import urllib
import urlparse


class Url(object):

    @staticmethod
    def build_url(base_url, path=None, args_dict=None):

        # Returns a list in the structure of urlparse.ParseResult
        url_parts = list(urlparse.urlparse(base_url))

        if path:
            url_parts[2] = path
        if args_dict:
            url_parts[4] = urllib.urlencode(args_dict)

        return urlparse.urlunparse(url_parts)

    @staticmethod
    def build_http(netloc, scheme='http', path='', args_dict=''):

        return urlparse.urlunparse([scheme, netloc, path, args_dict, '', ''])
