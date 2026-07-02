from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

#Table Model
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create API
@app.post("/todos")
def create_todo(title:str, description=str, db:Session = Depends(get_db)):
    todo = Todo(title=title,description=description,completed=False)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {
        "message" : "Data Created",
        "data": todo
    }

# Get ALL 

@app.get("/todos")
def get_all(db:Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return {
        "Total": len(todos),
        "data": todos
    }

# Get One
@app.get("/todos/{todo_id}")
def get_todo(todo_id= int, db:Session= Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="TODO not Found")
    return todo

#Update API
@app.put("/todos/{todo_id}")
def update_todo(todo_id:int, title:str, description:str, db:Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.title = title
    todo.description = description
    db.commit()
    db.refresh(todo)
    return {
        "message" : "Todo is updated Succesfully",
        "data" : todo
    }

#Delete API
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int, db:Session= Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo is not found")
    
    db.delete(todo)
    db.commit()

    return {
        "message": "Todo deleted successfully"
    }

