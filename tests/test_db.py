from db.session import engine
from db.models import Base
import pytest


@pytest.fixture(scope="module")
def test_db():
    Base.base.metadata.create_all(bind=engine)
    yield
    Base.base.metadata.drop_all(bind=engine)



def test_db_connection(test_db):
    assert True