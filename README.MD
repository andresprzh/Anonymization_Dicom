# Anonymization dicom studies

Script to anonymize dicom sudies from a folder, the script loop for all folders in the input directory and  save the anonymazed dicom image  in another directory, the image can be saved in NIFTI or dicom.

## Using the Script 🚀

### Requirements 📋

This script use the pydicom and dicom2nifti libraries

```
pip install pydicom
pip install dicom2nifti
```

### Anonimize dicom images 🔧

call dicomanon.py especifying input directory output directory and ouput format

```
python dicomanon.py input_directory output_directory --format_option
```

format options:
* --nifti
* --dicom



## Used libraries 🛠️

* [pydicom](https://github.com/pydicom/pydicom)
* [dicom2nifti](https://github.com/icometrix/dicom2nifti/tree/master/scripts/)

