from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Request, APIRouter
from fastapi.responses import JSONResponse
from typing import List

from connection_db import init_db, get_session
from mental_health import MentalHealth, MentalHealthCreate, MentalHealthUpdate, MentalHealthResponse
from social_media import SocialMedia, SocialMediaCreate, SocialMediaUpdate, SocialMediaResponse
from mental_health_operations import MentalHealthOperations
from social_media_operations import SocialMediaOperations

router = APIRouter()

@router.get("/")
@router.head("/")
async def root():
    return {"message": "API de Salud Mental y Redes Sociales"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
# ===============================
# Endpoints de Salud Mental
# ===============================

@app.post("/mental_health/", response_model=MentalHealthResponse, status_code=status.HTTP_201_CREATED)
async def create_mental_health(entry: MentalHealthCreate):
    async for session in get_session():
        try:
            return await MentalHealthOperations.create_mental_health(session, entry.dict())
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail=str(e))


@app.get("/mental_health/", response_model=List[MentalHealthResponse])
async def get_all_mental_health():
    async for session in get_session():
        return await MentalHealthOperations.get_all_mental_health(session)


@app.get("/mental_health/{entry_id}", response_model=MentalHealthResponse)
async def get_mental_health(entry_id: int):
    async for session in get_session():
        result = await MentalHealthOperations.get_mental_health_by_id(session, entry_id)
        if not result:
            raise HTTPException(status_code=404, detail="Registro de salud mental no encontrado")
        return result


@app.put("/mental_health/{entry_id}", response_model=MentalHealthResponse)
async def update_mental_health(entry_id: int, update_data: MentalHealthUpdate):
    async for session in get_session():
        try:
            result = await MentalHealthOperations.update_mental_health(session, entry_id, update_data.dict(exclude_unset=True))
            if not result:
                raise HTTPException(status_code=404, detail="El registro de salud mental no fue actualizado")
            return result
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail=str(e))


@app.delete("/mental_health/{entry_id}", response_model=MentalHealth)
async def delete_mental_health(entry_id: int):
    async for session in get_session():
        try:
            deleted = await MentalHealthOperations.delete_mental_health(session, entry_id)
            if not deleted:
                raise HTTPException(status_code=404, detail="El registro de salud mental no fue eliminado")
            return deleted
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail=str(e))


@app.get("/mental_health/search_by_age/", response_model=List[MentalHealthResponse])
async def search_by_age(age: int):
    async for session in get_session():
        result = await MentalHealthOperations.search_mental_health_by_age(session, age)
        if not result:
            raise HTTPException(status_code=404, detail=f"No se encontraron registros para edad {age}")
        return result


@app.get("/mental_health/filter_by_sleep_issues/", response_model=List[MentalHealthResponse])
async def filter_by_sleep_issues():
    async for session in get_session():
        result = await MentalHealthOperations.filter_by_sleep_issues(session)
        if not result:
            raise HTTPException(status_code=404, detail="No se encontraron registros.")
        return result


# ===============================
# Endpoints de Redes Sociales
# ===============================

@app.post("/social_media/", response_model=SocialMediaResponse, status_code=status.HTTP_201_CREATED)
async def create_social_media(entry: SocialMediaCreate):
    async for session in get_session():
        try:
            return await SocialMediaOperations.create(session, entry)
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail=str(e))


@app.get("/social_media/", response_model=List[SocialMediaResponse])
async def get_all_social_media():
    async for session in get_session():
        return await SocialMediaOperations.read_all(session)


@app.get("/social_media/{entry_id}", response_model=SocialMediaResponse)
async def get_social_media(entry_id: int):
    async for session in get_session():
        result = await SocialMediaOperations.read_one(session, entry_id)
        if not result:
            raise HTTPException(status_code=404, detail="Registro de redes sociales no encontrado")
        return result


@app.put("/social_media/{entry_id}", response_model=SocialMediaResponse)
async def update_social_media(entry_id: int, update_data: SocialMediaUpdate):
    async for session in get_session():
        try:
            result = await SocialMediaOperations.update(session, entry_id, update_data)
            if not result:
                raise HTTPException(status_code=404, detail="El registro de redes sociales no fue actualizado")
            return result
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail=str(e))


@app.delete("/social_media/{entry_id}", response_model=SocialMedia)
async def delete_social_media(entry_id: int):
    async for session in get_session():
        try:
            deleted = await SocialMediaOperations.delete(session, entry_id)
            if not deleted:
                raise HTTPException(status_code=404, detail="El registro de redes sociales no fue eliminado")
            return deleted
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail=str(e))


@app.get("/social_media/search_by_gender/", response_model=List[SocialMediaResponse])
async def search_by_gender(gender: str):
    async for session in get_session():
        result = await SocialMediaOperations.search_by_gender(session, gender)
        if not result:
            raise HTTPException(status_code=404, detail=f"No se encontraron registros con género: {gender}")
        return result


@app.get("/social_media/filter_by_age/", response_model=List[SocialMediaResponse])
async def filter_by_age():
    async for session in get_session():
        result = await SocialMediaOperations.filter_by_age(session)
        if not result:
            raise HTTPException(status_code=404, detail="No se encontraron registros.")
        return result

# =====================================================
# Manejo personalizado de errores
# =====================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "msg": "¡Ha ocurrido un error!",
            "detail": exc.detail,
            "path": str(request.url)
        }
    )

# --- Endpoints básicos ---
@app.get("/")
async def root():
    return {"message": "API de Salud Mental y Redes Sociales"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hola {name}, bienvenido al sistema de gestión"}
