from fastapi import FastAPI, HTTPException

app = FastAPI()

tasks = []

# task = {"id": int, "title": str, "description": str, "completed": bool}


@app.get("/tasks/", summary="Получить список задач", description="Возвращает все задачи")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", summary="Получить задачу по ID", description="Возвращает задачу по её идентификатору")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
        else:
            HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks/", summary="Создать новую задачу", description="Добавляет новую задачу в список")
def create_task(title: str, description: str = ""):
    task_id = len(tasks) + 1
    new_task = {
        "id": task_id,
        "title": title,
        "description": description,
        "completed": False
    }
    tasks.append(new_task)
    return new_task


@app.put("/tasks/{task_id}", summary="Обновить задачу", description="Обновляет информацию о задаче по ID")
def update_task(task_id: int, title: str = None, description: str = None, completed: bool = None):
    for task in tasks:
        if task["id"] == task_id:
            if title is not None:
                task["title"] = title
            if description is not None:
                task["description"] = description
            if completed is not None:
                task["completed"] = completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", summary="Удалить задачу", description="Удаляет задачу по её ID")
def delete_task(task_id: int):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return {"message": "Task deleted successfully"}