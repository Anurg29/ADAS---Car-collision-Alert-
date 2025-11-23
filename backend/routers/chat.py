from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter()

# In-memory storage for when database is offline
mock_alerts = []

class ChatMessage(BaseModel):
    message: str

class Alert(BaseModel):
    id: int
    timestamp: str
    object_class: str
    confidence: float
    distance: float

# Simple offline responses - no API needed!
def get_offline_response(message: str) -> str:
    """Provide helpful responses without API"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['alert', 'recent', 'what', 'show']):
        if len(mock_alerts) > 0:
            recent = mock_alerts[:3]
            response = f"You have {len(mock_alerts)} alerts. Recent detections:\n"
            for alert in recent:
                response += f"- {alert['object_class']} at {alert['distance']:.1f}m ({alert['confidence']*100:.0f}% confidence)\n"
            return response
        return "No alerts detected yet. System is monitoring your surroundings."
    
    elif any(word in message_lower for word in ['safety', 'tip', 'advice', 'improve']):
        return """Here are key safety tips:
• Maintain 3-second following distance
• Check blind spots before lane changes  
• Reduce speed in heavy traffic
• Stay alert, especially during rush hours
• Use ADAS as assistance, not replacement for attention"""
    
    elif any(word in message_lower for word in ['how', 'work', 'explain']):
        return """ADAS uses YOLOv5 AI to detect vehicles in real-time.
When an object comes within 50 meters:
1. System captures image automatically
2. Calculates distance using camera calibration
3. Triggers visual and sound alerts
4. Logs data for your review

The closer the object, the more urgent the alert!"""
    
    elif any(word in message_lower for word in ['distance', 'close', 'far']):
        return """Safe following distances:
• Critical (<30m): Immediate attention needed
• Warning (30-50m): Maintain awareness  
• Safe (>50m): Monitor situation

At highway speeds, maintain at least 3 seconds of following distance."""
    
    else:
        return """I'm your ADAS assistant! Ask me about:
• Recent alerts and detections
• Safety tips and best practices
• How the system works
• Distance recommendations

What would you like to know?"""

@router.post("/chat")
async def chat_with_ai(chat: ChatMessage):
    """AI Assistant - works offline with pre-programmed responses"""
    try:
        # Use offline responses (always works!)
        response_text = get_offline_response(chat.message)
        
        return {
            "response": response_text,
            "timestamp": datetime.now().isoformat(),
            "mode": "offline"
        }
        
    except Exception as e:
        return {
            "response": "I'm here to help! Ask me about alerts, safety tips, or how ADAS works.",
            "timestamp": datetime.now().isoformat(),
            "mode": "offline"
        }

@router.get("/chat/suggestions")
async def get_suggestions():
    """Get AI-powered driving suggestions"""
    if len(mock_alerts) == 0:
        return {"suggestions": [
            "No recent alerts - you're driving safely!",
            "Remember to maintain safe following distance",
            "Stay alert and check your blind spots"
        ]}
    
    close_calls = sum(1 for a in mock_alerts if a['distance'] < 30)
    
    if close_calls > 3:
        return {"suggestions": [
            f"You had {close_calls} close calls - increase following distance",
            "Consider reducing speed in traffic",
            "Take breaks to maintain focus"
        ]}
    else:
        return {"suggestions": [
            f"{len(mock_alerts)} alerts detected - stay aware",
            "Good job maintaining safe distances",
            "Continue monitoring your surroundings"
        ]}

@router.post("/alerts/add")
async def add_alert(alert: Alert):
    """Add alert to memory (for testing without database)"""
    mock_alerts.insert(0, alert.dict())
    if len(mock_alerts) > 50:
        mock_alerts.pop()
    return {"message": "Alert added", "total": len(mock_alerts)}
