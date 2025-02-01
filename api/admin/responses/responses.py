from fastapi import status
from .http_errors import HTTTPError
from ...roles.responses.http_errors import HTTTPError as HTTTPErrorRoles
from ...users.responses.http_errors import HTTTPError as HTTTPErrorUsers
from ...users.responses.responses import base_auth_responses
from ...users.responses.utils import convert_to_example


base_admin_response = base_auth_responses.copy()
base_admin_response.update({
    status.HTTP_403_FORBIDDEN: convert_to_example([
        HTTTPErrorUsers.NO_ACCESS_RIGHTS_403
    ])
})
"""Base administrations responses."""


class AdminResponses:
    """Admin responses.

    Attributes:
        update_user_role_put: Responses for update_user_role
        delete_user: Responses for delete_user
    """
    update_user_role_put = base_admin_response.copy()
    update_user_role_put.update({
        status.HTTP_404_NOT_FOUND: convert_to_example([
            HTTTPError.USER_NOT_FOUND_404,
            HTTTPErrorRoles.ROLE_NOT_FOUND_404,
        ]),
    })

    delete_user = base_admin_response.copy()
    delete_user.update({
        status.HTTP_404_NOT_FOUND: convert_to_example([
            HTTTPError.USER_NOT_FOUND_404,
        ]),
    })

