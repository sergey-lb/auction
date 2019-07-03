class ViewNameMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        request.view_name = ".".join((view_func.__module__, view_func.__name__))
        if request.view_name == 'AuctionApp.auth_helpers.wrapper_function':
            request.view_name = view_func.view_name
