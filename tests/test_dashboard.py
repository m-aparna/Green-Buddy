from .conftest import mock_sign_up_data, mock_plant_data
from app.models import Note

# Check if add plant form data is stored in database properly 
def test_add_plant(client, app):
    client.post("/sign-up", data=mock_sign_up_data)

    with app.app_context():
        response = client.post("/dashboard", data=mock_plant_data)

        note = Note.query.filter_by(plant_name="Mintu").first()        
        # Check Plant Name
        assert note.plant_name == mock_plant_data["plant_name"]
        #Check plant_species
        assert note.plant_species == mock_plant_data["plant_species"]
        #Check Details
        assert note.details == mock_plant_data["details"]

# Check if that added data is displayed properly 
def test_plant_display(client, app):
    client.post("/sign-up", data=mock_sign_up_data)

    with app.app_context():
        client.post("/dashboard", data=mock_plant_data)
        response = client.get("/dashboard")

        # Check status code
        assert response.status_code == 200
        # Check plant name is displayed
        assert b"<h4>Mintu</h4>" in response.data

# Check if delete function is working properly
def test_delete_plant(client, app):
    client.post("/sign-up", data=mock_sign_up_data)
    
    with app.app_context():
        client.post("/dashboard", data=mock_plant_data)
        note = Note.query.filter_by(plant_name="Mintu").first()

        assert note is not None # First check if plant exists

        response = client.post(f"/delete-note/{note.id}") # Delete 
        assert response.status_code == 302

        # Check if note was deleted
        deleted_note = Note.query.get(note.id)
        assert deleted_note is None

# Check if deleted data is not displayed
def test_delete_plant_display(client, app):
    client.post("/sign-up", data=mock_sign_up_data)

    with app.app_context():
        client.post("/dashboard", data=mock_plant_data)
        response_add_plant = client.get("/dashboard")

        # Check if plant is added
        assert b"<h4>Mintu</h4>" in response_add_plant.data

        # Delete plant
        note = Note.query.filter_by(plant_name="Mintu").first()
        client.post(f"/delete-note/{note.id}") # Delete 

        # Check if it is removed from displaying
        response_delete_plant = client.get("/dashboard")
        assert b"<h4>Mintu</h4>" not in response_delete_plant.data
