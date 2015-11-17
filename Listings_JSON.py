# Justin Johnson
# Nov 2015

# CBC Advisors
# Available Listings: Convert REApps CSV data export to GeoJSON for use in web maps

import os
import os.path
import time
import re
import argparse

# get the inputs from the command line
# > python Listings_JSON.py -c (optional) [inputfile]

parser = argparse.ArgumentParser(description="Process an REApps CSV data export file to GeoJSON for use in web maps")
parser.add_argument("CSVfile", help="the exported CSV file from REApps" )

# add an optional command line argument '-c' to indicate if user wants to export only CBC listings
# CBC listings will have a different filename format to keep them separate from the JSON files for All listings

parser.add_argument('-c', action='store_const', const='CBC', help='process only Coldwell Banker Commercial listings (default is all firms)')

args = parser.parse_args()


# optional '-c' parameter will be checked to determine if only CBC listings will be processed for the frontdesk app
# example...
if args.c:
    # user selected the -c parameter
    print "CBC Option Selected"
else:
    # user did not include the -c parameter
    print "Processing ALL listings"

# get the input filename and the output directory from the command line arguments
csvfilepath = os.path.normpath(args.CSVfile)  # input file
outputpath = os.path.dirname(csvfilepath)  # output folder, same as input file location

# contains a list of records that are missing lat/lon values
missingLatLon = os.path.join(outputpath, "LatLonMissing.csv")

# open the comma-delimited CSV text file
# REApps export format:  Data Exchange CSV [Excel]

# get timestamp of input csv file
# Intended to be used to show the date of the data export in the map popup window or map title

input_time = os.stat(csvfilepath)[8]  # index 8 contains timestamp of last modification in seconds from epoch
input_timestamp = time.strftime("%b %d, %Y at %H:%M", time.strptime(time.ctime(input_time)))

print "Input File Timestamp: " + input_timestamp


# column IDs
# Map the fields in the REApps CSV spreadsheet to key/value pairs in a dictionary
# the "Index" number contains the column where the field name is stored in each record
# example: REApps_fields("BLDGSF") = 12
#          When a row from the CSV is converted to a list below, index 12 will contain the "Building SF" value

