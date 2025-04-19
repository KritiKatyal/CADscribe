# fusion360_integration.py
import adsk.core, adsk.fusion, adsk.cam
import requests

FUSION_360_API_URL = "https://developer.api.autodesk.com/..."

def integrate_with_fusion360(file_path: str):
    """Integrates the generated model with Fusion 360."""
    try:
        response = requests.post(FUSION_360_API_URL, json={
            "file_path": file_path
        })
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Fusion 360 integration failed: {response.text}")
    except Exception as e:
        raise Exception(f"Fusion 360 integration error: {str(e)}")

def generate_and_import_model(prompt):
    """Generate a model and import it into Fusion 360."""
    response = requests.post("http://localhost:8000/generate_model/", json={"prompt": prompt})
    model_path = response.json().get("file")
    
    # Import the model into Fusion 360
    open_model_in_fusion(model_path)

def open_model_in_fusion(model_path):
    """Open the generated model in Fusion 360."""
    app = adsk.core.Application.get()
    design = app.activeProduct
    root = design.rootComponent

    stl_file = adsk.core.File.create(model_path)
    stl_importer = adsk.importexport.ImportManager.get().createSTLImporter(stl_file)
    stl_importer.execute(root)
