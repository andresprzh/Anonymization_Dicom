import dicom2nifti
import pydicom
import sys
import glob
import os
import pathlib

import shutil
import  csv

# last index of input directory
INPUT_FOLDER_INDEX = 0

# path output
ANON_STUDY_P = ''


TO_NIFTI = False

ID_PATIENT_DATA = []

# main function
def main():


    global INPUT_FOLDER_INDEX
    global ANON_STUDY_P
    global TO_NIFTI
    global ID_PATIENT_DATA

    

    if len(sys.argv)<2:
        print('please especify input directory')
        exit()
    elif len(sys.argv)<3:
        print('please especify output directory')
        exit()
        pass
    elif len(sys.argv)<4:
        print('please especify csv file')
        exit()
    elif len(sys.argv)<5:
        print('please especify a format option')
        exit()

    # directory where are located the studies to anonymize
    directory=sys.argv[1]
    if directory[-1]!='/':
        directory=directory+"/"
    
    # last index of string of the input directory
    INPUT_FOLDER_INDEX=len(directory)-1

    # output directory for anonymized data
    ANON_STUDY_P=sys.argv[2]
    if ANON_STUDY_P[-1]!='/':
        ANON_STUDY_P=ANON_STUDY_P+"/"
    
    # File to asign a valid number to the patient ID
    with open(sys.argv[3], newline='') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for row in spamreader:
            ID_PATIENT_DATA.append({'idpatient':row['idpatient'],'id':row['id']})

    # format option --nifti or --dicom
    if sys.argv[4]=='--nifti':
        TO_NIFTI=True
    elif sys.argv[4]=='--dicom':
        TO_NIFTI=False
    else:
        print('please select valid format option')
        exit()
    
    loopPath(directory)

    return True
def anom_path(path):
    for row in ID_PATIENT_DATA:
        new_path = path.replace(row['idpatient'], row['id'])
        if path != new_path:
            return new_path
    return path
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
        anon_studypath = ANON_STUDY_P+directory[INPUT_FOLDER_INDEX:]
        anon_studypath = anom_path(anon_studypath)

        # create folder for the anonyme data
        pathlib.Path(anon_studypath).mkdir(parents=True, exist_ok=True)

        print('***Anonymizing study %s ***' % directory)

        # anonymize images 
        images=anonymizeStudy(paths)

        # if no image was anonymized delete the folder
        if len(images)==0:
            os.rmdir(anon_studypath)
        # if format option is --nifti
        elif TO_NIFTI:
            try:
                dicom2nifti.convert_dicom.dicom_array_to_nifti(images, anon_studypath,reorient_nifti=False)
                shutil.rmtree(anon_studypath) #delete folder with dicom files
            except Exception as e: 
                print("ERROR converting to nifti ")         
            
        print('%d Anonymized files and saved in  %s ' %(len(images),anon_studypath))
        

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
        read = False
        # read the image
        try:
            image=pydicom.dcmread(filename)
            output_filepath=ANON_STUDY_P+filename[INPUT_FOLDER_INDEX:]
            output_filepath = anom_path(output_filepath)
            read = True
        except:
            print('error opening file %s' % filename)
        if (read):
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
        

    # Return the number of images anonymize
    return images

# search for the id
def searchid(id):
    for row in ID_PATIENT_DATA:
        if row['idpatient'] == id:
            return row['id']

