from fastapi import FastAPI, BackgroundTasks, HTTPException,Depends, Request
from pydantic import BaseModel, field_validator
from models import User, TranslationalModel
from auth import get_password_hash, verify_password, create_access_token,get_current_user
from fastapi.security import OAuth2PasswordRequestForm
import tasks
import time
import logging


app = FastAPI()

languages = [
    'english', 'french', 'spanish', 'german', 'italian', 
    'hindi', 'chinese', 'japanese', 'arabic', 'russian'
]

class Translation(BaseModel):
    text: str
    base_lang: str
    final_lang: str

    @field_validator('base_lang', 'final_lang')
    def valid_lang(cls, lang: str) -> str:
        lang = lang.strip().lower()  
        if lang not in languages:
            raise ValueError(f"Invalid language. Supported: {', '.join(languages)}")
        return lang  

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app_monitor.log"), # Writes to file
        logging.StreamHandler()                # prints to terminal
    ]
)
logger = logging.getLogger("monitor_requests")


@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"IP: {request.client.host} | Method: {request.method} | "
        f"Path: {request.url.path} | Status: {response.status_code} | "
        f"Duration: {process_time:.4f}s"
    )
    return response


@app.post("/signup")
def signup(username: str, password: str):
    hashed = get_password_hash(password)
    try:
        User.create(username=username, hashed_password=hashed)
        return {"message": "User created successfully"}
    except:
        raise HTTPException(status_code=400, detail="Username already exists")

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = User.get_or_none(User.username == form_data.username)
       
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
       
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/translate")
def post_translation(t: Translation, current_user: str = Depends(get_current_user)): 
    t_id = tasks.store_translation(t, current_user)
    tasks.run_translation.delay(t_id)
    return {'task_id': t_id}

@app.get("/results")
def get_translation(t_id: int, current_user: str = Depends(get_current_user)):
    return {'translation': tasks.find_translation(t_id)}