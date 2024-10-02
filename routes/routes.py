#routes/routes.py
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from utils.db import get_db
from models.models import CatBreed, Kitten

router = APIRouter()
templates = Jinja2Templates(directory="templates")

menu = [
    {"route": "home", "name": "home"},
    {"route": "breeds", "name": "breeds"},
    {"route": "kittens", "name": "kittens"},
]

# --- Main routes ---

@router.get("/", response_class=HTMLResponse, name="home",
            summary="Home Page",
            description="Render the home page of the application.")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "menu": menu})

@router.get("/breeds", response_class=HTMLResponse, name="breeds",
            summary="List of Cat Breeds",
            description="Fetch and display all cat breeds. If no breeds are found, default breeds will be displayed.")
async def breeds(request: Request, db: Session = Depends(get_db)):
    breeds = db.query(CatBreed).all()
    if not breeds:
        breeds = [
            {"name": "Siamese", "description": "Elegant and vocal cats."},
            {"name": "Persian", "description": "Long-haired and gentle cats."},
        ]
    return templates.TemplateResponse("breeds.html", {"request": request, "menu": menu, "breeds": breeds})

@router.get("/kittens", response_class=HTMLResponse, name="kittens",
            summary="List of Kittens",
            description="Fetch and display active kittens. Optionally filter by breed.")
async def kittens(request: Request, breed: int = 0, db: Session = Depends(get_db)):
    breeds = db.query(CatBreed).all()
    kittens_query = db.query(Kitten).filter(Kitten.is_active == True)

    if breed:
        kittens_query = kittens_query.filter(Kitten.breed_id == breed)

    kittens = kittens_query.all()
    return templates.TemplateResponse("kittens.html", {
        "request": request,
        "breeds": breeds,
        "kittens": kittens,
        "selected_breed_id": breed,
        "menu": menu
    })
# --- End Main routes ---

# --- Adding items routes  ---
@router.get("/add_kitten", response_class=HTMLResponse, name="add_kitten",
            summary="Add New Kitten Form",
            description="Render the form for adding a new kitten.")
async def add_kitten_form(request: Request, db: Session = Depends(get_db)):
    breeds = db.query(CatBreed).all()
    return templates.TemplateResponse("add_kitten.html", {"request": request, "breeds": breeds, "menu": menu})

@router.post("/add_kitten", response_class=RedirectResponse, name="create_kitten",
             summary="Create a New Kitten",
             description="Create a new kitten and add it to the database.")
async def create_kitten(
    request: Request,
    nickname: str = Form(...),
    name: str = Form(...),
    color: str = Form(...),
    age_months: int = Form(...),
    description: str = Form(...),
    breed_id: int = Form(...),
    db: Session = Depends(get_db)
):
    breeds = db.query(CatBreed).all()
    existing_kitten = db.query(Kitten).filter(Kitten.nickname == nickname).first()
    if existing_kitten:
        if existing_kitten.is_active:
            return templates.TemplateResponse("add_kitten.html", {
                "request": request,
                "nickname": nickname,
                "name": name,
                "description": description,
                "breed_id": breed_id,
                "age_months": age_months,
                "breeds": breeds,
                "error_message": f"A kitten with the code '{nickname}' already exists!"
            })
        else:
            existing_kitten.is_active = True
            db.commit()
            return RedirectResponse(url="/kittens", status_code=303)
    new_kitten = Kitten(
        name=name,
        color=color,
        age_months=age_months,
        breed_id=breed_id,
        nickname=nickname,
        description=description)
    db.add(new_kitten)
    db.commit()
    return RedirectResponse(url="/kittens", status_code=303)

@router.get("/add_breed", response_class=HTMLResponse, name="add_breed",
            summary="Add New Breed Form",
            description="Render the form for adding a new cat breed.")
async def add_breed(request: Request):
    return templates.TemplateResponse("add_breed.html", {"request": request})

@router.post("/add_breed", response_class=RedirectResponse, name="create_breed",
             summary="Create a New Breed",
             description="Create a new breed and add it to the database.")
