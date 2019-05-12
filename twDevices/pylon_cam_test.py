from pypylon import pylon
import numpy as np

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.StartGrabbingMax(5)

while camera.IsGrabbing():
    result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if result.GrabSucceeded():
        print(result.Width, result.Height, np.mean(result.Array))

    result.Release()


"""
/home/dominik/anaconda3/envs/TumbleTrack/bin/python /home/dominik/Workspace/tumbleweed/TumbleTrack/twDevices/pylon_cam_test.py
Traceback (most recent call last):
  File "/home/dominik/anaconda3/envs/TumbleTrack/lib/python3.7/site-packages/pypylon/pylon.py", line 42, in swig_import_helper
    return importlib.import_module(mname)
  File "/home/dominik/anaconda3/envs/TumbleTrack/lib/python3.7/importlib/__init__.py", line 127, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1006, in _gcd_import
  File "<frozen importlib._bootstrap>", line 983, in _find_and_load
  File "<frozen importlib._bootstrap>", line 967, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 670, in _load_unlocked
  File "<frozen importlib._bootstrap>", line 583, in module_from_spec
  File "<frozen importlib._bootstrap_external>", line 1043, in create_module
  File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
ImportError: libpython3.7m.so.1.0: cannot open shared object file: No such file or directory

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/dominik/Workspace/tumbleweed/TumbleTrack/twDevices/pylon_cam_test.py", line 1, in <module>
    from pypylon import pylon
  File "/home/dominik/anaconda3/envs/TumbleTrack/lib/python3.7/site-packages/pypylon/pylon.py", line 45, in <module>
    _pylon = swig_import_helper()
  File "/home/dominik/anaconda3/envs/TumbleTrack/lib/python3.7/site-packages/pypylon/pylon.py", line 44, in swig_import_helper
    return importlib.import_module('_pylon')
  File "/home/dominik/anaconda3/envs/TumbleTrack/lib/python3.7/importlib/__init__.py", line 127, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
ModuleNotFoundError: No module named '_pylon'
"""