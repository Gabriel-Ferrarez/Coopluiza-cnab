# motor_cnab.py
import re
from datetime import datetime

# =============================================================================
# ⚙️ CONFIGURAÇÕES DA SUA EMPRESA (FIXAS)
# =============================================================================
BANCO = "033"
AGENCIA = "0009"
CONTA = "13006934"      
DV_CONTA = "1"         
CNPJ = "02093154000109"
EMPRESA = "COOPLUIZA - FRANCA -SP"           # ← CORRIGIDO
NOME_BANCO = "SANTANDER (BRASIL) S.A."        # ← CORRIGIDO
CONVENIO_COMPLETO = "00334188004901695802"    # Código JWP5

# Endereço da empresa (header lote)
LOGRADOURO   = "RUA DO COMERCIO"
NUM_END      = "000002"
COMPLEMENTO  = "Andar"      # 15 chars: "  Andar       " -> ajustado abaixo
CIDADE       = "FRANCA"
CEP          = "14400660"   # ← CORRIGIDO (era 14400000 ou 14400+000)
UF           = "SP"

# =============================================================================
# FUNÇÕES DO GERADOR (NÃO ALTERAR)
# =============================================================================
def num(valor, tamanho):
    val_str = str(valor) if valor is not None else "0"
    val_str = "".join(filter(str.isdigit, val_str))
    return val_str.zfill(tamanho)[:tamanho]

def txt(valor, tamanho):
    s = str(valor).upper() if valor is not None else ""
    return s[:tamanho].ljust(tamanho)

def txt_numerico_puro(valor, tamanho):
    if valor is None: return "0" * tamanho
    s = "".join(filter(str.isdigit, str(valor)))
    return s.zfill(tamanho)[:tamanho]

def data_fmt(data=None):
    if data is None: data = datetime.now()
    if isinstance(data, str): return data
    return data.strftime("%d%m%Y")

def hora_fmt(hora=None):
    if hora is None: hora = datetime.now()
    return hora.strftime("%H%M%S")

# =============================================================================
# CABEÇALHOS - CORRIGIDOS CONFORME ARQUIVO QUE FUNCIONA
# =============================================================================

def header_arquivo(seq=1):
    """
    Linha de referência que funciona:
    03300000         2020931540001090033418800490169580200009 0000130069341 COOPLUIZA - FRANCA -SP        SANTANDER (BRASIL) S.A.                 13001202616040000139506000000...
    """
    linha  = BANCO                          # 3   Cód. Banco
    linha += "0000"                         # 4   Lote (0000 = header arq)
    linha += "0"                            # 1   Tipo registro
    linha += " " * 9                        # 9   Brancos
    linha += "2"                            # 1   Tipo inscrição (2=CNPJ)
    linha += num(CNPJ, 14)                  # 14  CNPJ
    linha += txt(CONVENIO_COMPLETO, 20)     # 20  Convênio
    linha += num(AGENCIA, 5)               # 5   Agência
    linha += " "                            # 1   DV Agência (espaço)
    linha += num(CONTA, 12)                # 12  Conta
    linha += txt(DV_CONTA, 1)             # 1   DV Conta
    linha += " "                            # 1   DV Ag/Conta (espaço)
    linha += txt(EMPRESA, 30)              # 30  Nome empresa
    linha += txt(NOME_BANCO, 30)           # 30  Nome banco  ← CORRIGIDO
    linha += " " * 10                       # 10  Brancos
    linha += "1"                            # 1   Arquivo (1=remessa)
    linha += data_fmt()                     # 8   Data geração
    linha += hora_fmt()                     # 6   Hora geração
    linha += num(seq, 6)                    # 6   Nº sequencial
    linha += "060"                          # 3   Versão layout
    linha += "00000"                        # 5   Densidade
    linha += " " * 20                       # 20  Reservado banco
    linha += " " * 20                       # 20  Reservado empresa
    linha += " " * 29                       # 29  Brancos (total até 240)
    return linha

