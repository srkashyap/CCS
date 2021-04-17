input : enrollment file with days seperated. 1day= 1 row
output : times where no classes are going on for each student.


Blocks:
1. Read input
2. Preprocessing: converting required columns to integer type, and selecting required columns
3. Creating tuples of class times
4. Creating a dictionary containing free intervals between times
5. Converting the dictionary to desired form and saving as excel

Class time dictionary format:
{studentID:
    (
    day1:(xx:yy AM/PM , xx:yy AM/PM),
    day2:(xx:yy AM/PM , xx:yy AM/PM),
    .
    .
    
    )
}

Free interval times:
1. Set start time of day. 
2. start iterating for one day for one student. 
   a. select end time of first class after 9:00AM and start time of next immediate class. save the pair as a tuple
   b. list of tuples is added to the dictionary
3. convert the dictionary to dataframe and save