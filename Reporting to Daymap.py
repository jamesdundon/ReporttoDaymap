# Python3 Script to import CSV containing student reporting data,
# automatically remove useless data, then append & re-format other
# data into suitable format for import into Daymap.
#
# Author: Glen McKie & James Dundon
# e: glen.mckie709@schools.sa.edu.au
# e: james.dundon341@schools.sa.edu.au
# Organisation: Modbury High School
#
# Current Version: in progress
# Date: December 2017

#CSV data should be organised using the included CSV titled Yr11_daymap_preparationSubject.csv

# Import pandas library
import pandas as pd
import os

# Read CSV file (Reporting) & input into a Pandas 'data frame'

# Define import path as variable "filename"
# This could be an input variable in later versions...
Input_CSV_File = 'Yr11_daymap_preparationSubject.csv'
print ('Attempting to import Reporting Data from file: "'+ Input_CSV_File + '"...')
Data_In = pd.read_csv(Input_CSV_File)

# Check file import for correctness
print('Import of "' + Input_CSV_File + '" was successful!')
#print(Data_In.tail())

# Check for dodgy student data, may not catch all if have varied subject numbers.
valid_data = False
# Grade types ie term, exam, semester
grade_types = 3
Student_IDS = Data_In['Student ID'].astype('str')
uniqueIDS = []
for student in Student_IDS:
    if Student_IDS.str.count(student).sum() % grade_types != 0:
        if not student in uniqueIDS:
            uniqueIDS.append(student)

if len(uniqueIDS) > 0:
    for student in uniqueIDS:
        print((student)+':','does not have the correct number of grade attributes')
else:
    valid_data = True
    print('All students appear to have the correct number of grade attributes')

while valid_data == True:
    # Creates a list of student ID's
    studentIDS = []
    for i in range(len(Data_In.index)):
        if not Data_In.loc[i]['Student ID'] in studentIDS:
            studentIDS.append(Data_In.loc[i]['Student ID'])
    print('Number of Student ID\'s:',len(studentIDS))

    #Check the length of Index
    print('Length of index:',len(Data_In.index))

    # Required CSV format is:
    # Column 1 = Student_Code
    # Columns 2:_ = Subjects

    # Number of subjects
    Num_subjects = 7

    # Set up a data frame to hold data in converted format

    print('Setting up new data frame to hold imported data...')

    #Required_Format = {'StudentCode' : [''],'Subject1' : [''], 'Subject2' : [''] ,'Subject3' : [''] ,'Subject4' : [''],'Subject5' : [''],'Subject6' : [''],'Subject7' : ['']}
    Required_Format = {'StudentCode' : ['']}
    for i in range(Num_subjects):
        Required_Format['Subject'+str(i+1)] = ['']



    Data_Out = pd.DataFrame(Required_Format)

    # Specify order of Data_Out columns

    #Data_Out = Data_Out[['StudentCode','Subject1','Subject2','Subject3','Subject4','Subject5','Subject6','Subject7']]

    # Would like to automate this based on Num_subjects
    row = pd.Series(['','','','','','','',''], index = ['StudentCode','Subject1','Subject2','Subject3','Subject4','Subject5','Subject6','Subject7'])

    # Creates an empty data frame with rows equalling the length of unique student ID's
    for i in range(len(studentIDS)-1):
                    Data_Out = Data_Out.append(row,ignore_index=True)

    #Check structure
    #print(Data_Out.tail())

    # Create variable to act as index within Data_In AND Data_Out df...
    data_out_index = 0
    data_in_index = 0

    # Loop through each student ID
    for ID in studentIDS:

        #While the student ID matches a row in the dataframe with that ID
        while ID == Data_In.loc[data_in_index]['Student ID']:
            # Extract Student ID from CSV & place data into df 'Data_Out' as Student Code

            Data_Out.loc[data_out_index]['StudentCode'] = Data_In.loc[data_in_index]['Student ID']
            student_code = Data_In.loc[data_in_index]['Student ID']

            # Required data for each subject is "SubjectName: Term 2, Grade, Exam, Grade, Semester, Grade"
            # Term_Grade = Subject grade in INPUT file
            # Exam_Grade = Subject grade2 in INPUT file
            # Semester_Grade = Subject grade3 in INPUT file

            ##############################

            # Extract SUBJECT data & place data into df 'Data_Out' in required format
            # if student_code in row matches current student (handles limited subjects for a student)
            # Cycles through for number of subjects in Num_subjects
            for i in range(Num_subjects):
                if  student_code == Data_In.loc[data_in_index]['Student ID']:
                    subject_name = str(Data_In.loc[data_in_index]['Report Class Code'])
                    term_grade = str(Data_In.loc[data_in_index]['EnteredText'])
                    exam_grade = str(Data_In.loc[data_in_index+1]['EnteredText'])
                    semester_grade = str(Data_In.loc[data_in_index+2]['EnteredText'])
                    # Deal with nan grade bug
                    if(term_grade) == 'nan':
                            term_grade = str('NA')
                    if(exam_grade) == 'nan':
                            exam_grade = str('NA')
                    if(semester_grade) == 'nan':
                            semester_grade = str('NA')

                    Data_Out.loc[data_out_index]['Subject'+str(i+1)] = subject_name + ": " + "Term 4, " + term_grade + ", Exam, " + exam_grade +", Semester, " + semester_grade

                    # Output converted SUBJECT data for checking
                    converted_summary = Data_Out.loc[data_out_index,'Subject'+str(i+1)]
                    # To print output, uncomment line below
                    #print(converted_summary)
                    # Move to next subject within the same student's data in Data_In
                    if data_in_index + 3 > len(Data_In.index)-1:
                        break
                    else:
                        data_in_index = data_in_index + grade_types

            data_out_index += 1
            if data_in_index + grade_types > len(Data_In.index)-1:
                break

    #All data loop Finished
    print('New Data Frame Complete!')

    # Output resulting df 'Data_Out' to CSV
    # In future the path could be input by user or similar -
    # currently the filename is static.

    # NB : this works, so do not touch!

    Data_Out.to_csv('Output_'+Input_CSV_File, encoding='utf-8', index=False)


    #print(Data_Out.tail())
    print ('CSV has been output... time for a beer!')
    valid_data = False
