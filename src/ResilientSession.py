from requests import Session
import logging
import time

class ResilientSession(Session):
    """Requests Session with added support for resilience (retry support on temporary errors like 502, 503, 504)
    Inspired by: https://bitbucket.org/bspeakmon/jira-python/src/a7fca855394402f58507ca4056de87ccdbd6a213/jira/resilientsession.py?at=master&fileviewer=file-view-default
    """

    def __init__(self, timeout=None, max_retries=None, retry_status_codes=[502, 503, 504]):
        """
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float or a `(connect timeout, read timeout)` tuple. By default, requests do not time out at all. 
            (Read more here: http://docs.python-requests.org/en/master/user/advanced/#timeouts)
        :param max_retries: (optional) Maximum number of retries before giving up completely. By default, requests keep retrying forever on temporary errors.
        :param retry_status_codes: (optional) List of HTTP status codes to use for retrying. By default, it retries 502, 503, 504.
        """
        super(ResilientSession, self).__init__()
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_status_codes = retry_status_codes

    def wait(self, counter):
        # @TODO : Implement exponential backoff algorithm
        delay = 10 * counter
        time.sleep(delay)

    def request(self, method, url, **kwargs):
        # set timeout
        kwargs['timeout'] = kwargs.get('timeout', self.timeout)

        counter = 0
        while True:
            counter += 1

            r = super(ResilientSession, self).request(method, url, **kwargs)
            if r.status_code in self.retry_status_codes:
                if self.max_retries is not None and counter >= self.max_retries:
                    logging.error("Still failing after #%s retries. Giving up!" % (counter))
                    return r

                logging.warn("Got recoverable error [%s] from %s %s, retry #%s in %ss" % (r.status_code, method, url, counter, delay))
                self.wait(counter)
                continue
            return r