REApps_fields = {
    #Fieldname                 Index       REApps Field Title
    "EXPORTBY"                :  0,  #     "Export By"
    "CBCID"                   :  1,  #     "ID column"
    "PROPNAME"                :  2,  #     "Property Name" 
    "ADDRESS"                 :  3,  #     "Address"
    "CITY"                    :  4,  #     "City"
    "STATE"                   :  5,  #     "State/Province"
    "COUNTY"                  :  6,  #     "County"
    "ZIPCODE"                 :  7,  #     "Zip Code"
    "COMPLEX"                 :  8,  #     "Complex or Park Name"
    "CONSTRUCTIONSTAT"        :  9,  #     "Status"
    "PROPTYPE"                :  10, #     "Type"
    "BLDGCLASS"               :  11, #     "Class"
    "BLDGSF"                  :  12, #     "Building  SF"
    "LANDSIZE"                :  13, #     "Land Size (Acres)"
    "PARKRATIO"               :  14, #     "Parking Ratio"
    "YEARBUILT"               :  15, #     "Year Built"
    "ZONING"                  :  16, #     "Zoning"
    "PARCEL"                  :  17, #     "Parcel"
    "LAT"                     :  18, #     "Rooftop Latitude"
    "LON"                     :  19, #     "Rooftop Longitude"
    "LINKFLYER"               :  20, #     "Link to flyer"
    "LINKPHOTO"               :  21, #     "Link to photo"
    "AVAILTYPE"               :  22, #     "Available Type"
    "CAMCHARGES"              :  23, #     "CAM Charges"
    "OCCUPIED"                :  24, #     "Occupied"
    "BUILDTOSUIT"             :  25, #     "Build to Suit"
    "VACANTSF"                :  26, #     "Total Vacant SF"
    "SUBLEASESF"              :  27, #     "Total Sublease Vacant SF"
    "DIRVACSF"                :  28, #     "Total Direct Vacant SF"
    "INVESTMENT"              :  29, #     "Investment"
    "AVAILMINWAREHS"          :  30, #     "Available Min Warehouse SF"
    "AVAILMAXWAREHS"          :  31, #     "Available Max Warehouse SF"
    "TOTALOFFICESF"           :  32, #     "Total Available Office SF"
    "TOTALMEZZSF"             :  33, #     "Available Total Mezzanine SF"
    "CLEARANCEHT"             :  34, #     "Clearance Height"
    "SPRINKLERED"             :  35, #     "Sprinklered"
    "RAILACCESS"              :  36, #     "Rail Access"
    "CRANE"                   :  37, #     "Crane"
    "VOLTS"                   :  38, #     "Volts"
    "AMPS"                    :  39, #     "Amps"
    "PHASE"                   :  40, #     "Phase"
    "ALLDOCKHT"               :  41, #     "All Total Dock Height"
    "ALLGLDOORS"              :  42, #     "All Total GL Doors"
    "DOCKHIGH"                :  43, #     "Dock High"
    "GLDOORS"                 :  44, #     "GL Doors"
    "GLDOORHT"                :  45, #     "GL Door Height"
    "YARD"                    :  46, #     "Yard"
    "YARDSF"                  :  47, #     "Yard Size SF"
    "NUMFLOORS"               :  48, #     "Number of Floors"
    "ELEVATORS"               :  49, #     "Elevators"
    "FIBERAVAIL"              :  50, #     "Fiber Available"
    "LOADFACTOR"              :  51, #     "Load Factor"
    "PARKINGCOST"             :  52, #     "Other Parking Cost"
    "EXPENSESTOPS"            :  53, #     "Expense Stops"
    "PRIMARYUSE"              :  54, #     "Primary Use"
    "SECONDUSE"               :  55, #     "Secondary Use"
    "SEWER"                   :  56, #     "Sewer"
    "FREEWAYEXP"              :  57, #     "Freeway Exposure"
    "PHONE"                   :  58, #     "Phone"
    "FIBER"                   :  59, #     "Fiber"
    "GAS"                     :  60, #     "Gas"
    "WATER"                   :  61, #     "Water"
    "ELECTRICITY"             :  62, #     "Electricity"
    "RAIL"                    :  63, #     "Rail"
    "UNITS"                   :  64, #     "# Units"
    "CAPRATE"                 :  65, #     "Cap Rate"
    "NOI"                     :  66, #     "NOI"
    "VACRATE"                 :  67, #     "Vacancy Rate"
    "SUITE"                   :  68, #     "Suite"
    "FLOOR"                   :  69, #     "Floor"
    "TOTALAVSF"               :  70, #     "Total Available SF"
    "MINAVSF"                 :  71, #     "Min Available SF"
    "MAXAVSF"                 :  72, #     "Max Available SF"
    "MINYRLYRATE"             :  73, #     "Min Rate Yearly"
    "ASKRATETYPE"             :  74, #     "Rate Type" 
    "SALEPRICE"               :  75, #     "Sale Price"
    "LISTCOMPANY"             :  76, #     "List Company"
    "LISTCOPHONE"             :  77, #     "List Company Phone"
    "AGENT1NAME"              :  78, #     "Agent 1 Name"
    "AGENT1PHONE"             :  79, #     "Agent 1 Phone"
    "AGENT2NAME"              :  80, #     "Agent 2 Name"
    "AGENT2PHONE"             :  81, #     "Agent 2 Phone"
    "AGENT3NAME"              :  82, #     "Agent 3 Name"
    "AGENT3PHONE"             :  83, #     "Agent 3 Phone"
    "LASTUPDATE"              :  84, #     "Last Updated"
    "MARKETDATE"              :  85, #     "Date on Market"
    "COMMENTS"                :  86  #     "Comments"
}


# Create a list of fields to export for each JSON Element in the output GeoJSON file.
# Fields can be added or dropped from these lists, depending on need, without altering code any further.
# Use a different list of output fields, depending on whether the user wants to process All listings,
# or just the current set of CBC listings for the front desk map app.

