# backend/rotas/contas_pagar.py
# =============================================================================
# 🔜 FUTURO - Rota de envio para Contas a Pagar
# =============================================================================
from fastapi import APIRouter, HTTPException
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

router = APIRouter(prefix="/contas-pagar", tags=["Contas a Pagar (Futuro)"])


@router.post("/enviar/{nome_arquivo}")
async def enviar_para_contas_pagar(nome_arquivo: str):
    """
    🔜 FUTURO: Envia os pagamentos de benefício diretamente para o
    contas a pagar do sistema interno via API.

    Quando você passar as credenciais e documentação da API,
    este endpoint será implementado aqui.
    """
    raise HTTPException(
        status_code=501,
        detail="Integração com API interna ainda não configurada. Em breve!"
    )


@router.get("/status/{id_envio}")
async def status_envio(id_envio: str):
    """🔜 FUTURO: Consulta o status de um envio para contas a pagar."""
    raise HTTPException(
        status_code=501,
        detail="Integração com API interna ainda não configurada. Em breve!"
    )
