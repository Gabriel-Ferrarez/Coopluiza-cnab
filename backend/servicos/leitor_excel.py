# backend/servicos/leitor_excel.py
import pandas as pd
from datetime import datetime
from io import BytesIO


COLUNAS_OBRIGATORIAS = ["Nome", "CPF", "Banco", "Agencia", "Conta", "DV", "Valor", "Documento"]


def ler_excel(conteudo_bytes: bytes, data_pagamento_str: str = None) -> dict:
    """
    Lê um arquivo Excel e retorna lista de pagamentos validados.

    Args:
        conteudo_bytes: conteúdo do arquivo .xlsx em bytes
        data_pagamento_str: data no formato DD/MM/YYYY (se None, usa hoje)

    Returns:
        dict com 'pagamentos' (lista) e 'erros' (lista de linhas com problema)
    """
    if data_pagamento_str is None:
        data_pagamento_str = datetime.now().strftime("%d/%m/%Y")

    try:
        df = pd.read_excel(BytesIO(conteudo_bytes), dtype=str)
    except Exception as e:
        raise ValueError(f"Erro ao abrir Excel: {e}")

    # Valida colunas obrigatórias
    faltando = [c for c in COLUNAS_OBRIGATORIAS if c not in df.columns]
    if faltando:
        raise ValueError(f"Colunas faltando na planilha: {', '.join(faltando)}")

    pagamentos = []
    erros = []

    for idx, row in df.iterrows():
        linha_num = idx + 2  # linha 1 = cabeçalho

        # Pula linhas vazias
        if pd.isna(row.get("Nome")) or pd.isna(row.get("Valor")):
            continue

        try:
            valor_str = (
                str(row["Valor"])
                .replace("R$", "")
                .replace(" ", "")
                .replace(".", "")
                .replace(",", ".")
            )
            valor = float(valor_str)

            if valor <= 0:
                raise ValueError("Valor deve ser maior que zero")

            pagamentos.append({
                "nome": str(row["Nome"]).strip().upper(),
                "cpf_cnpj": str(row["CPF"]).strip(),
                "banco": str(row["Banco"]).strip(),
                "agencia": str(row["Agencia"]).strip(),
                "conta": str(row["Conta"]).strip(),
                "dv_conta": str(row["DV"]).strip() if not pd.isna(row.get("DV")) else "0",
                "valor": valor,
                "documento": str(row["Documento"]).strip() if not pd.isna(row.get("Documento")) else "",
                "data_pagamento": datetime.strptime(data_pagamento_str, "%d/%m/%Y"),
            })

        except Exception as e:
            erros.append({"linha": linha_num, "nome": str(row.get("Nome", "?")), "erro": str(e)})

    return {"pagamentos": pagamentos, "erros": erros}
