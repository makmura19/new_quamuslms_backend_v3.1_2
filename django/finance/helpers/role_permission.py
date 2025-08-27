from rest_framework.permissions import BasePermission
from constants.access import Role


def get_user_roles(request):
    if hasattr(request.user, "role") and isinstance(request.user.role, str):
        return request.user.role.split(",")
    return []


class RolePermission(BasePermission):
    def has_permission(self, request, view):
        action_name = getattr(view, "action", None)
        if not action_name:
            return False

        action_config = getattr(view, "custom_actions", {}).get(action_name) or getattr(
            view, "actions", {}
        ).get(action_name)

        if not action_config:
            return False

        allowed_roles = action_config.get("roles", [])

        if Role.PUBLIC in allowed_roles:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        if allowed_roles == [Role.ALL]:
            return True

        user_roles = get_user_roles(request)
        return any(role in allowed_roles for role in user_roles)
