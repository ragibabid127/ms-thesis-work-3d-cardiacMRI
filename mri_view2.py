import SimpleITK as sitk
import napari
import numpy as np

image = sitk.ReadImage('your_image.nii.gz')
image_np = sitk.GetArrayFromImage(image)  # (Z, Y, X)
viewer = napari.Viewer()
viewer.add_image(image_np, name="MRI", colormap="gray", rendering="mip")
napari.run()