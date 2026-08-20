import os
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox

class InstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SignalShop Installer")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.admin_email = tk.StringVar(value="admin@example.com")
        self.admin_password = tk.StringVar(value="admin1234")
        self.signal_phone = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="SignalShop", font=("Arial", 24, "bold")).pack(pady=20)

        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        ttk.Label(frame, text="Email administrateur:").grid(row=0, column=0, sticky="e")
        ttk.Entry(frame, textvariable=self.admin_email, width=30).grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Mot de passe administrateur:").grid(row=1, column=0, sticky="e")
        ttk.Entry(frame, textvariable=self.admin_password, width=30, show="*").grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Numéro Signal (optionnel):").grid(row=2, column=0, sticky="e")
        ttk.Entry(frame, textvariable=self.signal_phone, width=30).grid(row=2, column=1, pady=5)

        self.install_btn = ttk.Button(self.root, text="Installer", command=self.start_install)
        self.install_btn.pack(pady=20)

        self.progress = ttk.Progressbar(self.root, length=400, mode='indeterminate')
        self.progress.pack(pady=10)

        self.log_text = tk.Text(self.root, height=10, width=70, state='disabled')
        self.log_text.pack(pady=10)

    def log(self, message):
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')

    def start_install(self):
        if self.admin_password.get() == "admin1234":
            messagebox.showwarning("Sécurité", "Veuillez choisir un mot de passe plus fort que 'admin1234'.")
            return

        self.install_btn.config(state='disabled')
        self.progress.start()
        threading.Thread(target=self.install).start()

    def install(self):
        try:
            self.log("Vérification de Docker...")
            if subprocess.call(["docker", "--version"], shell=True) != 0:
                self.show_error("Docker n'est pas installé.")
                return

            self.log("Vérification de Git...")
            if subprocess.call(["git", "--version"], shell=True) != 0:
                self.show_error("Git n'est pas installé.")
                return

            self.log("Création du fichier .env...")
            self.create_env_file()

            self.log("Démarrage des services Docker...")
            subprocess.call("docker compose --env-file .env -f docker/docker-compose.yml up -d --build", shell=True)

            self.log("Initialisation de la base...")
            subprocess.call("docker exec -it signalshop_backend python -m scripts.init_db", shell=True)
            subprocess.call("docker exec -it signalshop_backend python -m scripts.create_initial_user", shell=True)

            self.log("Installation terminée !")
            self.log("Dashboard : http://localhost:3000")
            messagebox.showinfo("Terminé", "SignalShop a été installé avec succès !")
        except Exception as e:
            self.show_error(str(e))
        finally:
            self.progress.stop()
            self.install_btn.config(state='normal')

    def create_env_file(self):
        content = f"""POSTGRES_USER=signaluser
POSTGRES_PASSWORD=change_this_strong_password
POSTGRES_DB=signal_shop
DATABASE_URL=postgresql://signaluser:change_this_strong_password@db:5432/signal_shop
REDIS_URL=redis://redis:6379/0
SECRET_KEY=change_this_secret_key
BACKEND_PORT=8000
FRONTEND_PORT=3000
SIGNAL_SERVICE_PHONE={self.signal_phone.get()}
ADMIN_EMAIL={self.admin_email.get()}
ADMIN_PASSWORD={self.admin_password.get()}
"""
        with open(".env", "w") as f:
            f.write(content)

    def show_error(self, message):
        self.log(f"ERREUR: {message}")
        messagebox.showerror("Erreur", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = InstallerApp(root)
    root.mainloop()