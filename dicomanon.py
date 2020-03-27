import pydicom
import sys
import glob
import os
import pathlib

import shutil
import dicom2nifti

# path output
ANON_STUDY_P=''


TO_NIFTI=False

# main function
def main():
    global ANON_STUDY_P
    global TO_NIFTI
    if len(sys.argv)<2:
        print('please especify input directory')
        exit()
    elif len(sys.argv)<3:
        print('please especify output directory')
        exit()
        pass
    elif len(sys.argv)<4:
        print('please especify a format option')
        exit()

    # directory where are located the studies to anonymize
    directory=sys.argv[1]
    
    # output directory for anonymized data
    ANON_STUDY_P=sys.argv[2]
    
    # format option --nifti or --dicom
    if sys.argv[3]=='--nifti':
        TO_NIFTI=True
    elif sys.argv[3]=='--dicom':
        TO_NIFTI=False
    else:
        print('please select valid format option')
        exit()
    
    loopPath(directory)

    return True

# loop searching for dicom files,
# if find a dicom file anonimize it 
# and save it in another folder
# receive a directory as an input
def loopPath(directory):

    # search for subpaths
    paths=glob.glob(directory+'/*', recursive=True)
    
    # if there is not subpaths
    if  len(paths)==0 :
        pass
    # if the subpath are files
    elif os.path.isfile(paths[0]):
        
        # new path for anonimized images
        anon_studypath=ANON_STUDY_P+directory[directory.find('/'):]
        
        # create folder for the anonyme data
        pathlib.Path(anon_studypath).mkdir(parents=True, exist_ok=True)

        # anonymize images 
        images=anonymizeStudy(paths)

        # if no image was anonymized delete the folder
        if len(images)==0:
            os.rmdir(anon_studypath)
        # if format option is --nifti
        elif TO_NIFTI:
            try:
                dicom2nifti.convert_dicom.dicom_array_to_nifti(images, anon_studypath,reorient_nifti=True)
                shutil.rmtree(anon_studypath) #delete folder with dicom files
            except:
                print("error converting to nifti study %s" % directory )            
            
        print('%d Anonymized files in study %s ' %(len(images),directory))
        

        return directory
    # if the subpaths are not files search files in the subpaths
    else:
        for path in paths:
            loopPath(path)

# function that anonymize study
# receibe a path of the estudy
# return the array of anonymized images
def anonymizeStudy(study):
    

    images=[]

    # loop for every image in the study
    # for filename in glob.glob(study+'/*', recursive=True):
    for filename in study:

        # read the image
        try:
            image=pydicom.dcmread(filename)

            output_filepath=ANON_STUDY_P+filename[filename.find('/'):]

            # if anonymize and save only image of CT and MR
            if image.Modality in {'CT','MR'}:
                # anonymize one image
                # if image is anonymized save th image ina new folder
                if(anonymizeOne(image)):
                    try:
                        image.save_as(output_filepath) # save anonymized image
                        images.append(image)
                    except:
                        print('Error saving anonymized images')
                else:
                    print('Error anonymising image')
        except:
            print('error opening file %s' % filename)

    # Return the number of images anonymize
    return images


# function that anonymize 1 image, 
# receive  and image as an input 
# return true if false if an erro occurred
def anonymizeOne(image):

    # array of dictionaries that define the element and the action,
    # Elements to anonymize -> https://support.qmenta.com/hc/en-us/articles/209558109-What-is-DICOM-anonymization-
    # replace = replace with dummy value
    # remove = delete the element
    remove_elements = [
        {'value':'AccessionNumber','action':'replace'},
        {'value':'InstitutionName','action':'remove'},
        {'value':'ReferringPhysicianIDSequence','action':'remove'},
        {'value':'PhysiciansOfRecord','action':'remove'},
        {'value':'PhysiciansOfRecordIDSequence','action':'remove'},
        {'value':'PerformingPhysicianName','action':'remove'},
        {'value':'PerformingPhysicianIDSequence','action':'remove'},
        {'value':'NameOfPhysicianReadingStudy','action':'remove'},
        {'value':'PhysicianReadingStudyIDSequence','action':'remove'},
        {'value':'PatientBirthDate'	,'action':'replace'},
        {'value':'PatientInsurancePlanCodeSequence','action':'remove'},
        {'value':'PatientPrimaryLanguageCodeSeq','action':'remove'},
        {'value':'OtherPatientIDs','action':'remove'},
        {'value':'OtherPatientNames','action':'remove'},
        {'value':'OtherPatientIDsSequence','action':'remove'},
        {'value':'PatientAge','action':'remove'},
        {'value':'PatientAddress','action':'remove'},
        {'value':'PatientMotherBirthName','action':'remove'},
        {'value':'PatientName','action':'replace'},
        {'value':'PatientID','action':'replace'},
        {'value':'IssuerOfPatientID','action':'remove'},
        {'value':'PatientBirthTime','action':'remove'},
        {'value':'PatientSex','action':'replace'},
        {'value':'OtherPatientIDs','action':'remove'},
        {'value':'OtherPatientNames','action':'remove'},
        {'value':'PatientBirthName','action':'remove'},
        {'value':'CountryOfResidence','action':'remove'},
        {'value':'RegionOfResidence','action':'remove'},
        {'value':'PatientTelephoneNumbers','action':'remove'},
        {'value':'CurrentPatientLocation','action':'remove'},
        {'value':'PatientInstitutionResidence','action':'remove'},
        {'value':'StudyDate','action':'replace'},
        {'value':'SeriesDate','action':'remove'},
        {'value':'AcquisitionDate','action':'remove'},
        {'value':'ContentDate'	,'action':'replace'},
        {'value':'OverlayDate','action':'remove'},
        {'value':'CurveDate','action':'remove'},
        {'value':'AcquisitionDateTime','action':'remove'},
        {'value':'StudyTime'	,'action':'replace'},
        {'value':'SeriesTime','action':'remove'},
        {'value':'AcquisitionTime','action':'remove'},
        {'value':'ContentTime'	,'action':'replace'},
        {'value':'OverlayTime','action':'remove'},
        {'value':'CurveTime','action':'remove'},
        {'value':'InstitutionAddress','action':'remove'},
        {'value':'ReferringPhysicianName','action':'replace'},
        {'value':'ReferringPhysicianAddress','action':'remove'},
        {'value':'ReferringPhysicianTelephoneNumber','action':'remove'},
        {'value':'InstitutionalDepartmentName','action':'remove'},
        {'value':'OperatorsName','action':'remove'},
        {'value':'StudyID','action':'replace'},
        {'value':'DateTime','action':'remove'},
        {'value':'Date','action':'remove'},
        {'value':'Time','action':'remove'},
        {'value':'PersonName','action':'replace'},
        {'value':'RequestAttributesSequence','action':'remove'},
    ]
    

    try:
        image.remove_private_tags() #reomeve private tags
        # lop for elements to anonymize
        for element in remove_elements:
            # if element exist anonymize
            if element['value'] in image:
                if element['action']=='replace':
                    image.data_element(element['value']).value = '19000101' #dummy value
                elif element['action']=='remove':
                    delattr(image, element['value'])  #delete value
        return True
        
    except:
        return False
    
        

    

if __name__ == "__main__":
    res=main()
    pass