# backend/servicos/api_sistema.py
# =============================================================================
# 🔜 FUTURO - Integração com API interna (Contas a Pagar)
# =============================================================================
# Este arquivo está preparado para receber as credenciais e a lógica
# de envio quando você passar os detalhes da API.
#
# Para ativar:
# 1. Preencha as variáveis no .env
# 2. Implemente autenticar() e enviar_pagamentos()
# =============================================================================

import os
import httpx
from datetime import datetime


API_URL = os.getenv("API_SISTEMA_URL", "")
API_USUARIO = os.getenv("API_SISTEMA_USUARIO", "")
API_SENHA = os.getenv("API_SISTEMA_SENHA", "")


async def autenticar() -> str:
    """
    Autentica na API interna e retorna o token.
    Implementar quando tiver as credenciais.
    """
    raise NotImplementedError("Integração com API interna ainda não configurada.")

    # Exemplo de como será:
    # async with httpx.AsyncClient() as client:
    #     resp = await client.post(f"{API_URL}/auth/login", json={
    #         "usuario": API_USUARIO,
    #         "senha": API_SENHA
    #     })
    #     resp.raise_for_status()
    #     return resp.json()["token"]


async def enviar_pagamentos(pagamentos: list, token: str) -> dict:
    """
    Envia os pagamentos para o contas a pagar do sistema interno.
    Implementar quando tiver a documentação da API.
    """
    raise NotImplementedError("Integração com API interna ainda não configurada.")

    # Exemplo de como será:
    # async with httpx.AsyncClient() as client:
    #     resp = await client.post(
    #         f"{API_URL}/contas-pagar/lote",
    #         headers={"Authorization": f"Bearer {token}"},
    #         json={"pagamentos": pagamentos, "origem": "CNAB_BENEFICIO"}
    #     )
    #     resp.raise_for_status()
    #     return resp.json()
