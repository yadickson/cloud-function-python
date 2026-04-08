from dataclasses import dataclass, field
from typing import List


@dataclass
class FileModel:
    filename: str
    content: bytes
    relations: List[str] = field(default_factory=list)
