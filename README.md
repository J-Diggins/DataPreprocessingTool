# DataPreprocessingTool
A simple tool for bulk processing of .csv files

Feel free to make changes to the code where necessary. 

It was made using YouTube, StackOverflow and the documentation for different programs.

I am very much a novice programmer, so there will definitely be improvements that can be made!

Please make sure to keep my name on the program :)


Piloting note: This option currently does not work as intended. If you are using a version before 2025, it does not save the name as "pilot". Additionally if you change the name from "pilot" in a 2025 version, the program will be unable to exclude them.

# Requirements
Python 3
SciPy
TKinter

### Change Log

01/09/2025 - Moved the pilot select options into the select folder area, to force a choice before folder selection, to ensure pilot selection remains accurate

02/09/2025 - Removed redundant code. Created a helper function to streamline iterating over .csv files

24/09/2025 - Added a helper function and changed the filename saves, so that it does not save conditions files as floats when they should be integers.

16/12/2025 - Changed help instructions to better suit previous changes.

19/02/2026 - Updated save function

02/03/2026 - Updated so pilot data works with PsychoPy Studio - will check for a column named piloting, and then ask if you wish to exclude pilot data or not. If there is no column (for older datasets) it will ignore the question, as it will need to be manually filtered.

16/06/2026 - Added Main function to allow for better functionality testing.

26/06/2026 - Added shift_rows function. This allows for moving rows around in the excel sheet if they are misaligned.

### To Do
- Move to a better UI
- Further minor changes to code to improve efficiency
