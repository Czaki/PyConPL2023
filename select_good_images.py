# https://gist.github.com/alisterburt/32ac8dc03a5e5083a80475bce44ab172

from pathlib import Path

import imageio
import numpy as np
import napari
from napari.utils.notifications import show_info

IMAGE_FILE_PATTERN = 'images/*'
DIRECTORY_FOR_GOOD_IMAGES = 'good_images'

# get list of all image files
image_files = list(Path('.').glob(IMAGE_FILE_PATTERN))

# make directory for good images
Path(DIRECTORY_FOR_GOOD_IMAGES).mkdir(exist_ok=True, parents=True)

# make a napari viewer and activate a text overlay to show filenames
viewer = napari.Viewer()
viewer.text_overlay.visible = True
viewer.text_overlay.position = 'top_left'


# function for loading files and storing metadata
def load_image(image_path: Path):
    data = np.array(imageio.v2.imread(image_path))
    if 'image' not in viewer.layers:
        viewer.add_image(data, name='image')
    else:
        viewer.layers['image'].data = data
    viewer.layers['image'].metadata['image_path'] = image_path
    viewer.text_overlay.text = image_path.stem
    viewer.reset_view()


# load first image
load_image(image_files[0])


# key bindings for image switching
@viewer.bind_key('Right')
def next_image(viewer):
    current_idx = image_files.index(viewer.layers['image'].metadata['image_path'])
    idx = current_idx + 1
    if idx >= len(image_files):
        idx = 0
    load_image(image_files[idx])


@viewer.bind_key('Left')
def previous_image(viewer):
    current_idx = image_files.index(viewer.layers['image'].metadata['image_path'])
    idx = current_idx - 1
    if idx < 0:
        idx = len(image_files) - 1
    load_image(image_files[idx])


# key binding to select a good image
@viewer.bind_key('Enter')
def valid_image(viewer):
    print("aaaa")
    image_path = viewer.layers['image'].metadata['image_path']
    output_path = Path(DIRECTORY_FOR_GOOD_IMAGES) / image_path.name
    image_path.rename(output_path)
    next_image(viewer)
    image_files.remove(image_path)
    show_info(f'{image_path.stem} -> {output_path.name}')


# start the event loop
napari.run()
