import random
import time
import datetime

modulos = ["Solar", "Eolico", "Comunicacao", "Propulsao"]
limites_temp = (-20, 80)
limite_energia = 10
limite_sinal = 50
alertas_log = []

def gerar_dados(modulo):
    return {
        "modulo": modulo,
        "temp": round(random.uniform(-30, 95), 1),
        "energia": round(random.uniform(5, 100), 1),
        "sinal": round(random.uniform(30, 100), 1),
        "status": random.choice(["OPERACIONAL", "STANDBY", "FALHA", "SOBRECARGA"]),
        "hora": datetime.datetime.now().strftime("%H:%M:%S")
    }

def checar_alertas(d):
    alertas = []
    if d["temp"] > limites_temp[1]:
        alertas.append(f"TEMP ALTA: {d['temp']}C")
    elif d["temp"] < limites_temp[0]:
        alertas.append(f"TEMP BAIXA: {d['temp']}C")
    if d["energia"] < limite_energia:
        alertas.append(f"ENERGIA CRITICA: {d['energia']}%")
    if d["sinal"] < limite_sinal:
        alertas.append(f"SINAL FRACO: {d['sinal']}%")
    if d["status"] in ["FALHA", "SOBRECARGA"]:
        alertas.append(f"STATUS: {d['status']}")
    return alertas

def decidir(d, alertas):
    acoes = []
    for a in alertas:
        if "TEMP ALTA" in a:
            acoes.append("-> ativando resfriamento")
        elif "TEMP BAIXA" in a:
            acoes.append("-> ativando aquecedores")
        elif "ENERGIA" in a:
            acoes.append("-> modo economia ativado")
        elif "SINAL" in a:
            acoes.append("-> realinhando antena")
        elif "FALHA" in d["status"]:
            acoes.append("-> reiniciando modulo")
        elif "SOBRECARGA" in d["status"]:
            acoes.append("-> desligando subsistemas")
    if not acoes:
        acoes.append("-> sistema estavel")
    return acoes

def mostrar(d, alertas, acoes):
    print(f"\n[{d['hora']}] Modulo {d['modulo']}")
    print(f"  temp: {d['temp']}C | energia: {d['energia']}% | sinal: {d['sinal']}% | status: {d['status']}")
    if alertas:
        for a in alertas:
            print(f"  ! {a}")
        for ac in acoes:
            print(f"  {ac}")
        alertas_log.extend(alertas)
    else:
        print("  ok")

def main():
    print("=== monitoramento missao espacial ===")
    ciclos = 3
    for c in range(1, ciclos + 1):
        print(f"\n-- ciclo {c}/{ciclos} --")
        for m in modulos:
            d = gerar_dados(m)
            alertas = checar_alertas(d)
            acoes = decidir(d, alertas)
            mostrar(d, alertas, acoes)
            time.sleep(0.2)
        if c < ciclos:
            time.sleep(1)

    print(f"\n=== resumo: {len(alertas_log)} alertas registrados ===")
    for a in alertas_log[:5]:
        print(f"  - {a}")
    if len(alertas_log) > 5:
        print(f"  ... e mais {len(alertas_log) - 5}")

if __name__ == "__main__":
    main()