async def create_breed(
    request: Request,
    name: str = Form(...),
    type: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_breed = db.query(CatBreed).filter(CatBreed.name == name).first()

    if existing_breed:
        if existing_breed.is_active:
            return templates.TemplateResponse("add_breed.html", {
                "request": request,
                "name": name,
                "type": type,
                "description": description,
                "error_message": f"A breed with the name '{name}' already exists!"
            })
        else:

            existing_breed.is_active = True
            existing_breed.type = type
            existing_breed.description = description
            db.commit()
            return RedirectResponse(url="/breeds", status_code=303)

    new_breed = CatBreed(name=name, type=type, description=description, is_active=True)
    db.add(new_breed)
    db.commit()
    return RedirectResponse(url="/breeds", status_code=303)

# --- End Adding items routes  ---

# --- Updating items routes  ---

@router.get("/update_kitten/{kitten_id}", response_class=HTMLResponse, name="update_kitten",
            summary="Update Kitten Form",
            description="Render the form to update an existing kitten's information.")
async def update_kitten(request: Request, kitten_id: int, db: Session = Depends(get_db)):
    kitten = db.query(Kitten).filter(Kitten.id == kitten_id).first()
    if not kitten:
        return RedirectResponse(url="/kittens", status_code=303)

    breeds = db.query(CatBreed).all()

    return templates.TemplateResponse("update_kitten.html", {
        "request": request,
        "kitten": kitten,
        "breeds": breeds,
        "menu": menu
    })

@router.post("/update_kitten/{kitten_id}", response_class=RedirectResponse, name="update_kitten_action",
             summary="Update Kitten",
             description="Process the update of an existing kitten's information.")
async def process_update_kitten(
    kitten_id: int,
    name: str = Form(...),
    color: str = Form(...),
    age_months: int = Form(...),
    description: str = Form(...),
    breed_id: int = Form(...),
    db: Session = Depends(get_db)
):
    kitten = db.query(Kitten).filter(Kitten.id == kitten_id).first()
    if kitten:
        kitten.name = name
        kitten.color = color
        kitten.age_months = age_months
        kitten.description = description
        kitten.breed_id = breed_id
        db.commit()

    return RedirectResponse(url="/kittens", status_code=303)

@router.get("/update_breed/{breed_id}", response_class=HTMLResponse, name="update_breed",
            summary="Update Breed Form",
            description="Render the form to update an existing breed's information.")
async def update_breed(request: Request, breed_id: int, db: Session = Depends(get_db)):
    breed = db.query(CatBreed).filter(CatBreed.id == breed_id).first()
    if not breed:
        return RedirectResponse(url="/breeds", status_code=303)

    return templates.TemplateResponse("update_breed.html", {"request": request, "breed": breed})

@router.post("/update_breed/{breed_id}", response_class=RedirectResponse, name="update_breed_action",
             summary="Update Breed",
             description="Process the update of an existing breed's information.")
async def process_update_breed(
    breed_id: int,
    name: str = Form(...),
    type: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db)
):
    breed = db.query(CatBreed).filter(CatBreed.id == breed_id).first()
    if breed:
        breed.name = name
        breed.type = type
        breed.description = description
        db.commit()

    return RedirectResponse(url="/breeds", status_code=303)

# --- End Updating items routes  ---

# --- Deleting items routes  ---

@router.get("/delete_kitten/{kitten_id}", response_class=HTMLResponse,
            summary="Delete Kitten Confirmation",
            description="Render the confirmation page for deleting a kitten.")
async def delete_kitten(request: Request, kitten_id: int, db: Session = Depends(get_db)):
    kitten = db.query(Kitten).filter(Kitten.id == kitten_id).first()
    if not kitten:
        raise HTTPException(status_code=404, detail="Kitten not found")

    return templates.TemplateResponse("confirm_delete_kitten.html", {
        "request": request,
        "kitten": kitten
    })

@router.post("/delete_kitten/{kitten_id}",
             summary="Delete Kitten",
             description="Delete a kitten from the database.")
async def delete_kitten_action(kitten_id: int, db: Session = Depends(get_db)):
    kitten = db.query(Kitten).filter(Kitten.id == kitten_id).first()
    if not kitten:
        raise HTTPException(status_code=404, detail="Kitten not found")

    kitten.is_active = False
    db.commit()

    return RedirectResponse(url="/kittens", status_code=303)


@router.get("/delete_breed/{breed_id}", response_class=HTMLResponse,
            summary="Delete Breed Confirmation",
            description="Render the confirmation page for deleting a breed.")
async def delete_breed(request: Request, breed_id: int, db: Session = Depends(get_db)):
    breed = db.query(CatBreed).filter(CatBreed.id == breed_id).first()
    if not breed:
        raise HTTPException(status_code=404, detail="Breed not found")

    return templates.TemplateResponse("confirm_delete_breed.html", {"request": request, "breed": breed})


@router.post("/delete_breed/{breed_id}",
             summary="Delete Breed",
             description="Delete a breed from the database.")
async def delete_breed_action(breed_id: int, db: Session = Depends(get_db)):
    breed = db.query(CatBreed).filter(CatBreed.id == breed_id).first()
    if not breed:
        raise HTTPException(status_code=404, detail="Breed not found")

    breed.is_active = False
    db.commit()

    return RedirectResponse(url="/breeds", status_code=303)

# --- End Deleting items routes  ---
