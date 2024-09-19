from fastapi.responses import RedirectResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import user, knowledge, file, chatbot, llm, message, socket, embedding
import uvicorn


app = FastAPI()
app_2 = FastAPI()
app_3 = FastAPI()


app.include_router(user.router)
app.include_router(knowledge.router)
app.include_router(file.router)
app.include_router(chatbot.router)
app.include_router(llm.router)
app.include_router(message.router)  
app_2.include_router(socket.router)
app_3.include_router(embedding.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app_2.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app_3.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",port=8000,reload=False)
    # uvicorn.run("main:app_2", host="0.0.0.0",port=8500,reload=False)
    # uvicorn.run("main:app_3", host="0.0.0.0",port=9000,reload=False, workers=4)
    
