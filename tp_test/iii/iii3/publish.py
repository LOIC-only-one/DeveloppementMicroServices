import asyncio
import nats

async def test_services():
    nc = await nats.connect("nats://192.168.19.130:4222")
    
    test_cases = [
        {"numero_compte": "11111111", "date": "2025-06-02", "montant": "5000"},
        {"numero_compte": "22222222", "date": "2024-12-31", "montant": "10000"},
        {"numero_compte": "33333333", "date": "2023-01-01", "montant": "0"},
    ]

    for case in test_cases:
        numero_compte = case["numero_compte"]
        date_test = case["date"]
        montant_test = case["montant"]

        print(f"\nTest pour le compte {numero_compte}")

        print("test du service compte")
        try:
            response = await nc.request(f"argent.{numero_compte}.compte", b"", timeout=2)
            print("reponse compte", response.data.decode())
        except asyncio.TimeoutError:
            print("aucune reponse du service compte")

        print("test du service date")
        try:
            response = await nc.request(f"argent.{numero_compte}.date", date_test.encode(), timeout=2)
            print("reponse date", response.data.decode())
        except asyncio.TimeoutError:
            print("aucune reponse du service date")

        print("test du service montant")
        try:
            response = await nc.request(f"argent.{numero_compte}.montant", montant_test.encode(), timeout=2)
            print("reponse montant", response.data.decode())
        except asyncio.TimeoutError:
            print("aucune reponse du service montant")

    await nc.close()

if __name__ == "__main__":
    asyncio.run(test_services())
