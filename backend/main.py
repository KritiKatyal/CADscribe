from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import Optional
import numpy as np
import trimesh
import os
import re
import uuid
from fastapi.staticfiles import StaticFiles
from shapely.geometry import Polygon
from trimesh.creation import triangulate_polygon


# --- Init App ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve files from the "uploads" folder
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# --- Load GPT-2 ---
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

# --- Ensure Uploads Directory Exists ---
os.makedirs("uploads", exist_ok=True)

# --- Request Model ---
class ModelRequest(BaseModel):
    prompt: str
    size: float = 100.0
    complexity: str = "medium"
    modification: Optional[str] = None

# --- Shape Functions ---
def create_sphere(size): return trimesh.creation.icosphere(radius=size)
def create_cube(size): return trimesh.creation.box(extents=[size]*3)
def create_cylinder(size): return trimesh.creation.cylinder(radius=size/2, height=size)
def create_cone(size): return trimesh.creation.cone(radius=size/2, height=size)
def create_pyramid(size):
    h = size
    s = size
    vertices = np.array([
        [0, 0, h],     # Top
        [s, s, 0],     # Base 1
        [-s, s, 0],    # Base 2
        [-s, -s, 0],   # Base 3
        [s, -s, 0]     # Base 4
    ])
    faces = np.array([
        [0, 1, 2],
        [0, 2, 3],
        [0, 3, 4],
        [0, 4, 1],
        [1, 2, 3],
        [1, 3, 4]
    ])
    return trimesh.Trimesh(vertices=vertices, faces=faces)

def make_regular_polygon(sides=6, radius=1.0):
    angle = 2 * np.pi / sides
    points = [(np.cos(i * angle) * radius, np.sin(i * angle) * radius) for i in range(sides)]
    return Polygon(points)
polygon = make_regular_polygon(sides=6, radius=1.0)

# Use specific triangulation engine
tri_mesh = trimesh.creation.extrude_polygon(polygon, height=1.0, triangulate=True)
def create_torus(size): return trimesh.creation.torus(radius=size/2, tube_radius=size/6)
# def create_prism(size, sides=3): return trimesh.creation.polyhedron(vertices=np.array([[size, 0, 0], [-size, 0, 0], [0, size, 0], [0, -size, 0], [0, 0, size]]), faces=np.array([[0, 1, 2], [1, 2, 3], [2, 3, 0]]))
def create_prism(size, sides=6):
    polygon = make_regular_polygon(sides=sides, radius=size)
    return trimesh.creation.extrude_polygon(polygon, height=size)



def create_ellipsoid(size): return trimesh.creation.ellipsoid(radius=size)
def create_wedge(size): return trimesh.creation.wedge(extents=[size, size, size])
def create_hollow_cylinder(size): return trimesh.creation.cylinder(radius=size/3, height=size)

# --- Mechanical Components ---
def create_bracket(size): return trimesh.creation.box(extents=[size, size/2, size/2])  # L-shaped, can modify later
def create_bolt(size): return trimesh.creation.cylinder(radius=size/5, height=size)
def create_screw(size): return trimesh.creation.cylinder(radius=size/5, height=size)
def create_nut(size): return trimesh.creation.cylinder(radius=size/2, height=size/10)
def create_thread(size): return trimesh.creation.cylinder(radius=size/5, height=size, sections=32)
def create_hole(size): return trimesh.creation.cylinder(radius=size/2, height=size)
def create_slot(size): return trimesh.creation.box(extents=[size, size/2, size/4])
def create_fillet(size): return trimesh.creation.sphere(radius=size)
def create_chamfer(size): return trimesh.creation.cylinder(radius=size/4, height=size/10)
def create_boss(size): return trimesh.creation.cylinder(radius=size/2, height=size/4)
def create_rib(size): return trimesh.creation.box(extents=[size, size/10, size])
def create_web(size): return trimesh.creation.box(extents=[size/10, size, size])
def create_gear(size): return trimesh.creation.cylinder(radius=size, height=size/10)  # Simplified spur gear example
def create_pin(size): return trimesh.creation.cylinder(radius=size/5, height=size)
def create_hinge(size): return trimesh.creation.cylinder(radius=size/4, height=size/2)
def create_joint(size): return trimesh.creation.sphere(radius=size)
def create_mount(size): return trimesh.creation.box(extents=[size*2, size, size/4])
def create_base_plate(size): return trimesh.creation.box(extents=[size, size, size/10])