if args.c:
    # if the user included the '-c' flag in the command line arguments, use a shortened list of fields.
    # this shortened list contains the fields that are of interest in the CBC Front Desk app.
    outputfields = [
        "PROPNAME",
        "PROPTYPE",
        "ADDRESS",
        "CITY",
        "STATE",
        "ZIPCODE",
        "LISTCOMPANY",
        "AGENT1NAME",
        "AGENT2NAME",
        "AGENT3NAME"
    ]
else:
    # include more listing information, for maps showing All available listings (default setting)
    outputfields = [
        "PROPNAME",
        "ADDRESS",
        "CITY",
        "STATE",
        "ZIPCODE",
        "PROPTYPE",
        "AVAILTYPE",
        "LISTCOMPANY",
        "AGENT1NAME",
        "AGENT2NAME",
        "AGENT3NAME",
        "AGENT1PHONE",
        "AGENT2PHONE",
        "AGENT3PHONE",
        "BLDGCLASS",
        "BLDGSF",
        "TOTALAVSF",
        "TOTALOFFICESF",
        "MINYRLYRATE",
        "ASKRATETYPE",
        "SALEPRICE",
        "LINKFLYER",
        "CLEARANCEHT",
        "PARKRATIO",
        "LASTUPDATE",
        "MARKETDATE"
    ]

# List of property types to export
# Each propbery type is exported as a separate JSON files in the output directory

proptypes = [
    "Hospitality",
    "Industrial",
    "Land",
    "Multi-Family",
    "Office",
    "Retail",
    "Manufactured Housing"
]

# create a dictionary of lists to store formatted GeoJSON
# one list for each unique property type

outputlists = {}

for proptype in proptypes:
    outputlists[proptype] = list()


def appendFieldsElement(fields, outputlists):
    """
    determine the correct output list for an input property type and append the formatted GeoJSON element to that list

    parameters:
        fields -- a list containing the CSV values from a table row split into separate elements
        outputlists -- a dictionary, each key is the name of a property tpye, each value is a list containing records
            formatted as GeoJSON elements

    returns:
        nothing. The Fields list is converted to GeoJSON and appended to the appropriate list in outputlists
    """
    
    # find the correct output list based on the PROPTYPE value
    outputlist = outputlists[fields[REApps_fields["PROPTYPE"]]]
    
    # write the header for the point feature, include LON and LAT (in that order)
    element = '''
      {  "type": "Feature",
         "geometry": {"type": "Point", "coordinates": [%s, %s]}''' % (fields[REApps_fields["LON"]], fields[REApps_fields["LAT"]])
    
    # if there are additional attributes to include for the point, write all of them here
    if len(outputfields) > 0:
        # add the formatted elements
        element += ''',\n         "properties": {'''
        
        proplist = [] # each record is a key:value pair
        
        # compile regular expression to search for non-numeric characters in phone numbers
        p = re.compile("[^0-9]")  # Matches any single character that is not numeric

        for fieldname in outputfields:
            # format the phone numbers here
            fieldval = fields[REApps_fields[fieldname]]

            phonefields = ["AGENT1PHONE", "AGENT2PHONE", "AGENT3PHONE"]

            if fieldname in phonefields:
                # strip the non-numeric characters from the phone number, then add dashes
                if fieldval != "":
                    # replace any non-numeric characters with empty strings to get only the digits
                    fieldval = p.sub("", fieldval)
                    # add the dashes at the appropriate locations for a phone number
                    fieldval = fieldval[0:3] + "-" + fieldval[3:6] + "-" + fieldval[6:]

            proplist.append('''\n            "%s": "%s"''' % (fieldname, fieldval))

        # "join" the list of strings into a comma-delimited string of values
        element = element + ",".join(proplist)
        
        # close the element
        element += "\n          }\n      }"
        
    else:
        element += "\n      }"  # close out the element without adding any additional properties
    
    # append the GeoJSON element to the appropriate output list (Office, Retail, Industrial, etc.)
    outputlist.append(element) 


