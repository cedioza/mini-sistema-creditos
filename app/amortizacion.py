import pandas as pd

def generar_plan_amortizacion(monto, plazo, tasa_interes):
    tasa_mensual = tasa_interes / 100 / 12
    pago_mensual = monto * tasa_mensual / (1 - (1 + tasa_mensual) ** -plazo)
    plan = []
    saldo_restante = monto

    for mes in range(1, plazo + 1):
        interes = saldo_restante * tasa_mensual
        capital = pago_mensual - interes
        saldo_restante -= capital
        plan.append({"Mes": mes, "Pago": round(pago_mensual, 2), "Capital": round(capital, 2), "Interés": round(interes, 2), "Saldo Restante": round(saldo_restante, 2)})

    return pd.DataFrame(plan)
