# Anonymization dicom studies

Script to anonymize dicom sudies from a folder, the script loop for all folders in the input directory and  save the anonymazed dicom image  in another directory, the image can be saved in NIFTI or dicom.

## Attributes and data to anonymize

<table>
    <thead>
        <tr> 
            <th>DICOM Attributes</th>
            <th>Action</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>AccessionNumber</td>
            <td>Replace Dummy</td>
        <tr>
            <td>InstitutionName</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>ReferringPhysicianIDSequence</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>PhysiciansOfRecord</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>PhysiciansOfRecordIDSequence</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>PerformingPhysicianName</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>PerformingPhysicianIDSequence</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>NameOfPhysicianReadingStudy</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>PhysicianReadingStudyIDSequence</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>PatientInsurancePlanCodeSequence</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>PatientPrimaryLanguageCodeSeq</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>OtherPatientIDs</td>
            <td>Replace</td> 
        </tr>
        <tr>
            <td>OtherPatientNames</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>OtherPatientIDsSequence</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>PatientAddress</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>PatientMotherBirthName</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>PatientName</td>
            <td>Replace Dummy</td>
        </tr>
        <tr>
            <td>PatientID</td>
            <td>Replace Dummy</td>
        </tr>
        <tr>
            <td>IssuerOfPatientID</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>PatientBirthTime</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>OtherPatientIDs</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>OtherPatientNames</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>PatientBirthName</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>CountryOfResidence</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>RegionOfResidence</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>PatientTelephoneNumbers</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>CurrentPatientLocation</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>PatientInstitutionResidence</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>InstitutionAddress</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>ReferringPhysicianName</td>
            <td>Replace Dummy</td>
        </tr>
        <tr>
            <td>ReferringPhysicianAddress</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>ReferringPhysicianTelephoneNumber</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>InstitutionalDepartmentName</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>OperatorsName</td>
            <td>Remove</td>
        </tr>
        <tr>
            <td>StudyID</td>
            <td>Replace</td> 
        </tr>
        <tr>
            <td>PersonName</td>
            <td>Replace Dummy</td>
        </tr>
        <tr>
            <td>RequestAttributesSequence</td>
            <td>Remove</td>
        </tr>
    </tbody>
</table>

### Action description

<table>
  <tr>
    <th>Action</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Replace Dummy</td>
    <td>Replace to a dummy value, the used value is '19000101'</td>
  </tr>
  <tr>
    <td>Remove</td>
    <td>Remove the attribute from DICOM image</td>
  </tr>
  <tr>
    <td>Replace</td>
    <td>Replace data to a similar value</td>
  </tr>
</table>

## Using the Script 🚀

### Requirements 📋

This script use pydicom and dicom2nifti libraries

```
pip install pydicom
pip install dicom2nifti
```

### Anonymize dicom images 🔧

Call dicomanon.py especifying input directory, output directory and ouput format

```
python dicomanon.py input_directory output_directory --format_option
```

format options:
* --nifti
* --dicom



## Used libraries 🛠️

* [pydicom](https://github.com/pydicom/pydicom)
* [dicom2nifti](https://github.com/icometrix/dicom2nifti/tree/master/scripts/)

