from pydantic import BaseModel, Field
import datetime

# Modèle de base pour une tâche Todo
class Todo(BaseModel):
    title: str
    completed: bool = False

# Modèle pour retourner l'identifiant d'une tâche
class TodoId(BaseModel):
    id: str

# Modèle complet d'une tâche avec dates de création et de mise à jour
class TodoRecord(TodoId, Todo):
    created_at: datetime.datetime
    updated_at: datetime.datetime