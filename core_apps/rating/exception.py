from rest_framework.exceptions import APIException

class AlreadyHaveRating(APIException):
    status_code = 200
    default_detail = "You already have rating for this article"
    default_code = "bad_request"