import nibabel as nib
import napari
import numpy as np

nifti_img = nib.load('cropped_norm/cropped_norm/pat0_cropped_norm.nii.gz')
image_data = np.transpose(nifti_img.get_fdata(), (2, 1, 0)).astype(np.float32)

viewer = napari.Viewer()
viewer.add_image(image_data, name='MRI', colormap='gray', rendering='mip')

napari.run()