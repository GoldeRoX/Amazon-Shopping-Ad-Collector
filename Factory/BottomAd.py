from dataclasses import dataclass


@dataclass
class _BottomAd(object):
    _filename: str
    _width: int
    _height: int
    _location_x: int
    _location_y: int
    _text: str
    _timestamp: str
    _ad_type: int = 1

    def __init__(self, filename: str, width: int, height: int, location_x: int,
                 location_y: int, text: str, timestamp: str):
        self._filename = filename
        self._width = width
        self._height = height
        self._location_x = location_x
        self._location_y = location_y
        self._text = text
        self._timestamp = timestamp

    def to_dict(self) -> {}:
        return {"filename": self._filename,
                "width": self._width,
                "height": self._height,
                "location_x": self._location_x,
                "location_y": self._location_y,
                "test": self._text,
                "timestamp": self._timestamp}

    @property
    def filename(self):
        return self._filename

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def location_x(self):
        return self._location_x

    @property
    def ad_type(self):
        return self._ad_type

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def text(self):
        return self._text

    @property
    def location_y(self):
        return self._location_y
