from os.path import join, dirname, abspath
from re import sub, search

# regex
regex1 = r'<[^<>]*>'  # selects all <> tags
regex2 = r'&amp;'
regex3 = r'[A-Z]{3} [0-9]{4}.*(?= -)' # selects course ids "CSD 1101" or "CSD 4902A"
regex4 = r'Status|Units|Grading|Deadlines|Class Nbr|Section|Component|Days and Times|Room|Instructor|Start/End Date'
regex5 = r'Graded|(Pass / Fail)' # get graded status
regex6 = r'ALL|[LPW][0-9]' # get section
#regex7 = r'[MTWFS][ouehra] [0-2][0-9]:[0-5][0-9] - [0-2][0-9]:[0-5][0-9]' # get time (specifically 24h time only)
regex8 = r'[MTWFS][ouehra] [0-2]?[0-9]:[0-5][0-9](AM|PM)? - [0-2]?[0-9]:[0-5][0-9](AM|PM)?' # get time





# source
sourcepath = join(dirname(abspath(__file__)),'source.txt')
with open(sourcepath) as f:
  sourcefile = f.readlines()


# cleanup
cleanfile = []
ignore = True
for line in sourcefile:
  # regex
  line = sub(regex1, '', line)
  line = sub(regex2, 'and', line)

  # spellcheck
  line = line.replace('Integrated Work Study Programm', 'Integrated Work Study Programme')

  # ignore top lines until "Select Display Option"
  if line == 'Select Display Option\n':
    ignore = False

  # ignore bottom lines after "Printer Friendly Page"
  if line == 'Printer Friendly Page\n':
    ignore = True
  
  # skip ahead
  if ignore:
    continue

  # clean lines
  if line != '\n' and line != '&nbsp;\n':
    # append
    cleanfile.append(line)

# surgical post-cleanup cleaning
datareadyfile = cleanfile[2:]
for i in range(1,6):
  del cleanfile[1]


# splits all the courses into their own array
# pre-extracts course info
courses = ['ignore']
datareadyfiles = []
datareadyfile = []
for line in cleanfile:
  # match course id
  courseid = search(regex3, line)

  # catch every line in outputfile until the next time courseid matches
  # this splits all the courses into their own array
  if courseid is not None:
    courses.append(courseid.string.rstrip())
    datareadyfiles.append(datareadyfile)
    datareadyfile = []
    #outputfile.append(line)
    continue
  
  datareadyfile.append(line)

datareadyfiles.append(datareadyfile)

# course header/label cleanup
for index, file in enumerate(datareadyfiles):
  for index, line in enumerate(file):
    # clean up headers
    search4 = search(regex4, line)
    if search4 is not None:
      file[index] = ''



# data init for extraction
csvlines = []
csvline = []

name_of_course = ''
component = ''
course_info = ''
grading = ''
section = ''
instructor = ''
start_date = ''
start_time = ''
end_date = ''
end_time = ''
location = ''

# csv construction
def ConstructCSVLine():
  # build subject
  subject = f'{name_of_course} ({component})'

  # build description
  description = f'<u><b>{course_info}</b></u><br>{grading} - {section} - {instructor}'
  #<u><b>CSD 1101 - Computer Environment</b></u><br>Graded - <span>ALL - </span><span>VADIM SUROV</span>

  # fill in the rest (All Day Event / Private)
  all_day_event = False
  private = True

  # build csv line
  #return ','.join(subject, start_date, start_time, end_date, end_time, all_day_event, description, location, private)
  return f'{subject},{start_date},{start_time},{end_date},{end_time},{all_day_event},{description},{location},{private}\n'



# data extraction
for index, file in enumerate(datareadyfiles):
  # ignore first file
  if index == 0: continue

  # ignore dropped classes
  if 'Dropped\n' in file: continue

  # get course info
  course_info = courses[index]
  ## get name of course
  name_of_course = course_info.split(' - ')[1]

  # start looking through
  for index, line in enumerate(file):
    # get grading (one per file)
    search5 = search(regex5, line)
    if search5 is not None:
      grading = line.rstrip()
    
    if grading == '': continue
    
    # get section (start component block)
    # get component
    search6 = search(regex6, line)
    if search6 is not None:
      section = line.rstrip()
      component = file[index+1].rstrip()
    
    if section == '': continue

    # get time (start class block)
    #search7 = search(regex7, line)
    search8 = search(regex8, line)
    if search8 is not None:
      # get time
      if 'AM' or 'PM' in search8: # 12h clock
        time = line.rstrip()
        # split
        splittime = time.split(' ')
        del splittime[2]
        del splittime[0]
        # convert to 24h
        for i, time in enumerate(splittime):
          if 'PM' in time:
            hour_minute = time.split(':')
            newtime = str(int(hour_minute[0]) + 12) + ':' + hour_minute[1][:2]
          else:
            newtime = time.replace('AM', '')
            if len(newtime) == 4: # turn 9:00 to 09:00
              newtime = '0' + newtime
          splittime[i] = newtime

        start_time = splittime[0]
        end_time = splittime[1]
      else: # 24h clock
        time = line.rstrip()
        # split
        start_time = time[3:8]
        end_time = time[-5:]

      # get room
      location = file[index+1].rstrip()
      # get instructor
      if ',' in file[index+2]: # for the stupid case where there's TWO lecturers for one class
        getfile = file[index+2].rstrip() + ' ' + file[index+3]
        twoinstructors = True
      else: # expected outcome
        getfile = file[index+2]
        twoinstructors = False
      instructor = getfile.rstrip().replace(' .','')

      # get date
      if twoinstructors:
        date = file[index+4].rstrip().split(' - ')
      else:
        date = file[index+3].rstrip().split(' - ')
      # split
      start_date = date[0]
      end_date = date[1]

      # for each class block, write a csvline with data from above
      csvline = ConstructCSVLine()
      csvlines.append(csvline)



# write to output
# init with header
outputfile = ['Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description,Location,Private\n']
for csvline in csvlines:
  for line in csvline:
    outputfile.append(line)


# write to csv
outputpath = join(dirname(abspath(__file__)),'output.csv')
with open(outputpath, "w") as f:
  f.writelines(outputfile)