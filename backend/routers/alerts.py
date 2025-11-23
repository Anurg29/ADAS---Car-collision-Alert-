from fastapi import APIRouter, HTTPException, Response
import mysql.connector
from mysql.connector import pooling
from typing import List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/alerts", tags=["alerts"])

db_config = {
    'user': 'root',
    'password': 'Anurag*29',
    'host': 'localhost',
    'database': 'car',
    'pool_name': 'alert_pool',
    'pool_size': 5
}

# Create connection pool
try:
    connection_pool = pooling.MySQLConnectionPool(**db_config)
except mysql.connector.Error as err:
    print(f"Error creating connection pool: {err}")
    connection_pool = None

class Alert(BaseModel):
    id: int
    timestamp: datetime
    object_class: str
    confidence: float
    distance: float
    image_path: str

@router.get("/", response_model=List[Alert])
def get_alerts(limit: int = 10):
    """Get recent alerts from database"""
    cnx = None
    cursor = None
    try:
        if connection_pool:
            cnx = connection_pool.get_connection()
        else:
            cnx = mysql.connector.connect(**{k: v for k, v in db_config.items() if k not in ['pool_name', 'pool_size']})
        
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT id, timestamp, object_class, confidence, distance, image_path FROM alerts ORDER BY id DESC LIMIT %s"
        cursor.execute(query, (limit,))
        alerts = cursor.fetchall()
        return alerts
    except mysql.connector.Error as err:
        print(f"Database not available for alerts: {err}")
        return []  # Return empty list when database is offline
    except Exception as e:
        print(f"Error fetching alerts: {e}")
        return []  # Return empty list on error
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

@router.get("/{alert_id}/image")
def get_alert_image(alert_id: int):
    cnx = None
    cursor = None
    try:
        if connection_pool:
            cnx = connection_pool.get_connection()
        else:
            cnx = mysql.connector.connect(**{k: v for k, v in db_config.items() if k not in ['pool_name', 'pool_size']})
        
        cursor = cnx.cursor()
        query = "SELECT image_data FROM alerts WHERE id = %s"
        cursor.execute(query, (alert_id,))
        result = cursor.fetchone()
        
        if result and result[0]:
            return Response(content=result[0], media_type="image/jpeg")
        else:
            raise HTTPException(status_code=404, detail="Image not found")
            
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()
