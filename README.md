# Installation
### Dependencies
 - opencv-python (>=4.3.0.36)
 - numpy (>= 1.19.1)
 - pandas (>= 1.1.0)
# Detect Exposure
Detect exposure of an image. If it passes, then return True, else False.

### Input
image (type = GRAY)
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

# Exposure Correction
correct exposure of an image.

### Input
image (type = GRAY)
### Output
image (type = GRAY)

### Use Example

```sh
import cv2 as cv
from exposure_image import ExposureImage

img = cv.imread(path, cv.IMREAD_GRAYSCALE) #read image
exposureImage = ExposureImage(img)
correct_img = exposureImage.fit()
```