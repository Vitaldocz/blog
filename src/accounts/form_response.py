class FormResponse:
    def __init__(self, status=None, message='', redirect_url='', error=None):
        self.status = status
        self.message = message
        self.redirect_url = redirect_url
        self.error = error

    def to_json(self):
        json = {
            'status': self.status,
            'message': self.message,
            'redirect_url': self.redirect_url,
            'error': self.error
        }
        return json

    def update_status(self, status):
        self.status = status

    def update_error(self, error):
        self.error = error

    def update_message(self, message):
        self.message = message

    def update_redirect_url(self, url):
        self.redirect_url = url


def error_response(error, redirect_url=''):
    return FormResponse(error=error, status=False, redirect_url=redirect_url)


def success_response(message, redirect_url=''):
    return FormResponse(message=message, status=True, redirect_url=redirect_url)
