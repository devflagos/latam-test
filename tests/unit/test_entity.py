from uuid import uuid4

from app.core.domain.entities.entity import Entity


class TestEntity:
    def test_create_entity(self):
        entity = Entity()
        assert entity.id is not None
        assert entity.created_at is not None
        assert entity.updated_at is not None

    def test_entity_with_custom_id(self):
        custom_id = uuid4()
        entity = Entity(id=custom_id)
        assert entity.id == custom_id

    def test_entity_equality(self):
        id = uuid4()
        entity1 = Entity(id=id)
        entity2 = Entity(id=id)
        assert entity1 == entity2

    def test_entity_inequality(self):
        entity1 = Entity()
        entity2 = Entity()
        assert entity1 != entity2

    def test_entity_hash(self):
        id = uuid4()
        entity = Entity(id=id)
        assert hash(entity) == hash(id)
