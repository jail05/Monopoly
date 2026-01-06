from Monopoly.server.server import Server
from Monopoly.server.client import Client

def main():
    # ساخت سرور
    server = Server()

    # ساخت کلاینت‌ها
    c1 = Client(server, "A")
    c2 = Client(server, "B")
    c3 = Client(server, "C")
    c4 = Client(server, "D")

    # اتصال کلاینت‌ها (HELLO)
    print(c1.connect())
    print(c2.connect())
    print(c3.connect())
    print(c4.connect())

    print("\n--- GAME START ---\n")

    # ===== Turn Player A =====
    print("A rolls dice")
    print(c1.roll_dice())

    print("A ends turn")
    print(c1.end_turn())

    # ===== Turn Player B =====
    print("B rolls dice")
    print(c2.roll_dice())

    # اگر property آزاد بود، خرید
    state = c2.send({"type": "BUY_PROPERTY", "property_id": 1})
    print(state)

    print("B ends turn")
    print(c2.end_turn())

    # ===== Turn Player C =====
    print("C rolls dice")
    print(c3.roll_dice())
    print("C ends turn")
    print(c3.end_turn())

    # ===== Turn Player D =====
    print("D rolls dice")
    print(c4.roll_dice())
    print("D ends turn")
    print(c4.end_turn())

    print("\n--- GAME STATE ---")
    print(server.state_update())

if __name__ == "__main__":
    main()
