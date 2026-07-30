import logging

import httpx
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app import schemas, crud


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/contact", tags=["Contact"])

# 
N8N_WEBHOOK_URL = settings.n8n_webhook_url

# Função para notificar o n8n de forma assíncrona
async def notify_n8n(payload: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                N8N_WEBHOOK_URL, json=payload, timeout=10.0
            )
            response.raise_for_status()
            logger.info("n8n notificado com sucesso para: %s", payload.get("email"))
        except httpx.HTTPStatusError as e:
            logger.error(
                "n8n retornou erro HTTP %s para %s: %s",
                e.response.status_code,
                payload.get("email"),
                e,
            )
        except Exception as e:
            logger.error("Erro ao notificar n8n para %s: %s", payload.get("email"), e)


@router.post("", response_model=schemas.ContactMessageResponse, status_code=201)
def create_contact(
    payload: schemas.ContactMessageCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    try:
        contact = crud.create_contact_message(db, payload)
        # Envia notificação para o n8n em background, sem bloquear a resposta
        background_tasks.add_task(notify_n8n, payload.model_dump())
        return contact
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao salvar mensagem: {exc}"
        )
          


@router.get("", response_model=list[schemas.ContactMessageResponse])
def list_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_contact_messages(db, skip=skip, limit=limit)
