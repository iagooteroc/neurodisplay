# Neurodisplay

<p align="center"><img src="https://user-images.githubusercontent.com/22031856/76228050-8058cc00-6220-11ea-917a-65e2ff19e194.png" alt="screenshot" width="600"></p>

This is a script that displays brain scan volumes as slices in three different views at the same time. It can show up to two different brain volumes at once for comparison.
It can also overlay binary images to visualize segmentations.

## Requirements

This script uses scans in a `.nii.gz` format, so the [nibabel](https://nipy.org/nibabel/) package is required. You also need [opencv](https://pypi.org/project/opencv-python/) and [numpy](https://numpy.org/).

To install them, simply type the following, and press enter:

```shell
pip install -r requirements.txt
```

## Run the script

To run the script, type the following and press enter:
```shell
python neurodisplay.py -i <volume_name.nii.gz> [-j <volume_name2.nii.gz> ...]
```
Replace the string `<volume_name.nii.gz>` from above with the path to your volume and add the following optional parameters as desired:
- `-j`: path to a secondary brain volume for comparison which will be displayed below de first one.
- `-x`: path to a binary segmentation volume which will be overlaid on the first volume.
- `-y`: path to a secondary binary segmentation volume which will be overlaid on the second volume.

It is possible to provide only one brain volume and two segmentations. In that case, the same volume will be displayed on both rows.

### Examples

Single brain volume:
```shell
python neurodisplay.py -i images/t1.nii.gz
```
Single brain volume with overlaid segmentation:
```shell
python neurodisplay.py -i images/t1.nii.gz -x pred/t1.nii.gz
```
Two brain volumes with overlaid segmentation:
```shell
python neurodisplay.py -i images/t1.nii.gz -j images_t1ce/t1ce.nii.gz -x pred/t1.nii.gz -y labels/lab.nii.gz
```

### Usage

```
usage: neurodisplay.py [-h] -i I [-j J] [-x X] [-y Y]

Display neuroimages with binary labels. At least one brain image (-i) is required

optional arguments:
  -h, --help  show this help message and exit
  -i I        path to the top brain image (required)
  -j J        path to the bottom brain image
  -x X        path to the top label image
  -y Y        path to the bottom label image
```
