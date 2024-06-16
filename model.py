from pathlib import Path
from onnxruntime import InferenceSession
from opyv8 import Predictor

model = Path("./data/best.onnx")

classes = model.parent.joinpath("./classes.txt").read_text().split("\n")
session = InferenceSession(
    model.as_posix(),
    providers=[
        "CUDAExecutionProvider",
        "CPUExecutionProvider",
    ],
)

predictor = Predictor(session, classes)


def get_russian_classname(classname):
    return {
        'adj': 'прилегающий дефект',
        'int': 'дефект целостности',
        'geo': 'дефект геометрии',
        'pro': 'дефект постобработки',
        'non': 'дефект невыполнения'
    }[classname]


def predict(image):
    return predictor.predict(image)
