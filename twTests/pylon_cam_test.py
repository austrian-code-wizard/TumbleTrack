from pypylon import pylon
import numpy as np
from matplotlib import pyplot as plt
import time

# TODO pylon docs: https://docs.baslerweb.com/#t=en%2Fdaa2500-14uc.htm

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()
camera.PixelFormat = "RGB8"
camera.BinningHorizontal = 4
camera.BinningVertical = 4

while True:
    result = camera.GrabOne(1000)

    if result.GrabSucceeded():
        img = result.Array
        print(result.Width, result.Height, np.mean(img))
        print(img.shape)
        plt.imshow(result.Array)
        plt.show()

    result.Release()
    time.sleep(0.5)

camera.Close()