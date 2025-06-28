from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.database import engine, Base
from app.api.v1 import auth, users, mentors, matches

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mentor-Mentee Matching API",
    description="API for matching mentors and mentees in a mentoring platform",
    version="1.0.0",
    contact={
        "name": "Mentor-Mentee Matching App"
    },
    license_info={
        "name": "MIT"
    }
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving
app.mount("/static", StaticFiles(directory="static"), name="static")

# Register API routers
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(mentors.router, prefix="/api", tags=["Mentors"])
app.include_router(matches.router, prefix="/api", tags=["Matches"])


@app.get("/")
async def root():
    return {"message": "Mentor-Mentee Matching API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
