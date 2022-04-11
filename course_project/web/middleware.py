from course_project.web.views.error_page import NotExistPageView, ServerErrorPageView, ForbiddenPageView


# def handle_exception(get_response):
#     def middleware(request):
#         response = get_response(request)
#         if response.status_code == 404:
#             return NotExistPageView.as_view()(request)
#         elif response.status_code >= 500:
#             return ServerErrorPageView.as_view()(request)
#         return response
#     return middleware


class HandleException:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return NotExistPageView.as_view()(request)
        elif response.status_code == 403:
            return ForbiddenPageView.as_view()(request)
        elif response.status_code >= 500:
            return ServerErrorPageView.as_view()(request)
        return response
