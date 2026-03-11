# backend/rotas/cnab.py
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from modelos.emprestimo import RemessaEmprestimo
from modelos.beneficio import RemessaBeneficio
from servicos.gerador_cnab import gerar_cnab, listar_historico, HISTORICO_PATH
from servicos.leitor_excel import ler_excel

router = APIRouter(prefix="/cnab", tags=["CNAB"])


# =============================================================================
# GERAR VIA JSON (formulário manual)
# =============================================================================

@router.post("/emprestimo")
def gerar_cnab_emprestimo(remessa: RemessaEmprestimo):
    """Gera CNAB de empréstimo a partir de dados JSON (formulário manual)."""
    try:
        pagamentos = [p.to_dict() for p in remessa.pagamentos]
        resultado = gerar_cnab(pagamentos, tipo="emprestimo", seq_manual=remessa.seq_arquivo)
        return {"sucesso": True, **resultado}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/beneficio")
def gerar_cnab_beneficio(remessa: RemessaBeneficio):
    """Gera CNAB de benefício a partir de dados JSON (formulário manual)."""
    try:
        pagamentos = [p.to_dict() for p in remessa.pagamentos]
        resultado = gerar_cnab(pagamentos, tipo="beneficio", seq_manual=remessa.seq_arquivo)
        return {"sucesso": True, **resultado}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# GERAR VIA UPLOAD DE EXCEL
# =============================================================================

@router.post("/emprestimo/upload-excel")
async def upload_excel_emprestimo(
    arquivo: UploadFile = File(...),
    data_pagamento: str = Form(...),   # DD/MM/YYYY
):
    """Gera CNAB de empréstimo a partir de planilha Excel."""
    if not arquivo.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Envie um arquivo .xlsx ou .xls")

    conteudo = await arquivo.read()

    try:
        leitura = ler_excel(conteudo, data_pagamento)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not leitura["pagamentos"]:
        raise HTTPException(status_code=400, detail="Nenhum pagamento válido encontrado na planilha.")

    resultado = gerar_cnab(leitura["pagamentos"], tipo="emprestimo")

    return {
        "sucesso": True,
        **resultado,
        "erros_planilha": leitura["erros"],
    }


@router.post("/beneficio/upload-excel")
async def upload_excel_beneficio(
    arquivo: UploadFile = File(...),
    data_pagamento: str = Form(...),   # DD/MM/YYYY
):
    """Gera CNAB de benefício a partir de planilha Excel."""
    if not arquivo.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Envie um arquivo .xlsx ou .xls")

    conteudo = await arquivo.read()

    try:
        leitura = ler_excel(conteudo, data_pagamento)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not leitura["pagamentos"]:
        raise HTTPException(status_code=400, detail="Nenhum pagamento válido encontrado na planilha.")

    resultado = gerar_cnab(leitura["pagamentos"], tipo="beneficio")

    return {
        "sucesso": True,
        **resultado,
        "erros_planilha": leitura["erros"],
    }


# =============================================================================
# HISTÓRICO E DOWNLOAD
# =============================================================================

@router.get("/historico")
def historico():
    """Lista todos os arquivos CNAB gerados."""
    return {"arquivos": listar_historico()}


@router.get("/download/{nome_arquivo}")
def download(nome_arquivo: str):
    """Faz download de um arquivo CNAB do histórico."""
    caminho = HISTORICO_PATH / nome_arquivo

    if not caminho.exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")

    # Segurança: evita path traversal
    if not str(caminho.resolve()).startswith(str(HISTORICO_PATH.resolve())):
        raise HTTPException(status_code=403, detail="Acesso negado.")

    return FileResponse(
        path=str(caminho),
        filename=nome_arquivo,
        media_type="text/plain",
    )