# --- Advanced Parametric Shapes ---
def create_lofted_shape(size): return trimesh.creation.extrude_polygon(trimesh.creation.regular_polygon(3, radius=size), height=size)
def create_revolved_shape(size):
    profile = np.array([
        [0, 0],
        [size/4, 0],
        [size/2, size/2],
        [0, size]
    ])
    return trimesh.creation.revolve(profile)

def create_swept_shape(size): return trimesh.creation.extrude_polygon(trimesh.creation.regular_polygon(6, radius=size), height=size)
def create_extruded_shape(size): return trimesh.creation.extrude_polygon(trimesh.creation.regular_polygon(4, radius=size), height=size)
def create_shell(size): return trimesh.creation.cylinder(radius=size, height=size/2)

# --- Add all shapes to shape_creators dictionary ---
shape_creators = {
    "sphere": create_sphere,
    "cube": create_cube,
    "cylinder": create_cylinder,
    "cone": create_cone,
    "pyramid": create_pyramid,
    "torus": create_torus,
    "prism": create_prism,
    "ellipsoid": create_ellipsoid,
    "wedge": create_wedge,
    "tube": create_hollow_cylinder,  # For Tube / Hollow Cylinder
    "hollow_cylinder": create_hollow_cylinder,  # Alias for hollow cylinder
    "bracket": create_bracket,
    "bolt": create_bolt,
    "screw": create_screw,
    "nut": create_nut,
    "thread": create_thread,
    "hole": create_hole,
    "slot": create_slot,
    "fillet": create_fillet,
    "chamfer": create_chamfer,
    "boss": create_boss,
    "rib": create_rib,
    "web": create_web,
    "gear": create_gear,
    "pin": create_pin,
    "hinge": create_hinge,
    "joint": create_joint,
    "mount": create_mount,
    "base_plate": create_base_plate,
    "lofted_shape": create_lofted_shape,
    "revolved_shape": create_revolved_shape,
    "swept_shape": create_swept_shape,
    "extruded_shape": create_extruded_shape,
    "shell": create_shell,
}

# --- Modification Function ---
def modify_model(model_path: str, modification: str):
    try:
        model = trimesh.load_mesh(model_path)
        match = re.search(r"(increase|decrease).+by\s+(\d+(?:\.\d+)?)\s*mm", modification)
        if not match:
            print("No valid modification pattern found.")
            return model_path

        action, value = match.group(1), float(match.group(2))
        scale = 1 + value / 100 if action == "increase" else 1 - value / 100
        
        # Handle Specific Modifications
        if "length" in modification:
            model.apply_transform(trimesh.transformations.scale_matrix(1 + value / 100, [1, 0, 0]))
        elif "width" in modification:
            model.apply_transform(trimesh.transformations.scale_matrix(1 + value / 100, [0, 1, 0]))
        elif "height" in modification:
            model.apply_transform(trimesh.transformations.scale_matrix(1 + value / 100, [0, 0, 1]))
        else:
            model.apply_transform(trimesh.transformations.scale_matrix(scale, model.centroid))

        mod_path = os.path.join("uploads", f"{uuid.uuid4().hex}_modified.stl")
        model.export(mod_path)
        return mod_path
    except Exception as e:
        print(f"Modification failed: {e}")
        return model_path

# --- Model Generator ---
def generate_advanced_model(prompt: str, size: float, complexity: str):
    try:
        input_text = f"Generate a 3D model of a shape from the following description: {prompt}. Complexity: {complexity}."
        inputs = tokenizer(input_text, return_tensors="pt")
        outputs = model.generate(**inputs, max_length=100, temperature=0.8, top_p=0.95)
        decoded = tokenizer.decode(outputs[0], skip_special_tokens=True).lower()
        print(f"GPT-2 output: {decoded}")

        for keyword, shape_func in shape_creators.items():
            if keyword in decoded:
                mesh = shape_func(size)
                file_name = f"{uuid.uuid4().hex}_{keyword}.stl"
                model_path = os.path.join("uploads", file_name)
                mesh.export(model_path)
                return model_path

        raise ValueError("Shape not recognized in the GPT-2 output.")
    except Exception as e:
        print(f"Error during model generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Async Endpoint for Model Generation ---
@app.post("/generate_model/")
async def generate_model(request: ModelRequest):
    model_path = generate_advanced_model(request.prompt, request.size, request.complexity)
    return {"file": model_path}

# --- Async Endpoint for Generate + Modify ---
@app.post("/modify_model/")
async def modify_model_endpoint(request: ModelRequest):
    base_path = generate_advanced_model(request.prompt, request.size, request.complexity)
    modified_path = modify_model(base_path, request.modification or "")
    return {"modifiedFile": modified_path}