def header_lote():
    """
    Linha de referência que funciona:
    03300011C2001031 2020931540001090033418800490169580200009 0000130069341 COOPLUIZA - FRANCA -SP                                                RUA DO COMERCIO               000002  Andar       FRANCA              14400660SP
    """
    # Complemento de endereço com 15 chars exatos: " Andar       "
    complemento_fmt = (NUM_END[5:] + "  " + COMPLEMENTO).ljust(15)[:15]

    linha  = BANCO                          # 3   Cód. Banco
    linha += "0001"                         # 4   Lote
    linha += "1"                            # 1   Tipo registro
    linha += "C"                            # 1   Tipo operação (C=crédito)
    linha += "20"                           # 2   Tipo serviço (20=pagamento fornecedores)
    linha += "01"                           # 2   Forma lançamento (01=crédito em conta)
    linha += "031"                          # 3   Versão layout lote
    linha += " "                            # 1   Branco
    linha += "2"                            # 1   Tipo inscrição (2=CNPJ)
    linha += num(CNPJ, 14)                  # 14  CNPJ
    linha += txt(CONVENIO_COMPLETO, 20)     # 20  Convênio
    linha += num(AGENCIA, 5)               # 5   Agência
    linha += " "                            # 1   DV Agência (espaço)
    linha += num(CONTA, 12)                # 12  Conta
    linha += txt(DV_CONTA, 1)             # 1   DV Conta
    linha += " "                            # 1   DV Ag/Conta (espaço)
    linha += txt(EMPRESA, 30)              # 30  Nome empresa
    linha += " " * 40                       # 40  Finalidade lote (brancos)
    linha += txt(LOGRADOURO, 30)           # 30  Logradouro
    linha += NUM_END[:5].ljust(5)          # 6   Número  ← CORRIGIDO (000002→primeiros 5)
    linha += complemento_fmt               # 15  Complemento  ← CORRIGIDO
    linha += txt(CIDADE, 20)              # 20  Cidade
    linha += num(CEP, 8)                  # 8   CEP  ← CORRIGIDO (14400660)
    linha += UF                            # 2   UF
    linha += " " * 8                       # 8   Brancos
    linha += " " * 10                      # 10  Ocorrências
    return linha

# =============================================================================
# SEGMENTOS A e B, TRAILERS (sem alteração)
# =============================================================================

def segmento_a(seq, pag):
    valor_cents = int(float(pag["valor"]) * 100)
    linha  = BANCO + "0001" + "3" + num(seq, 5) + "A" + "0" + "00" + "009"
    linha += num(pag["banco"], 3)
    linha += num(pag["agencia"], 5)
    linha += "0"
    linha += num(pag["conta"], 12)
    linha += num(pag.get("dv_conta", "0"), 1)
    linha += " "
    linha += txt(pag["nome"], 30)
    linha += txt_numerico_puro(pag.get("documento", ""), 20)
    linha += data_fmt(pag["data_pagamento"])
    linha += "BRL" + num(0, 15) + num(valor_cents, 15)
    linha += (" " * 20) + "00000000" + num(0, 15)
    linha += (" " * 40) + "  " + (" " * 5) + "  " + "   " + "0" + (" " * 10)
    return linha

def segmento_b(seq, pag):
    cpf_limpo = "".join(filter(str.isdigit, str(pag["cpf_cnpj"])))
    tipo_insc = "1" if len(cpf_limpo) <= 11 else "2"
    valor_cents = int(float(pag["valor"]) * 100)

    linha  = BANCO + "0001" + "3" + num(seq, 5) + "B" + "05" + " " + tipo_insc
    linha += num(cpf_limpo, 14) + (" " * 30) + "00000" + (" " * 15) + (" " * 15)
    linha += (" " * 20) + "00000000" + "  " + data_fmt(pag["data_pagamento"])
    linha += num(valor_cents, 15) + num(0, 60)
    linha += "0000" + (" " * 11) + "0000" + "0" + (" " * 10)
    return linha

def trailer_lote(qtd, total):
    linha  = BANCO + "0001" + "5" + (" " * 9) + num(qtd, 6) + num(total, 18)
    linha += num(0, 18) + (" " * 171) + (" " * 10)
    return linha

def trailer_arquivo(lotes, regs):
    linha = BANCO + "9999" + "9" + (" " * 9) + num(lotes, 6) + num(regs, 6) + (" " * 211)
    return linha

# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def gerar_arquivo_cnab(pagamentos, nome_arquivo_saida, seq_arquivo=1):
    """
    seq_arquivo: número sequencial do arquivo enviado ao banco.
    Incrementa a cada remessa. O Santander rejeita nº repetido.
    Exemplo: seq_arquivo=1396 para o próximo após o 1395 do arquivo de referência.
    """
    linhas = [header_arquivo(seq=seq_arquivo), header_lote()]
    seq = 1
    total = 0

    for pag in pagamentos:
        linhas.append(segmento_a(seq, pag))
        seq += 1
        linhas.append(segmento_b(seq, pag))
        seq += 1
        total += int(float(pag["valor"]) * 100)

    linhas.append(trailer_lote(seq + 1, total))
    linhas.append(trailer_arquivo(1, len(linhas) + 1))

    with open(nome_arquivo_saida, "w", encoding="latin-1", newline="") as f:
        f.write("\r\n".join(linhas) + "\r\n")

    return nome_arquivo_saida