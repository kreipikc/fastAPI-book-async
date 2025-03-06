from fastapi import status
from .http_errors import HTTTPError
from ...admin.responses.responses import base_admin_response
from ...users.responses.utils import convert_to_example, merge_responses


class RoleResponse:
    """Roles responses.

    Attributes:
        update_role_put: Responses for update_role
        delete_role: Responses for delete_role
    """
    update_role_put = merge_responses(
        base_admin_response,
        {
            status.HTTP_404_NOT_FOUND: convert_to_example([
                HTTTPError.ROLE_NOT_FOUND_404,
            ]),
        }
    )

    delete_role = merge_responses(
        base_admin_response,
        {
            status.HTTP_404_NOT_FOUND: convert_to_example([
                HTTTPError.ROLE_NOT_FOUND_404,
            ]),
        }
    )