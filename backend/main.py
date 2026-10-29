from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers import navigation, playlist, editing, statistics

app = FastAPI()


@app.exception_handler(LookupError)
async def not_found_handler(request: Request, exc: LookupError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

# frontend is opened from file:// or a local dev server, so allow any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(playlist.router)
app.include_router(navigation.router)
app.include_router(editing.router)
app.include_router(statistics.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
