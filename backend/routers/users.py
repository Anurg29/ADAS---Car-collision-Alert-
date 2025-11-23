from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional
import mysql.connector
from mysql.connector import pooling
from datetime import datetime

router = APIRouter()

# Database connection pool (optional - works without MySQL)
try:
    db_pool = pooling.MySQLConnectionPool(
        pool_name="user_pool",
        pool_size=5,
        host='localhost',
        user='root',
        password='Anurag*29',
        database='car'
    )
    print("✓ User database pool created")
except Exception as e:
    print(f"⚠ MySQL not available for users: {e}")
    db_pool = None

class UserCreate(BaseModel):
    uid: str
    email: str
    display_name: Optional[str] = None
    email_verified: bool = False

class UserLogin(BaseModel):
    uid: str
    email: str

def get_db():
    """Get database connection from pool"""
    if db_pool is None:
        raise HTTPException(status_code=503, detail="Database not available")
    try:
        return db_pool.get_connection()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

@router.post("/users/register")
async def register_user(user: UserCreate):
    """Register new user in MySQL when they sign up via Firebase"""
    conn = get_db()
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE uid = %s OR email = %s", (user.uid, user.email))
        existing = cursor.fetchone()
        
        if existing:
            return {"message": "User already exists", "user_id": existing['id']}
        
        # Insert new user
        query = """
        INSERT INTO users (uid, email, display_name, email_verified, role)
        VALUES (%s, %s, %s, %s, 'user')
        """
        cursor.execute(query, (user.uid, user.email, user.display_name, user.email_verified))
        conn.commit()
        user_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return {"message": "User registered successfully", "user_id": user_id}
        
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/users/login")
async def log_user_login(user: UserLogin, user_agent: Optional[str] = Header(None), x_forwarded_for: Optional[str] = Header(None)):
    """Log user login and update last_login"""
    conn = get_db()
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Update last_login
        cursor.execute("UPDATE users SET last_login = NOW() WHERE uid = %s", (user.uid,))
        
        # Get user_id
        cursor.execute("SELECT id FROM users WHERE uid = %s", (user.uid,))
        user_data = cursor.fetchone()
        
        if user_data:
            # Log session
            cursor.execute("""
                INSERT INTO user_sessions (user_id, ip_address, user_agent)
                VALUES (%s, %s, %s)
            """, (user_data['id'], x_forwarded_for or 'unknown', user_agent or 'unknown'))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {"message": "Login logged successfully"}
        
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{uid}")
async def get_user(uid: str):
    """Get user details by UID"""
    conn = get_db()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, uid, email, display_name, email_verified, created_at, last_login, role, is_active FROM users WHERE uid = %s", (uid,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/users")
async def get_all_users():
    """Get all users (admin only - add auth later)"""
    conn = get_db()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, uid, email, display_name, email_verified, created_at, last_login, role, is_active
            FROM users
            ORDER BY created_at DESC
        """)
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return {"users": users, "total": len(users)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/users/{user_id}/alerts")
async def get_user_alerts(user_id: int):
    """Get all alerts for a specific user"""
    conn = get_db()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, timestamp, object_class, confidence, distance, image_path
            FROM alerts
            WHERE user_id = %s
            ORDER BY timestamp DESC
        """, (user_id,))
        alerts = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return {"alerts": alerts, "total": len(alerts)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/stats")
async def get_admin_stats():
    """Get overall system statistics"""
    conn = get_db()
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Total users
        cursor.execute("SELECT COUNT(*) as total FROM users")
        total_users = cursor.fetchone()['total']
        
        # Total alerts
        cursor.execute("SELECT COUNT(*) as total FROM alerts")
        total_alerts = cursor.fetchone()['total']
        
        # Active users (logged in last 24 hours)
        cursor.execute("""
            SELECT COUNT(*) as total 
            FROM users 
            WHERE last_login >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
        """)
        active_users = cursor.fetchone()['total']
        
        # Recent alerts (last 24 hours)
        cursor.execute("""
            SELECT COUNT(*) as total 
            FROM alerts 
            WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
        """)
        recent_alerts = cursor.fetchone()['total']
        
        cursor.close()
        conn.close()
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "total_alerts": total_alerts,
            "recent_alerts": recent_alerts
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
