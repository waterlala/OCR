# Installation
### Dependencies
 - opencv-python (>=4.3.0.36)
 - numpy (>= 1.19.1)
 - pandas (>= 1.1.0)
# Detect Exposure
Detect exposure of an image. If it passes, then return True, else False.

### Input
image (type = GRAY)
type
 - type = string
 - default = 'None'
### Output
boolean

### Use Example

```sh
import cv2 as cv
from detect_exposure import DetectExposure

img = cv.imread(path, cv.IMREAD_GRAYSCALE) #read image
detectExposure = DetectExposure(img)
pass = detectExposure.fit() #pass = True or False
```

# Correct Exposure
correct exposure of an image.

### Input
image (type = GRAY)
### Output
image (type = GRAY)

### Use Example

```sh
import cv2 as cv
from correct_exposure import CorrectExposure

img = cv.imread(path, cv.IMREAD_GRAYSCALE) #read image
correctExposure = CorrectExposure(img)
correct_img = correctExposure.fit()
```