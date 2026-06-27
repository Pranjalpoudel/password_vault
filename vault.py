"""
Vault module for Secure Password Vault.
Handles CRUD operations for stored credentials.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from database import VaultDatabase


class CredentialVault:
    """Manages credential storage and retrieval."""

    def __init__(self, db: VaultDatabase, user_id: int):
        """Initialize vault for a specific user."""
        self.db = db
        self.user_id = user_id

    def add_entry(self, service_name: str, service_username: str, 
                  service_password: str, notes: str = "") -> tuple[bool, str]:
        """
        Add a new credential entry to the vault.
        
        Args:
            service_name: Name of the service (e.g., 'Gmail', 'Bank')
            service_username: Username for the service
            service_password: Password for the service
            notes: Optional notes about the entry
            
        Returns:
            (success, message/entry_id)
        """
        try:
            insert_query = """
                INSERT INTO vault_entries 
                (user_id, service_name, service_username, service_password, notes, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                RETURNING entry_id
            """
            
            result = self.db.execute_query_single(
                insert_query, 
                (self.user_id, service_name, service_username, service_password, notes)
            )
            
            if result:
                entry_id = result[0]
                # Log to audit
                self._log_action("ADD", entry_id)
                return True, f"Entry added successfully (ID: {entry_id})"
            return False, "Failed to add entry"
        except Exception as e:
            return False, f"Error adding entry: {str(e)}"

    def get_entry(self, entry_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single credential entry.
        
        Args:
            entry_id: ID of the entry to retrieve
            
        Returns:
            Dictionary with entry details or None if not found
        """
        query = """
            SELECT entry_id, service_name, service_username, service_password, notes, created_at, updated_at
            FROM vault_entries
            WHERE entry_id = %s AND user_id = %s
        """
        
        result = self.db.execute_query_single(query, (entry_id, self.user_id))
        
        if result:
            self._log_action("VIEW", entry_id)
            return {
                "entry_id": result[0],
                "service_name": result[1],
                "service_username": result[2],
                "service_password": result[3],
                "notes": result[4],
                "created_at": result[5],
                "updated_at": result[6]
            }
        return None

    def list_entries(self, search_term: str = "") -> List[Dict[str, Any]]:
        """
        List all credential entries for the user, optionally filtered by search.
        
        Args:
            search_term: Optional search filter for service names
            
        Returns:
            List of entry dictionaries
        """
        if search_term:
            query = """
                SELECT entry_id, service_name, service_username, created_at, updated_at
                FROM vault_entries
                WHERE user_id = %s AND service_name ILIKE %s
                ORDER BY service_name
            """
            results = self.db.execute_query(query, (self.user_id, f"%{search_term}%"), fetch=True)
        else:
            query = """
                SELECT entry_id, service_name, service_username, created_at, updated_at
                FROM vault_entries
                WHERE user_id = %s
                ORDER BY service_name
            """
            results = self.db.execute_query(query, (self.user_id,), fetch=True)
        
        entries = []
        if results:
            for row in results:
                entries.append({
                    "entry_id": row[0],
                    "service_name": row[1],
                    "service_username": row[2],
                    "created_at": row[3],
                    "updated_at": row[4]
                })
        
        return entries

    def update_entry(self, entry_id: int, service_name: Optional[str] = None,
                     service_username: Optional[str] = None,
                     service_password: Optional[str] = None,
                     notes: Optional[str] = None) -> tuple[bool, str]:
        """
        Update an existing credential entry.
        
        Args:
            entry_id: ID of entry to update
            service_name: New service name (optional)
            service_username: New username (optional)
            service_password: New password (optional)
            notes: New notes (optional)
            
        Returns:
            (success, message)
        """
        # Build dynamic update query
        updates = []
        params = []
        
        if service_name is not None:
            updates.append("service_name = %s")
            params.append(service_name)
        if service_username is not None:
            updates.append("service_username = %s")
            params.append(service_username)
        if service_password is not None:
            updates.append("service_password = %s")
            params.append(service_password)
        if notes is not None:
            updates.append("notes = %s")
            params.append(notes)
        
        if not updates:
            return False, "No fields to update"
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(entry_id)
        params.append(self.user_id)
        
        try:
            query = f"""
                UPDATE vault_entries
                SET {', '.join(updates)}
                WHERE entry_id = %s AND user_id = %s
            """
            
            self.db.execute_query(query, tuple(params))
            self._log_action("UPDATE", entry_id)
            return True, "Entry updated successfully"
        except Exception as e:
            return False, f"Error updating entry: {str(e)}"

    def delete_entry(self, entry_id: int) -> tuple[bool, str]:
        """
        Delete a credential entry.
        
        Args:
            entry_id: ID of entry to delete
            
        Returns:
            (success, message)
        """
        try:
            query = "DELETE FROM vault_entries WHERE entry_id = %s AND user_id = %s"
            self.db.execute_query(query, (entry_id, self.user_id))
            self._log_action("DELETE", entry_id)
            return True, "Entry deleted successfully"
        except Exception as e:
            return False, f"Error deleting entry: {str(e)}"

    def _log_action(self, action: str, entry_id: Optional[int] = None) -> None:
        """Log an action to the audit log."""
        log_query = """
            INSERT INTO audit_log (user_id, action, entry_id, action_time)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
        """
        self.db.execute_query(log_query, (self.user_id, action, entry_id))
