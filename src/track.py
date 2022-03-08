import dataclasses
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Track:
    id: str
    title: str
    artists: List[str]
    album: Optional[str]
    duration: int

    def dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)
