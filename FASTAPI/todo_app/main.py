from fastapi import FastAPI, HTTPException
## motor permet d'interagir avec MongoDB de manière asynchrone
from motor.motor_asyncio import AsyncIOMotorClient
import datetime
## typing permet de spécifier les types des listes
from typing import List
## bson permet de manipuler les ObjectId de MongoDB
from bson import ObjectId
from models import Todo, TodoId, TodoRecord

### Utile de fournir les variables d'environnement pour la connexion à la base de données
from dotenv import load_dotenv
import os

# Connexion à la base de données MongoDB avec un fichier .env
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
db_client = AsyncIOMotorClient(MONGO_URI)

db = db_client.todo_app

# Création de l'application FastAPI
app = FastAPI(
    title="Todo App API",
    description="Une API simple de gestion de tâches avec FastAPI et MongoDB",
    version="1.0.0",
    docs_url="/",
)

@app.get("/todos", response_model=List[TodoRecord])
async def get_todos():
    """
    Récupère toutes les tâches Todo de la base de données.
    """
    todos = []
    async for todo in db.todos.find():
        todos.append(TodoRecord(
            id=str(todo["_id"]),
            title=todo["title"],
            completed=todo["completed"],
            created_at=todo["created_at"],
            updated_at=todo["updated_at"]
        ))
    return todos


@app.get("/todos/{todo_id}", response_model=TodoRecord)
async def get_todo(todo_id):
    """
    Récupère une tâche Todo spécifique par son identifiant.
    """
    todo = await db.todos.find_one({"_id": ObjectId(todo_id)})
    if not todo:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    
    return TodoRecord(
        id=str(todo["_id"]),
        title=todo["title"],
        completed=todo["completed"],
        created_at=todo["created_at"],
        updated_at=todo["updated_at"]
    )



# Route pour créer une nouvelle tâche
@app.post("/todos", response_model=TodoId)
async def create_todo(payload: Todo):
    """
    Crée une nouvelle tâche Todo dans la base de données.
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    # Insertion de la tâche dans la collection 'todos'
    insert_result = await db.todos.insert_one(
        {
            "title": payload.title,
            "completed": payload.completed,
            "created_at": now,
            "updated_at": now
        }
    )
    # Retourne l'identifiant de la tâche créée
    return TodoId(id=str(insert_result.inserted_id))



@app.put("/todos/{todo_id}", response_model=TodoRecord)
async def update_todo(todo_id: str, payload: Todo):
    """
    Met à jour une tâche Todo existante.
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    update_result = await db.todos.update_one(
        {"_id": ObjectId(todo_id)},
        {
            "$set": {
                "title": payload.title,
                "completed": payload.completed,
                "updated_at": now
            }
        }
    )
    
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Tâche non trouvée ou aucune modification apportée")
    
    updated_todo = await db.todos.find_one({"_id": ObjectId(todo_id)})
    
    return TodoRecord(
        id=str(updated_todo["_id"]),
        title=updated_todo["title"],
        completed=updated_todo["completed"],
        created_at=updated_todo["created_at"],
        updated_at=updated_todo["updated_at"]
    )


@app.delete("/todos/{todo_id}", response_model=TodoId)
async def delete_todo(todo_id):
    """
    Supprime une tâche Todo de la base de données.
    """
    delete_result = await db.todos.delete_one({"_id": ObjectId(todo_id)})
    
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    
    return TodoId(id=todo_id)

# Point d'entrée pour lancer le serveur en mode développement uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)