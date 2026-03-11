# backend/servicos/gerador_cnab.py
import json
import os
from datetime import datetime
from pathlib import Path

# Caminho do contador sequencial
CONTADOR_PATH = Path(__file__).parent.parent / "contador_seq.json"
HISTORICO_PATH = Path(__file__).parent.parent / "historico"

# Garante que a pasta histórico existe
HISTORICO_PATH.mkdir(exist_ok=True)


def _ler_seq() -> int:
    """Lê o número sequencial atual do arquivo."""
    if CONTADOR_PATH.exists():
        try:
            with open(CONTADOR_PATH) as f:
                conteudo = f.read().strip()
                if conteudo:
                    return json.loads(conteudo).get("seq", 1)
        except (json.JSONDecodeError, ValueError):
            pass  # arquivo vazio ou corrompido, recria abaixo
    # Primeira vez ou arquivo inválido: pega do .env ou começa em 1
    seq_env = int(os.getenv("SEQ_ARQUIVO", "1"))
    _salvar_seq(seq_env)
    return seq_env


def _salvar_seq(seq: int):
    """Salva o número sequencial atual."""
    with open(CONTADOR_PATH, "w") as f:
        json.dump({"seq": seq, "atualizado_em": datetime.now().isoformat()}, f)


def proximo_seq() -> int:
    """Retorna o próximo sequencial e já incrementa o contador."""
    seq = _ler_seq()
    _salvar_seq(seq + 1)
    return seq


def gerar_cnab(pagamentos_dict: list, tipo: str, seq_manual: int = None) -> dict:
    """
    Gera o arquivo CNAB e salva no histórico.

    Args:
        pagamentos_dict: lista de dicts prontos para o motor_cnab
        tipo: "emprestimo" ou "beneficio"
        seq_manual: se informado, usa esse número em vez do automático

    Returns:
        dict com nome_arquivo, caminho, seq_usado, total, qtd
    """
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from motor_cnab import gerar_arquivo_cnab

    seq = seq_manual if seq_manual is not None else proximo_seq()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"CNAB_{tipo.upper()}_{timestamp}.txt"
    caminho_completo = HISTORICO_PATH / nome_arquivo

    gerar_arquivo_cnab(pagamentos_dict, str(caminho_completo), seq_arquivo=seq)

    total = sum(p["valor"] for p in pagamentos_dict)

    return {
        "nome_arquivo": nome_arquivo,
        "caminho": str(caminho_completo),
        "seq_usado": seq,
        "total": round(total, 2),
        "qtd_pagamentos": len(pagamentos_dict),
        "tipo": tipo,
        "gerado_em": datetime.now().isoformat(),
    }


def listar_historico() -> list:
    """Lista todos os arquivos CNAB gerados."""
    arquivos = []
    for f in sorted(HISTORICO_PATH.glob("*.txt"), reverse=True):
        stat = f.stat()
        arquivos.append({
            "nome": f.name,
            "tamanho_bytes": stat.st_size,
            "gerado_em": datetime.fromtimestamp(stat.st_mtime).strftime("%d/%m/%Y %H:%M:%S"),
        })
    return arquivos