def getREAppsFields(record):
    """
    Clean the line of records from the CSV. Return a list of cleaned split fields.

    parameters:
        record -- a string containing a row from the input CSV text file

    returns:
        a list containing containing the values from the CSV row.  Fields correspond to the key/value pairs
        in the REApps_fields dictionary.
    """
    
    # output from REApps contains unwanted characters
        
    # strip off the newline character at the end of the line and remove any superfluous '=' signs
    record = re.sub('[=\n]', '', record)

    # remove the double-quote character from the beginning and end of the string
    # quotes are the result of the readline() method, apparently.
    record = record[1:-1]
    
    # split the line of comma-delimited values into a list
    fields = record.split('","')
    
    # check for lat/lon values and check if the property type matches one of the types in the output list
    # if not, write the current record to a CSV file and return value of None
    if (fields[REApps_fields["LAT"]] == "" or fields[REApps_fields["LON"]] == "" or not (fields[REApps_fields["PROPTYPE"] in proptypes])):
        latlon_out.write(record)
        print "Bad Record Found: " + record
        return None
    
    # clean the field values
    # REApps seems to export dates improperly, with an '=' in front, which also screws up the quotation marks
    # example:  '="6/16/2014"'
    
    # remove the beginning and ending quotation marks that sometimes get added to field values
    # replace the ampersand character (&) with the HTML character sequence ($amp;)
    # replace any internal double-quote characters (") with single-quotes, to avoid screwing up the double-quoted JSON values
    
    for i in range(len(fields)):
        fields[i] = fields[i].strip('"')
        if fields[i].find("&") > 0:
            fields[i] = fields[i].replace("&", "&amp;")
        if fields[i].find('"') > 0:
            fields[i] = fields[i].replace('"', "'")
    
    return fields

# Begin processing the input file

# compile a regular expression to search for values beginning with any form of "CBC"
cbcregex = re.compile(r'^[Cc][Bb][Cc]')

# open the input file
csvfile = open(csvfilepath, 'r')

# read the input file into a list of lines
csvrecords = csvfile.readlines()

# remove and save the first line of the input file (column headers)
fieldnames = csvrecords.pop(0)

# open the text file to write the records with missing Lat Lon
latlon_out = open(missingLatLon, 'w')
latlon_out.write(fieldnames)

# read the records
# check if the user requested only the subset of CBC listings
# write them to GeoJSON features
for record in csvrecords:
    
    # clean the line of text from the CSV and split it into a list of fields
    fields = getREAppsFields(record)
    
    # if the record is missing lat/lon values or a property type, a value of None is returned from getREAppsFields()
    
    if fields:
        if args.c and cbcregex.match(fields[REApps_fields["LISTCOMPANY"]]):
            # user selected the CBC command-line flag, and the listing company begins with "CBC"
            # write the record to the appropriate output list
            appendFieldsElement(fields, outputlists)
        elif not args.c:
            # user did not select the CBC flag
            # write All records to the appropriate list
            appendFieldsElement(fields, outputlists)
    else:
        # write the line with missing data to the error output file
        latlon_out.write(record)

# close the input file and the missing lat/lon file

csvfile.close()
latlon_out.close()

# Loop through the lists of JSON elements created using appendFieldsElement()
# write each separate JSON file in the output directory
# name the output files according to whether the CBC flag was selected, or All listings were processed

for outputname in outputlists:
    # Open the output file
    if args.c:
        JSON = open(outputpath + "//CBC_Listings_" + outputname + ".json", "w")
    else:
        JSON = open(outputpath + "//ALL_Listings_" + outputname + ".json", "w")

    # write JSON header
    JSON.write("""{ "type": "FeatureCollection",
    "features": [""")

    # write the JSON elements from the list
    JSON.write(",".join(outputlists[outputname]))

    # close the header
    JSON.write("""\n    ]\n}""")
    
    # close the output file
    JSON.close()


# Write all of the output into a single JSON file, for possible use in Google Maps apps
if args.c:
    JSON = open(outputpath + "//CBC_Listings_ALL.json", "w" )
else:
    JSON = open(outputpath + "//ALL_Listings_ALL.json", "w" )

# write JSON header
JSON.write("""{ "type": "FeatureCollection",
"features": [""")

allsites = []

for outputname in outputlists:
    # merge all of the lists into a single list
    allsites.extend(outputlists[outputname])
        
# write the JSON elements from the list
JSON.write(",".join(allsites))

# close the header
JSON.write("""\n    ]\n}""")
    
# close the output file
JSON.close()
  
print("done")
