# Installation
### Dependencies
 - opencv-python (>=4.3.0.36)
 - numpy (>= 1.19.1)
 - pandas (>= 1.1.0)
# Detect Exposure
Detect exposure of an image. If it passes, then return True, else False.

### Dependencies:
 - CorrectExposure
### Parameters:
- __image__ : numpy.ndarray, image type is gray, default : None
- __type__ : string, default : None, could be : None, 401, 403, BS, IS.
### Returns:
- __boolean__

### Methods:
- __fit__()

### Examples:

```python
import cv2 as cv
from detect_exposure import DetectExposure

img = cv.imread(path, cv.IMREAD_GRAYSCALE) #read image
detectExposure = DetectExposure(img)
pass = detectExposure.fit() #pass = True or False
```

# Correct Exposure
correct exposure of an image.

### Parameters
- __image__ : numpy.ndarray, image type is gray, default : None
- __times__ : int, fit x times, default : 10

### Returns
- __image__ : numpy.ndarray, image type is gray

### Methods:
- __fit__()

### Examples

```python
import cv2 as cv
from correct_exposure import CorrectExposure

img = cv.imread(path, cv.IMREAD_GRAYSCALE) #read image
correctExposure = CorrectExposure(img)
correct_img = correctExposure.fit()
```