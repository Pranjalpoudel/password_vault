"""
Main application for Secure Password Vault.
Desktop GUI built with Tkinter.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkinter import scrolledtext
import os
from dotenv import load_dotenv
from database import VaultDatabase
from auth import AuthManager
from vault import CredentialVault
from generator import PasswordGenerator, PasswordStrengthChecker
from config import Config

# Load environment variables from .env file
load_dotenv()


class PasswordVaultApp:
    """Main Tkinter application for the password vault."""

    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title("Secure Password Vault")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Initialize database with Config
        try:
            self.db = VaultDatabase(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                port=Config.DB_PORT
            )
            self.db.initialize_schema()
        except Exception as e:
            messagebox.showerror(
                "Database Error", 
                f"Failed to connect to database:\n\n{str(e)}\n\n"
                "Please ensure:\n"
                "1. PostgreSQL is installed and running\n"
                "2. Create a .env file with your credentials (see .env.example)\n"
                "3. Run setup_database.py to initialize"
            )
            root.destroy()
            return

        self.auth = AuthManager(self.db)
        self.vault = None
        self.user_id = None
        self.current_user = None

        # Start with login screen
        self.show_login_screen()

    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        """Display login/registration screen."""
        self.clear_window()
        
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)

        ttk.Label(frame, text="Secure Password Vault", font=("Arial", 20, "bold")).pack(pady=10)
        ttk.Label(frame, text="Password Management", font=("Arial", 12)).pack(pady=5)

        # Username
        ttk.Label(frame, text="Username:").pack(pady=5)
        username_var = tk.StringVar()
        ttk.Entry(frame, textvariable=username_var, width=30).pack()

        # Password
        ttk.Label(frame, text="Master Password:").pack(pady=5)
        password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=password_var, show="*", width=30).pack()

        def login():
            username = username_var.get()
            password = password_var.get()
            
            if not username or not password:
                messagebox.showerror("Error", "Please enter username and password.")
                return

            success, user_id, message = self.auth.login_user(username, password)
            if success:
                self.user_id = user_id
                self.current_user = username
                self.vault = CredentialVault(self.db, user_id)
                self.show_vault_screen()
            else:
                messagebox.showerror("Login Failed", message)

        def register():
            username = username_var.get()
            password = password_var.get()
            
            if not username or not password:
                messagebox.showerror("Error", "Please enter username and password.")
                return

            success, message = self.auth.register_user(username, password)
            if success:
                messagebox.showinfo("Success", message)
                username_var.delete(0, tk.END)
                password_var.delete(0, tk.END)
            else:
                messagebox.showerror("Registration Failed", message)

        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="Login", command=login, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Register", command=register, width=15).pack(side=tk.LEFT, padx=5)

    def show_vault_screen(self):
        """Display the main vault management screen."""
        self.clear_window()

        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(header_frame, text=f"Vault - {self.current_user}", font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        ttk.Button(header_frame, text="Logout", command=self.logout).pack(side=tk.RIGHT)

        # Toolbar
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(toolbar, text="Add Entry", command=self.show_add_entry_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Generate Password", command=self.show_generator_dialog).pack(side=tk.LEFT, padx=5)

        # Search
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame)
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        def perform_search():
            term = search_var.get()
            refresh_list(term)

        search_var.trace("w", lambda *args: perform_search())
        search_entry.config(textvariable=search_var)

        # Entries list
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tree_scroll = ttk.Scrollbar(list_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        tree = ttk.Treeview(
            list_frame,
            columns=("Service", "Username", "Updated"),
            height=15,
            yscrollcommand=tree_scroll.set
        )
        tree_scroll.config(command=tree.yview)
        tree.heading("#0", text="ID")
        tree.heading("Service", text="Service")
        tree.heading("Username", text="Username")
        tree.heading("Updated", text="Last Updated")
        tree.column("#0", width=30)
        tree.column("Service", width=200)
        tree.column("Username", width=200)
        tree.column("Updated", width=150)
        tree.pack(fill=tk.BOTH, expand=True)

        def refresh_list(search_term=""):
            for item in tree.get_children():
                tree.delete(item)
            
            entries = self.vault.list_entries(search_term)
            for entry in entries:
                tree.insert(
                    "",
                    "end",
                    text=str(entry["entry_id"]),
                    values=(
                        entry["service_name"],
                        entry["service_username"],
                        str(entry["updated_at"])[:10]
                    ),
                    tags=("entry",)
                )

        def on_entry_select(event):
            selected = tree.selection()
            if not selected:
                return
            entry_id = int(tree.item(selected[0])["text"])
            self.show_entry_details(entry_id)

        tree.bind("<<TreeviewSelect>>", on_entry_select)
        refresh_list()

    def show_add_entry_dialog(self):
        """Show dialog to add a new vault entry."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Entry")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Service Name:").pack(pady=5)
        service_var = tk.StringVar()
        ttk.Entry(frame, textvariable=service_var, width=40).pack(pady=5)

        ttk.Label(frame, text="Username:").pack(pady=5)
        username_var = tk.StringVar()
        ttk.Entry(frame, textvariable=username_var, width=40).pack(pady=5)

        ttk.Label(frame, text="Password:").pack(pady=5)
        password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=password_var, show="*", width=40).pack(pady=5)

        ttk.Label(frame, text="Notes:").pack(pady=5)
        notes_var = tk.StringVar()
        notes_text = scrolledtext.ScrolledText(frame, width=40, height=5)
        notes_text.pack(pady=5)

        def save_entry():
            service = service_var.get()
            username = username_var.get()
            password = password_var.get()
            notes = notes_text.get("1.0", tk.END).strip()

            if not service or not username or not password:
                messagebox.showerror("Error", "Please fill in all required fields.")
                return

            success, message = self.vault.add_entry(service, username, password, notes)
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.show_vault_screen()
            else:
                messagebox.showerror("Error", message)

        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="Save", command=save_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def show_entry_details(self, entry_id: int):
        """Show details of a specific entry."""
        entry = self.vault.get_entry(entry_id)
        if not entry:
            messagebox.showerror("Error", "Entry not found.")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Entry: {entry['service_name']}")
        dialog.geometry("500x450")
        dialog.transient(self.root)
        dialog.grab_set()

        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Service Name:").pack(pady=5)
        service_var = tk.StringVar(value=entry["service_name"])
        ttk.Entry(frame, textvariable=service_var, width=40).pack(pady=5)

        ttk.Label(frame, text="Username:").pack(pady=5)
        username_var = tk.StringVar(value=entry["service_username"])
        ttk.Entry(frame, textvariable=username_var, width=40).pack(pady=5)

        ttk.Label(frame, text="Password:").pack(pady=5)
        password_var = tk.StringVar(value=entry["service_password"])
        password_entry = ttk.Entry(frame, textvariable=password_var, show="*", width=40)
        password_entry.pack(pady=5)

        def toggle_password():
            if password_entry.cget("show") == "*":
                password_entry.config(show="")
            else:
                password_entry.config(show="*")

        ttk.Button(frame, text="Show/Hide", command=toggle_password).pack(pady=5)

        ttk.Label(frame, text="Notes:").pack(pady=5)
        notes_text = scrolledtext.ScrolledText(frame, width=40, height=5)
        notes_text.insert("1.0", entry["notes"])
        notes_text.pack(pady=5)

        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)

        def update_entry():
            success, message = self.vault.update_entry(
                entry_id,
                service_name=service_var.get(),
                service_username=username_var.get(),
                service_password=password_var.get(),
                notes=notes_text.get("1.0", tk.END).strip()
            )
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.show_vault_screen()
            else:
                messagebox.showerror("Error", message)

        def delete_entry():
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this entry?"):
                success, message = self.vault.delete_entry(entry_id)
                if success:
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                    self.show_vault_screen()
                else:
                    messagebox.showerror("Error", message)

        ttk.Button(button_frame, text="Update", command=update_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete", command=delete_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def show_generator_dialog(self):
        """Show password generator and strength checker dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Password Generator")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()

        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        generator = PasswordGenerator()
        strength_checker = PasswordStrengthChecker()

        ttk.Label(frame, text="Password Length:", font=("Arial", 10)).pack(pady=5)
        length_var = tk.IntVar(value=16)
        ttk.Scale(frame, from_=8, to=64, variable=length_var, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        length_label = ttk.Label(frame, text="16")
        length_label.pack()

        def update_length(*args):
            length_label.config(text=str(length_var.get()))

        length_var.trace("w", update_length)

        # Checkboxes
        options_frame = ttk.LabelFrame(frame, text="Character Types", padding="10")
        options_frame.pack(fill=tk.X, pady=10)

        uppercase_var = tk.BooleanVar(value=True)
        lowercase_var = tk.BooleanVar(value=True)
        digits_var = tk.BooleanVar(value=True)
        symbols_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(options_frame, text="Uppercase", variable=uppercase_var).pack()
        ttk.Checkbutton(options_frame, text="Lowercase", variable=lowercase_var).pack()
        ttk.Checkbutton(options_frame, text="Digits", variable=digits_var).pack()
        ttk.Checkbutton(options_frame, text="Symbols", variable=symbols_var).pack()

        ttk.Label(frame, text="Generated Password:", font=("Arial", 10)).pack(pady=5)
        password_var = tk.StringVar()
        password_entry = ttk.Entry(frame, textvariable=password_var, width=50)
        password_entry.pack(pady=5)

        # Strength indicator
        strength_frame = ttk.LabelFrame(frame, text="Password Strength", padding="10")
        strength_frame.pack(fill=tk.X, pady=10)

        strength_label = ttk.Label(strength_frame, text="Very Weak", font=("Arial", 12, "bold"))
        strength_label.pack()

        details_text = scrolledtext.ScrolledText(strength_frame, width=50, height=4)
        details_text.pack(pady=5)

        def generate_password():
            password = generator.generate(
                length=length_var.get(),
                use_uppercase=uppercase_var.get(),
                use_lowercase=lowercase_var.get(),
                use_digits=digits_var.get(),
                use_symbols=symbols_var.get()
            )
            password_var.set(password)
            
            # Check strength
            strength_level, label, color, details = strength_checker.check(password)
            strength_label.config(text=label)
            
            details_text.config(state=tk.NORMAL)
            details_text.delete("1.0", tk.END)
            details_text.insert("1.0", f"""Length: {details['length']}
Entropy: {details['entropy']} bits
Has Uppercase: {details['has_uppercase']}
Has Lowercase: {details['has_lowercase']}
Has Digits: {details['has_digits']}
Has Symbols: {details['has_symbols']}""")
            details_text.config(state=tk.DISABLED)

        def copy_password():
            password = password_var.get()
            if password:
                self.root.clipboard_clear()
                self.root.clipboard_append(password)
                messagebox.showinfo("Copied", "Password copied to clipboard.")

        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Generate", command=generate_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Copy", command=copy_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def logout(self):
        """Logout current user and return to login screen."""
        self.user_id = None
        self.current_user = None
        self.vault = None
        self.show_login_screen()


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordVaultApp(root)
    root.mainloop()
