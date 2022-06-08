from dataclasses import dataclass


@dataclass
class BrandsRelatedToYourSearch(object):
    filename: str
    width: int
    height: int
    location_x: int
    location_y: int
    text: str
    timestamp: str
    ad_type: int = 2

    def __init__(self, filename: str, width: int, height: int, location_x: int,
                 location_y: int, text: str, timestamp: str):
        self.filename = filename
        self.width = width
        self.height = height
        self.location_x = location_x
        self.location_y = location_y
        self.text = text
        self.timestamp = timestamp

    def to_dict(self) -> {}:
        return {"filename": self.filename,
                "width": self.width,
                "height": self.height,
                "location_x": self.location_x,
                "location_y": self.location_y,
                "test": self.text,
                "timestamp": self.timestamp}