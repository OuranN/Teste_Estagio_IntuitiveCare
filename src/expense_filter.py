def is_expense(row):
    code = str(row["codigo"])
    desc = str(row["descricao"]).upper()

    if code.startswith("41"):
        return True

    if code.startswith("4") and ("EVENTOS" in desc or "SINISTROS" in desc):
        return True

    return False
