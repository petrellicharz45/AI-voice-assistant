from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any

@dataclass
class ChatMessage:
    """
    Represents a single message in a conversation
    """
    content: str
    sender: str  # 'user' or 'assistant'
    timestamp: datetime = field(default_factory=datetime.now)
    message_type: str = 'text'  # 'text', 'voice', 'image', etc.
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert message to dictionary representation
        """
        return {
            'content': self.content,
            'sender': self.sender,
            'timestamp': self.timestamp.isoformat(),
            'message_type': self.message_type,
            'metadata': self.metadata or {}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatMessage':
        """
        Create a ChatMessage from a dictionary
        """
        return cls(
            content=data['content'],
            sender=data['sender'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            message_type=data.get('message_type', 'text'),
            metadata=data.get('metadata')
        )