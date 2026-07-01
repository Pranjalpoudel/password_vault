"""
API reference and integration module for Secure Password Vault.
Provides REST-style interfaces for external integrations.
"""

from typing import Dict, Any, List, Optional
from database import VaultDatabase
from vault import CredentialVault
from auth import AuthManager


class VaultAPI:
    """High-level API for password vault operations."""

    def __init__(self, db: VaultDatabase):
        """Initialize vault API."""
        self.db = db
        self.auth = AuthManager(db)
        self.current_user_id = None

    def authenticate(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user and return session details."""
        success, user_id, message = self.auth.login_user(username, password)
        
        if success:
            self.current_user_id = user_id
            return {
                "success": True,
                "user_id": user_id,
                "message": message
            }
        
        return {
            "success": False,
            "user_id": None,
            "message": message
        }

    def register(self, username: str, password: str) -> Dict[str, Any]:
        """Register new user."""
        success, message = self.auth.register_user(username, password)
        
        return {
            "success": success,
            "message": message
        }

    def get_credentials(self, search_term: str = "") -> Dict[str, Any]:
        """Get credentials from vault."""
        if not self.current_user_id:
            return {"success": False, "message": "Not authenticated"}

        try:
            vault = CredentialVault(self.db, self.current_user_id)
            entries = vault.list_entries(search_term)
            
            return {
                "success": True,
                "count": len(entries),
                "entries": entries
            }
        except Exception as e:
            return {"success": False, "message": str(e)}

    def add_credential(self, service_name: str, username: str, 
                      password: str, notes: str = "") -> Dict[str, Any]:
        """Add new credential."""
        if not self.current_user_id:
            return {"success": False, "message": "Not authenticated"}

        try:
            vault = CredentialVault(self.db, self.current_user_id)
            success, message = vault.add_entry(service_name, username, password, notes)
            
            return {"success": success, "message": message}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def delete_credential(self, entry_id: int) -> Dict[str, Any]:
        """Delete a credential."""
        if not self.current_user_id:
            return {"success": False, "message": "Not authenticated"}

        try:
            vault = CredentialVault(self.db, self.current_user_id)
            success, message = vault.delete_entry(entry_id)
            
            return {"success": success, "message": message}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def logout(self) -> Dict[str, Any]:
        """Logout current user."""
        self.current_user_id = None
        return {"success": True, "message": "Logged out successfully"}
