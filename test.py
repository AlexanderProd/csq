import cv2
from cv2 import dnn_superres

# Create an SR object
sr = dnn_superres.DnnSuperResImpl_create()

# Read image
image = cv2.imread("/Users/alexanderhoerl/Downloads/285uy-FLIR0494.csq-turbo.png")

# Read the desired model
path = "models/LapSRN_x4.pb"
sr.readModel(path)

# Set the desired model and scale to get correct pre- and post-processing
sr.setModel("edsr", 4)

# Upscale the image
result = sr.upsample(image)

# Save the image
cv2.imwrite("/Users/alexanderhoerl/Downloads/upscaled.png", result)
