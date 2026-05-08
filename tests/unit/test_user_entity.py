from uuid import uuid4

from app.core.domain.entities.entity import Entity
from app.core.domain.entities.user import User, UserRole


class TestUserEntity:
    def test_create_user_with_defaults(self):
        user = User(
            username="testuser",
            email="test@example.com",
            first_name="John",
            last_name="Doe",
        )
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.role == UserRole.USER
        assert user.active is True
        assert user.id is not None

    def test_create_user_with_custom_values(self):
        custom_id = uuid4()
        user = User(
            username="admin",
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            role=UserRole.ADMIN,
            active=False,
            id=custom_id,
        )
        assert user.id == custom_id
        assert user.role == UserRole.ADMIN
        assert user.active is False

    def test_user_is_entity(self):
        user = User(
            username="testuser",
            email="test@example.com",
            first_name="John",
            last_name="Doe",
        )
        assert isinstance(user, Entity)

    def test_update_username(self):
        user = User(
            username="oldname",
            email="test@example.com",
            first_name="John",
            last_name="Doe",
        )
        user.update(username="newname")
        assert user.username == "newname"

    def test_update_email(self):
        user = User(
            username="testuser",
            email="old@example.com",
            first_name="John",
            last_name="Doe",
        )
        user.update(email="new@example.com")
        assert user.email == "new@example.com"

    def test_update_multiple_fields(self):
        user = User(
            username="testuser",
            email="test@example.com",
            first_name="John",
            last_name="Doe",
        )
        user.update(
            first_name="Jane",
            last_name="Smith",
            role=UserRole.ADMIN,
        )
        assert user.first_name == "Jane"
        assert user.last_name == "Smith"
        assert user.role == UserRole.ADMIN

    def test_activate_user(self):
        user = User(
            username="testuser",
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            active=False,
        )
        user.activate()
        assert user.active is True

    def test_deactivate_user(self):
        user = User(
            username="testuser",
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            active=True,
        )
        user.deactivate()
        assert user.active is False

    def test_user_roles(self):
        assert UserRole.ADMIN.value == "admin"
        assert UserRole.USER.value == "user"
        assert UserRole.GUEST.value == "guest"

    def test_user_properties(self):
        user = User(
            username="testuser",
            email="test@example.com",
            first_name="John",
            last_name="Doe",
        )
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.role == UserRole.USER
        assert user.active is True

    def test_user_timestamps(self):
        user = User(
            username="testuser",
            email="test@example.com",
            first_name="John",
            last_name="Doe",
        )
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_user_with_guest_role(self):
        user = User(
            username="guestuser",
            email="guest@example.com",
            first_name="Guest",
            last_name="User",
            role=UserRole.GUEST,
        )
        assert user.role == UserRole.GUEST

    def test_update_role_only(self):
        user = User(
            username="testuser",
            email="test@example.com",
            first_name="John",
            last_name="Doe",
        )
        user.update(role=UserRole.ADMIN)
        assert user.role == UserRole.ADMIN

    def test_update_active_only(self):
        user = User(
            username="testuser",
            email="test@example.com",
            first_name="John",
            last_name="Doe",
        )
        user.update(active=False)
        assert user.active is False

    def test_entity_equality(self):
        id = uuid4()
        user1 = User(
            id=id,
            username="testuser",
            email="test@example.com",
            first_name="John",
            last_name="Doe",
        )
        user2 = User(
            id=id,
            username="other",
            email="other@example.com",
            first_name="Jane",
            last_name="Doe",
        )
        assert user1 == user2

    def test_entity_inequality(self):
        user1 = User(
            username="user1",
            email="user1@example.com",
            first_name="John",
            last_name="Doe",
        )
        user2 = User(
            username="user2",
            email="user2@example.com",
            first_name="Jane",
            last_name="Doe",
        )
        assert user1 != user2
