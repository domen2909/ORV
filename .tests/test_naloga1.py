import cv2 as cv
import numpy as np
from naloga1 import zmanjsaj_sliko

def test_zmanjsaj_sliko():
    slika = np.zeros((100, 100, 3), dtype=np.uint8)
    nova = zmanjsaj_sliko(slika, 50, 50)
    assert nova.shape == (50, 50, 3)
