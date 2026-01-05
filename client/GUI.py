import tkinter as tk
from tkinter import messagebox

class MonopolyGUI:
    def __init__(self, root, client):
        self.root = root
        self.client = client
        self.root.title("Monopoly - Client")

        # ====== Frames ======
        self.info_frame = tk.Frame(root)
        self.info_frame.pack(pady=10)

        self.players_frame = tk.Frame(root)
        self.players_frame.pack(pady=10)

        self.control_frame = tk.Frame(root)
        self.control_frame.pack(pady=10)

        self.log_frame = tk.Frame(root)
        self.log_frame.pack(pady=10)

        # ====== Info ======
        self.turn_label = tk.Label(self.info_frame, text="Turn: -")
        self.turn_label.pack()


        self.players_labels = {}


        tk.Button(self.control_frame, text="Roll Dice", command=self.roll_dice).grid(row=0, column=0, padx=5)
        tk.Button(self.control_frame, text="Buy Property", command=self.buy_property).grid(row=0, column=1, padx=5)
        tk.Button(self.control_frame, text="Undo", command=self.undo).grid(row=0, column=2, padx=5)
        tk.Button(self.control_frame, text="Redo", command=self.redo).grid(row=0, column=3, padx=5)
        tk.Button(self.control_frame, text="End Turn", command=self.end_turn).grid(row=0, column=4, padx=5)

        # ====== Event Log ======
        tk.Label(self.log_frame, text="Event Log").pack()
        self.log_text = tk.Text(self.log_frame, height=10, width=70)
        self.log_text.pack()
        self.connect()


    def connect(self):
        response = self.client.send({"type": "HELLO"})
        if response.get("type") == "ERROR":
            messagebox.showerror("Error", response["message"])
        else:
            self.player_id = response.get("player_id")
            self.log("Connected as Player " + str(self.player_id))
            self.update_state(response)

    def roll_dice(self):
        self.update_state(self.client.send({"type": "ROLL_DICE"}))

    def buy_property(self):
        self.update_state(self.client.send({"type": "BUY_PROPERTY"}))

    def undo(self):
        self.update_state(self.client.send({"type": "UNDO"}))

    def redo(self):
        self.update_state(self.client.send({"type": "REDO"}))

    def end_turn(self):
        self.update_state(self.client.send({"type": "END_TURN"}))


    def update_state(self, response):
        if response.get("type") == "ERROR":
            self.log("ERROR: " + response["message"])
            return

        if response.get("type") == "STATE_UPDATE":
            state = response["state"]

            self.turn_label.config(
                text=f"Current Player: {state['current_player']} | Round: {state['round']}"
            )

            self.update_players(state["players"])
            self.log("State updated")

    def update_players(self, players):
        for widget in self.players_frame.winfo_children():
            widget.destroy()

        for pid, pdata in players.items():
            text = (
                f"Player {pid} | "
                f"Money: {pdata['balance']} | "
                f"Tile: {pdata['tile']} | "
                f"State: {pdata['state']}"
            )
            tk.Label(self.players_frame, text=text).pack(anchor="w")

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
