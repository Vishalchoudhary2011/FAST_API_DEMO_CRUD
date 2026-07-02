from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
todolist =[]

class Todo(BaseModel):
    id: int
    title:str
    description: str
    status:bool

#Create API 
@app.post("/todos")
def create_todo(todo:Todo):
    todolist.append(todo)
    return { "message" : "TODO is created", "data" : todo}

# Get API
@app.get("/todos")
def get_todo():
    return todolist

# Get one API
@app.get("/todos/{todo_id}")
def get_todo(todo_id:int):
    for todo in todolist:
        if todo.id == todo_id:
            return todo
    return {"error": "TODO not found"}
    
# Update API     
@app.put("/update_todo/{todo_id}")
def update_todo(todo_id:int, update_todo:Todo):
    for index, todo in enumerate(todolist):
        if todo.id == todo_id:
            todolist[index] = update_todo
            return {
                "message": "Data updated", 
                "data": update_todo
                }   
    return { "error" : "Todo not found"}

# Delete API
@app.delete("/update_todo/{todo_id}")
def delete_todo(todo_id:int):
    for index, todo in enumerate(todolist):
        print(todo.id, "===", todo_id)

        if todo.id == todo_id:
            todolist.pop(index)
            return {"Data deleted Successfully"}
        
    return { "error" : "Todo not found"}

     


   



