# backend/main.py
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Carrega .env
load_dotenv(Path(__file__).parent.parent / ".env")

# Adiciona o diretório backend ao path
sys.path.insert(0, str(Path(__file__).parent))

from rotas.cnab import router as cnab_router
from rotas.contas_pagar import router as contas_pagar_router

# =============================================================================
# APLICAÇÃO
# =============================================================================

app = FastAPI(
    title="CNAB Coopluiza - API",
    description="Gerador de remessas CNAB 240 Santander Pagfor PIX",
    version="1.0.0",
)

# CORS - permite que o frontend (mesmo localhost) chame a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restringir para o IP/domínio da intranet
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# ROTAS DA API
# =============================================================================

app.include_router(cnab_router)
app.include_router(contas_pagar_router)


@app.get("/", tags=["Status"])
def health_check():
    return {
        "status": "online",
        "sistema": "CNAB Coopluiza",
        "versao": "1.0.0",
        "docs": "/docs",
    }



# =============================================================================
# SERVIR MODELOS DE PLANILHA
# =============================================================================
modelos_path = Path(__file__).parent.parent / "modelos_planilhas"

@app.get("/modelos/emprestimo", tags=["Modelos"])
def modelo_emprestimo():
    f = modelos_path / "modelo_emprestimo.xlsx"
    if not f.exists():
        raise HTTPException(status_code=404, detail="Modelo não encontrado")
    return FileResponse(str(f), filename="modelo_emprestimo.xlsx",
              media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

@app.get("/modelos/beneficio", tags=["Modelos"])
def modelo_beneficio():
    f = modelos_path / "modelo_beneficio.xlsx"
    if not f.exists():
        raise HTTPException(status_code=404, detail="Modelo não encontrado")
    return FileResponse(str(f), filename="modelo_beneficio.xlsx",
              media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# =============================================================================
# SERVIR O FRONTEND (arquivos estáticos)
# =============================================================================

frontend_path = Path(__file__).parent.parent / "frontend"

if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path / "assets")), name="static")

    @app.get("/app", include_in_schema=False)
    def servir_frontend():
        return FileResponse(str(frontend_path / "index.html"))


# =============================================================================
# INICIALIZAÇÃO DIRETA
# =============================================================================

if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    print("=" * 60)
    print("  CNAB Coopluiza - Servidor iniciando...")
    print(f"  Acesse: http://localhost:{port}")
    print(f"  Documentação da API: http://localhost:{port}/docs")
    print("=" * 60)

    uvicorn.run("main:app", host=host, port=port, reload=True)