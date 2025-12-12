 
import sqlite3
import os
from datetime import datetime
from typing import Optional, Dict, List
import json

class Database:
    def __init__(self, db_path: str = "storage/data/beauty.db"):
        if not os.path.isabs(db_path):
            project_root = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
            db_path = os.path.normpath(os.path.join(project_root, db_path))
        
        self.db_path = db_path
        self._ensure_db_dir()

        if not os.path.exists(self.db_path) or os.path.getsize(self.db_path) == 0:
            try:
                self.init_db()
            except Exception as e:
                print(f"Ошибка инициализации БД: {e}")
                raise
        
        self._migrate()

    def _ensure_db_dir(self):
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=5)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        try:
            conn = self._get_connection()
            sql = """
            PRAGMA foreign_keys = ON;

            CREATE TABLE IF NOT EXISTS masters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                name TEXT,
                username TEXT,
                bio TEXT,
                location TEXT,
                profile_image_path TEXT,
                booking_link TEXT,
                telegram TEXT,
                youtube TEXT,
                instagram TEXT,
                tiktok TEXT,
                pinterest TEXT,
                is_profile_complete INTEGER DEFAULT 0,
                profile_completion_percent INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                master_id INTEGER,
                name TEXT NOT NULL,
                description TEXT,
                duration_minutes INTEGER,
                price REAL,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                master_id INTEGER,
                client_id TEXT,
                client_name TEXT,
                service_id INTEGER,
                booking_date DATE,
                booking_time TIME,
                status TEXT DEFAULT 'pending',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                name TEXT,
                phone TEXT,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS schedule_slots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                master_id INTEGER,
                slot_date DATE,
                start_time TIME,
                end_time TIME,
                is_booked INTEGER DEFAULT 0,
                service_ids TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            conn.executescript(sql)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"✗ ОШИБКА инициализации БД: {e}")
            raise

    def _migrate(self):
        columns = [
            ('telegram', 'TEXT'), ('youtube', 'TEXT'), ('instagram', 'TEXT'),
            ('tiktok', 'TEXT'), ('pinterest', 'TEXT'),
        ]
        conn = self._get_connection()
        cursor = conn.cursor()
        for col_name, col_type in columns:
            try:
                cursor.execute(f"ALTER TABLE masters ADD COLUMN {col_name} {col_type}")
            except sqlite3.OperationalError:
                pass
        
        try:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS schedule_slots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                master_id INTEGER,
                slot_date DATE,
                start_time TIME,
                end_time TIME,
                is_booked INTEGER DEFAULT 0,
                service_ids TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
        except Exception as e:
            pass

        conn.commit()
        conn.close()

 
    def get_or_create_master(self, user_id: str) -> Dict:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM masters WHERE user_id = ?", (user_id,))
        master = cursor.fetchone()

        if master:
            conn.close()
            return dict(master)

        cursor.execute("INSERT INTO masters (user_id, booking_link) VALUES (?, ?)", (user_id, f"be.beauty/{user_id}"))
        conn.commit()
        master_id = cursor.lastrowid
        conn.close()
        return self.get_master_by_id(master_id)

    def get_master_by_id(self, master_id: int) -> Optional[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM masters WHERE id = ?", (master_id,))
        master = cursor.fetchone()
        conn.close()
        return dict(master) if master else None

    def get_master_by_user_id(self, user_id: str) -> Optional[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM masters WHERE user_id = ?", (user_id,))
        master = cursor.fetchone()
        conn.close()
        return dict(master) if master else None

    def get_all_masters(self) -> List[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM masters ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def search_masters(self, city: str = "", service: str = "") -> List[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        query = "SELECT DISTINCT m.* FROM masters m"
        params = []
        conditions = []
        if service:
            query += " JOIN services s ON m.id = s.master_id"
            conditions.append("s.name LIKE ?")
            params.append(f"%{service}%")
        if city:
            conditions.append("m.location LIKE ?")
            params.append(f"%{city}%")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY m.created_at DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def update_master_profile(self, master_id: int, **kwargs) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        allowed_fields = ['name', 'username', 'bio', 'location', 'profile_image_path',
                          'telegram', 'youtube', 'instagram', 'tiktok', 'pinterest']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not updates:
            conn.close()
            return False
        updates['updated_at'] = datetime.now().isoformat()
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [master_id]
        cursor.execute(f"UPDATE masters SET {set_clause} WHERE id = ?", values)
        conn.commit()
        conn.close()
        self._update_profile_completion(master_id)
        return True

    def _update_profile_completion(self, master_id: int):
        master = self.get_master_by_id(master_id)
        if not master: return
        filled_fields = sum([bool(master.get('name')), bool(master.get('username')), bool(master.get('bio')), bool(master.get('location'))])
        total_fields = 4
        completion_percent = int((filled_fields / total_fields) * 100)
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE masters SET profile_completion_percent = ?, is_profile_complete = ? WHERE id = ?", 
                       (completion_percent, 1 if completion_percent == 100 else 0, master_id))
        conn.commit()
        conn.close()

 
    def add_service(self, master_id: int, name: str, description: str = "", duration_minutes: int = 30, price: float = 0) -> int:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO services (master_id, name, description, duration_minutes, price) VALUES (?, ?, ?, ?, ?)", 
                       (master_id, name, description, duration_minutes, price))
        conn.commit()
        service_id = cursor.lastrowid
        conn.close()
        return service_id

    def update_service(self, service_id: int, name: str, description: str, duration_minutes: int, price: float) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE services 
                SET name = ?, description = ?, duration_minutes = ?, price = ?
                WHERE id = ?
            """, (name, description, duration_minutes, price, service_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Update service error: {e}")
            return False
        finally:
            conn.close()

    def get_master_services(self, master_id: int) -> List[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM services WHERE master_id = ? AND is_active = 1 ORDER BY created_at", (master_id,))
        services = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return services

    def delete_service(self, service_id: int) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE services SET is_active = 0 WHERE id = ?", (service_id,))
        conn.commit()
        conn.close()
        return True
        
    def get_services_by_ids(self, service_ids: list) -> List[Dict]:
        if not service_ids: return []
        conn = self._get_connection()
        cursor = conn.cursor()
        placeholders = ','.join('?' for _ in service_ids)
        query = f"SELECT * FROM services WHERE id IN ({placeholders})"
        cursor.execute(query, service_ids)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

 
    def add_booking(self, master_id: int, service_id: int, client_name: str, booking_date: str, booking_time: str, notes: str = "") -> int:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bookings (master_id, service_id, client_name, booking_date, booking_time, notes, status) VALUES (?, ?, ?, ?, ?, ?, 'confirmed')", 
                       (master_id, service_id, client_name, booking_date, booking_time, notes))
        conn.commit()
        booking_id = cursor.lastrowid
        conn.close()
        return booking_id

    def get_master_bookings(self, master_id: int) -> List[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.*, s.name as service_name, s.price
            FROM bookings b
            LEFT JOIN services s ON b.service_id = s.id
            WHERE b.master_id = ?
            ORDER BY b.booking_date DESC, b.booking_time DESC
        """, (master_id,))
        bookings = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return bookings

 
    def add_schedule_slot(self, master_id: int, slot_date: str, start_time: str, end_time: str, service_ids: list) -> int:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO schedule_slots (master_id, slot_date, start_time, end_time, service_ids, is_booked) VALUES (?, ?, ?, ?, ?, 0)", 
                       (master_id, slot_date, start_time, end_time, json.dumps(service_ids)))
        conn.commit()
        slot_id = cursor.lastrowid
        conn.close()
        return slot_id

    def get_schedule_slots(self, master_id: int, slot_date: str) -> List[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM schedule_slots WHERE master_id = ? AND slot_date = ? ORDER BY start_time", (master_id, slot_date))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_available_slots(self, master_id: int) -> List[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
            SELECT * FROM schedule_slots 
            WHERE master_id = ? AND is_booked = 0 AND slot_date >= ?
            ORDER BY slot_date, start_time
        """, (master_id, today))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def book_slot_transaction(self, slot_id: int, client_name: str, notes: str) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM schedule_slots WHERE id = ?", (slot_id,))
            slot = cursor.fetchone()
            if not slot or slot['is_booked']:
                return False
            
            cursor.execute("UPDATE schedule_slots SET is_booked = 1 WHERE id = ?", (slot_id,))
            
            service_ids = json.loads(slot['service_ids'])
            main_service_id = service_ids[0] if service_ids else None
            
            cursor.execute("""
                INSERT INTO bookings (master_id, service_id, client_name, booking_date, booking_time, notes, status)
                VALUES (?, ?, ?, ?, ?, ?, 'confirmed')
            """, (slot['master_id'], main_service_id, client_name, slot['slot_date'], slot['start_time'], notes))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Booking transaction error: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def delete_schedule_slot(self, slot_id: int) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM schedule_slots WHERE id = ?", (slot_id,))
        conn.commit()
        conn.close()
        return True

 
    def get_or_create_client(self, user_id: str, name: str = "", phone: str = "") -> Dict:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE user_id = ?", (user_id,))
        client = cursor.fetchone()
        if client:
            conn.close()
            return dict(client)
        cursor.execute("INSERT INTO clients (user_id, name, phone) VALUES (?, ?, ?)", (user_id, name, phone))
        conn.commit()
        client_id = cursor.lastrowid
        conn.close()
        return self.get_client_by_id(client_id)

    def get_client_by_id(self, client_id: int) -> Optional[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        client = cursor.fetchone()
        conn.close()
        return dict(client) if client else None

    def update_client(self, client_id: int, **kwargs) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        allowed_fields = ['name', 'phone', 'email']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not updates:
            conn.close()
            return False
        updates['updated_at'] = datetime.now().isoformat()
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [client_id]
        cursor.execute(f"UPDATE clients SET {set_clause} WHERE id = ?", values)
        conn.commit()
        conn.close()
        return True

 
    def check_user_role(self, user_id: str) -> str:
        """
        Проверяет, кем является пользователь.
        Возвращает: 'master', 'client' или 'new'
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
 
        cursor.execute("SELECT id FROM masters WHERE user_id = ?", (user_id,))
        if cursor.fetchone():
            conn.close()
            return 'master'
            
 
        cursor.execute("SELECT id FROM clients WHERE user_id = ?", (user_id,))
        if cursor.fetchone():
            conn.close()
            return 'client'
            
        conn.close()
        return 'new'