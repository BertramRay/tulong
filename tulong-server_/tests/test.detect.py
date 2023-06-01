import os
from tulong_api.core.detector import StyleDetector


shapeDetector = StyleDetector(
    os.path.abspath(os.path.dirname(__file__)) + "/images/1.png"
)
shapeDetector.detect()
