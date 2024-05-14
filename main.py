from fastapi import FastAPI
from api.endpoints import auth, tasks
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=['auth'])
app.include_router(tasks.router, tags = ["tasks"])




if __name__ == "__main__":
    import uvicorn 
    uvicorn.run("main:app", host= "0.0.0.0", port= 8000, reload=True)