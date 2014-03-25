Glider Data Conversion
===========

Simple Repository for Ocean Glider Data Conversion to NetCDF Format.  

#Guide for Converting Glider Data Using the SPT Toolbox

## Introduction
This guide has been created to document the steps taken to convert Glider data from native Glider format to NetCDF format.  The process relies heavily on the work done by John Kerfoot of Rutgers University.  Work performed was on behalf of the Great Lakes Observing System (GLOS).  

##Background Information
The Glider reports two types of data (Flight Control and Scientific), in two different formats (Full Resolution and Reduced Resolution).  The file extension is used to differentiate between these 4 distinct datasets.  The table below explains what the file extensions mean.

|                    | Flight Control | Scientific |
| ------------------ |:--------------:| :---------:|
| Full Resolution    |      .dbd      |     .ebd   |
| Reduced Resolution |      .sbd      |     .tbd   |

To be able to convert the data properly, the operator MUST have resolution-paired flight control and scientific data (i.e. .dbd and .ebd OR .sbd and .tbd).  

## Required Software and Files
1. MATLAB
2. ToolsUI
3. CSIRO Matlab EOS-80 Seawater Library (http://www.cmar.csiro.au/datacentre/ext_docs/seawater.htm)
4. Slocum Power Tools Toolbox for MATLAB (http://www.github.com/kerfoot/spt)
5. TWRC Glider Data Utlities (http://marine.rutgers.edu/~kerfoot/slocum/data/readme/wrc_exe/)
6. processDbds.sh
7. standard_sensors.txt
8. convert.py

##Guide
### Caveat Emptor
Ideally, the entire conversion process would occur in Linux (as John Kerfoot's examples show).  However, MATLAB was only available in Windows.  In an attempt to compartmentalize this issue all work not performed in MATLAB was done using Linux.  This required large data transfers between multiple computers and virtual machines.  It would be benficial to avoid this in the future by using a Linux version of MATLAB.
All MATLAB commands are the same between Windows and Linux.

### Pre MATLAB Process
The first step in converting the data is obtaining it.  The data used for the first conversion was located on the tds.glos.us server in the /data/thredds/glider directory.  Once obtained, the data should be briefly reviewed to ensure that it is resolution-paired flight control and scientific data.  If it is not, the proper data must be obtained.

NOTE: There is an simpler alternative method that can be used, but first the standard method should be understood.  

Once the data is verified as corrrectly paired formats, it must be converted from the binary glider data files to ascii.  To do this, the TWRC Glider Data Utility 'dbd2asc' should be used.  The utility requires you to send the standard output to a file, or combine the ascii conversion step in with the sensor filter step.

The sensor filter step is necessary because the glider reports a large amount of data that is unrelated to scientific study.  This superfluous data causes the datasets to become much larger than needed, which in turns increases the processing time.

To fitler the data, the dbd2asc output should be piped to the TWRC utility 'dba_sensor_filter' with a list of sensors desired.  In general, the sensors in standard_sensors.txt can be used during this step.  The combined commands should look like the example below (uses full resolution data):

```linux
cd /dir/with/utltities/and/glider/data
./dba2asc FILENAME.dbd | ./dba_sensor_filter -f standard_sensors.txt > FILENAME.dba.asc
./dba2asc FILENAME.ebd | ./dba_sensor_filter -f standard_sensors.txt > FILENAME.eba.asc
```

NOTE: the .dbd and .ebd file extensions were changed to .dba and .eba to dentoe they are in ascii form.


Once the data has been converted to ascii and filtered by desired sensors the two outputs should be merged into one file for MATLAB processing.  The 'dba_merge' TWRC utility is used for this.  An example is shown below.  

```linux
./dba_merge FILENAME.dba.asc FILENAME.eba.asc > FILENAME.dbd.dat
```

This merged file is now ready to be processed in MATLAB.  

####Alternative Method
The alternative method utilizes John Kerfoot's processDbds.sh script and a cusomt built convert.py utility.  The processDbds.sh script must be slightly modified for every use, but this modification is minimal.  
1. On line  35, the existing location that the file header files should be written to.  
2. On line 38 the location of the TWRC executables should be specified.  In many cases this will be where the data is.  

Also, the convert.py should have the location of the data defined on line 7.

Next, the convert.py script should run to call the processDbds.sh routine for each data pair.  

The conversion and merging of large datasets may take a long period of time.

###MATLAB Setup
To properly setup MATLAB for the glider conversion a directory must be created to store the SPT toolbox and CSIRO Matlab EOS-80 Seawater Library.  Ideally, the data to be converted will be located there as well.  Move the previously mentioned files to the newly created folder and open MATLAB.  Navigate to the 'Current Folder' pane (should be open on the left side by default).  Use this pane to navigate to the newly created folder.  Right-Click the folder, go to 'Add to Path', and select 'Selected Folders and Subfolders'.  Check that this worked by typing 'Dbd()' into the command window.  If this command is unrecognized, refer to John Kerfoot's wiki for help.

###MATLAB Process
Once the data is converted and merged it should be loaded into MATLAB by using the 'listDbds' command, like so:  

```
dbds = listDbds('dir','FOLDER-HOLDING-MERGED-FILES', 'ext', 'dat');
```

Once the files are loaded, they should be moved into one Dbd Group using the 'DbdGroup' command, like so:

```
dbgroup = DbdGroup(dbds(1:end));
```

Next, we must add and modify some information, like so:

```
addCtdSensors(dbgroup);
dbgroup.timestampSensors = 'drv_sci_m_present_tiem_datenum';
dbgroup.depthSensors = 'drv_sci_water_pressure';
for i = 1:length(dbgroup.dbds)
    dbgroup.dbds(1,i).fillTimes = 'linear';
    dbgroup.dbds(1,i).fillDepths = 'linear';
    dbgroup.dbds(1,i).fillGps = 'linear';
end
```

Now that the DbdGroup has been succesfully created and modified, it is time to create the NetCDF files.  To do so the 'DbdGroup2TrajectoryNc' command is used, like so:

```
DbdGroup2TrajectoryNc(dbgroup)
'''

    