# function that anonymize 1 image, 
# receive  and image as an input 
# return true if false if an erro occurred
def anonymizeOne(image):

    # array of dictionaries that define the element and the action,
    # Elements to anonymize -> https://support.qmenta.com/hc/en-us/articles/209558109-What-is-DICOM-anonymization-
    # replace = replace with dummy value
    # remove = delete the element
    remove_elements = [
        {'key':(0x0008,0x0050),'value':'AccessionNumber','action':'replace'},
        {'key':(0x0008,0x0080),'value':'InstitutionName','action':'remove'},
        {'key':(0x0008,0x0096),'value':'ReferringPhysicianIDSequence','action':'remove'},
        {'key':(0x0008,0x1048),'value':'PhysiciansOfRecord','action':'remove'},
        {'key':(0x0008,0x1049),'value':'PhysiciansOfRecordIDSequence','action':'remove'},
        {'key':(0x0008,0x1050),'value':'PerformingPhysicianName','action':'remove'},
        {'key':(0x0008,0x1052),'value':'PerformingPhysicianIDSequence','action':'remove'},
        {'key':(0x0008,0x1060),'value':'NameOfPhysicianReadingStudy','action':'remove'},
        {'key':(0x0008,0x1062),'value':'PhysicianReadingStudyIDSequence','action':'remove'},
        {'key':(0x0010,0x0050),'value':'PatientInsurancePlanCodeSequence','action':'remove'},
        {'key':(0x0010,0x0101),'value':'PatientPrimaryLanguageCodeSeq','action':'remove'},
        #{'key':(0x0010,0x1000),'value':'OtherPatientIDs','action':'replace-valid'},
        {'key':(0x0010,0x1000),'value':'OtherPatientIDs','action':'replace'},
        {'key':(0x0010,0x0010),'value':'PatientName','action':'remove'},
        {'key':(0x0010,0x1002),'value':'OtherPatientIDsSequence','action':'remove'},
        {'key':(0x0010,0x1040),'value':'PatientAddress','action':'remove'},
        {'key':(0x0010,0x1060),'value':'PatientMotherBirthName','action':'remove'},
        {'key':(0x0010,0x0010),'value':'PatientName','action':'replace'},
        {'key':(0x0010,0x0020),'value':'PatientID','action':'replaceid'},
        {'key':(0x0010,0x0021),'value':'IssuerOfPatientID','action':'remove'},
        {'key':(0x0010,0x0032),'value':'PatientBirthTime','action':'remove'},
        {'key':(0x0010,0x1000),'value':'OtherPatientIDs','action':'remove'},
        {'key':(0x0010,0x1001),'value':'OtherPatientNames','action':'remove'},
        {'key':(0x0010,0x1005),'value':'PatientBirthName','action':'remove'},
        {'key':(0x0010,0x2150),'value':'CountryOfResidence','action':'remove'},
        {'key':(0x0010,0x2152),'value':'RegionOfResidence','action':'remove'},
        {'key':(0x0010,0x2154),'value':'PatientTelephoneNumbers','action':'remove'},
        {'key':(0x0038,0x0300),'value':'CurrentPatientLocation','action':'remove'},
        {'key':(0x0038,0x0400),'value':'PatientInstitutionResidence','action':'remove'},
        {'key':(0x0008,0x0081),'value':'InstitutionAddress','action':'remove'},
        {'key':(0x0008,0x0090),'value':'ReferringPhysicianName','action':'replace'},
        {'key':(0x0008,0x0092),'value':'ReferringPhysicianAddress','action':'remove'},
        {'key':(0x0008,0x0094),'value':'ReferringPhysicianTelephoneNumber','action':'remove'},
        {'key':(0x0008,0x1040),'value':'InstitutionalDepartmentName','action':'remove'},
        {'key':(0x0008,0x1070),'value':'OperatorsName','action':'remove'},
        #{'key':(0x0020,0x0010),'value':'StudyID','action':'replace-valid'},
        {'key':(0x0020,0x0010),'value':'StudyID','action':'replace'},
        {'key':(0x0040,0xA123),'value':'PersonName','action':'replace'},
        {'key':(0x0040,0x0275),'value':'RequestAttributesSequence','action':'remove'},
        {'key':(0x0032,0x1032),'value':'RequestingPhysician','action':'remove'}
        	

    ]

    try:
        image.remove_private_tags() #reomeve private tags
        # lop for elements to anonymize
        for element in remove_elements:
            # if element exist anonymize
            if element['key'] in image:
                if element['action']=='replace':
                    # image.data_element(element['key']).value = '19000101' #dummy value
                    image[element['key']].value = '19000101' #dummy value
                elif element['action']=='replaceid':
                    image[element['key']].value = searchid(image[element['key']].value) #dummy value
                elif element['action']=='remove':
                    delattr(image, element['value'])  #delete value
        return True
        
    except:
        return False
    
        

    

if __name__ == "__main__":
    res=main()
    pass