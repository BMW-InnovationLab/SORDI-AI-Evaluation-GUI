from typing import Optional

from pydantic import BaseModel


class BoundingBox(BaseModel):
    left: float
    right: float
    top: float
    bottom: float
    width: Optional[float]
    height: Optional[float]

    @property
    def centroid(self):
        return self.left + (self.width / 2), self.top + (self.height / 2)

    @property
    def area(self):
        return (self.right - self.left) * (self.bottom - self.top)
