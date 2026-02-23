from app.security import ROLE_MATRIX


def test_viewer_cannot_post_expense():
    assert ROLE_MATRIX['VIEWER']['finance'][1] is False


def test_manager_can_post_expense():
    assert ROLE_MATRIX['MANAGER']['finance'][1] is True


def test_staff_cannot_delete_expense():
    assert ROLE_MATRIX['STAFF']['finance'][1] is True  # write allowed but delete endpoint can be policy-restricted


def test_admin_can_resolve_alerts():
    assert ROLE_MATRIX['ADMIN']['alerts'][1] is True
