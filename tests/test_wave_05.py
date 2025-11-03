from app.models import goal
from app.models.goal import Goal
from app.db import db
import pytest

from tests.conftest import one_goal


def test_goal_to_dict():
    #Arrange
    new_goal = Goal(id=1, title="Seize the Day!")
    
    #Act
    goal_dict = new_goal.to_dict()

    #Assert
    assert goal_dict["id"] == 1
    assert goal_dict["title"] == "Seize the Day!"

def test_goal_to_dict_no_id():
    #Arrange
    new_goal = Goal(title="Seize the Day!")
    
    #Act
    goal_dict = new_goal.to_dict()

    #Assert
    assert goal_dict["id"] is None
    assert goal_dict["title"] == "Seize the Day!"


def test_goal_to_dict_no_title():
    #Arrange
    new_goal = Goal(id=1)
    
    #Act
    goal_dict = new_goal.to_dict()

    #Assert
    assert goal_dict["id"] == 1
    assert goal_dict["title"] is None




def test_goal_from_dict():
    #Arrange
    goal_dict =  {
        "title": "Seize the Day!",
    }

    #Act
    goal_obj =  Goal.from_dict(goal_dict)

    #Assert
    assert goal_obj.title == "Seize the Day!"


def test_goal_from_dict_no_title():
    #Arrange
    goal_dict =  {
    }

    #Act & Assert
    with pytest.raises(KeyError, match = 'title'):
        Goal.from_dict(goal_dict)


def test_get_goals_no_saved_goals(client):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_goals_one_saved_goal(client, one_goal):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Build a habit of going outside daily"
        }
    ]


def test_get_goal(client, one_goal):
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Build a habit of going outside daily"
    }


def test_get_goal_not_found(client):
    pass
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()

    assert response.status_code == 404

    assert "message" in response_body
    assert response_body["message"] == "Goal with ID (1) not found."

def test_create_goal(client):
    # Act
    response = client.post("/goals", json={
        "title": "My New Goal"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "title": "My New Goal"
    }


def test_update_goal(client, one_goal):
        # Act
    response = client.put(f"/goals/1", json={
            "title": "Updated Goal Title",
        })
    
    assert response.status_code == 204

    query = db.select(Goal).where(Goal.id == 1)
    goal = db.session.scalar(query)

    assert goal.title == "Updated Goal Title"
    assert goal.id == 1



def test_update_goal_not_found(client):
    # Act
    response = client.put("/goals/1", json={
        "title": "Updated Goal Title",
        })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404

    assert response_body == {"message": "Goal with ID (1) not found."}

def test_delete_goal(client, one_goal):
   # Act
    response = client.delete("/goals/1")

    # Assert
    assert response.status_code == 204

    query = db.select(Goal).where(Goal.id == 1)
    assert db.session.scalar(query) == None



def test_delete_goal_not_found(client):
    # Act
    response = client.delete("/goals/1")
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Goal with ID (1) not found."}

    assert db.session.scalars(db.select(Goal)).all() == []


def test_create_goal_missing_title(client):
    # Act
    response = client.post("/goals", json={})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Invalid data"
    }
