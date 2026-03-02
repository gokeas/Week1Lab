import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


# Snapshot of initial activities so tests can reset shared state
_INITIAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    # Reset the in-memory activities dict before each test for isolation
    activities.clear()
    activities.update(copy.deepcopy(_INITIAL_ACTIVITIES))
    yield


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
