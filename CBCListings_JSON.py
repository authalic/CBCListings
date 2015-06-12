
# Justin Johnson
# June 2015

# CBC Advisors
# Available Listings: REApps to GIS Processing
# Convert a report to a GIS format


import os
import time
import re
# import sys  # for command line arguments

# get the inputs from the command line
# >python CBCListings.py [inputfile_type] [inputfile_path]

#inputfile_type = sys.argv[1]
#inputfile_path = sys.argv[2]


# open the comma-delimited text file
# report should be in a plain-text format, with quoted comma delimiters between fields (",")
# REApps export format:  Data Exchange CSV [Excel]


csvfilepath = r"C:\projects\Dropbox\code\Python\CBC\inout\Listings06112015.csv"

JSONoutputpath = r"C:\projects\Dropbox\code\Python\CBC\inout\CBC_listings"

LatLonList = r"C:\projects\Dropbox\code\Python\CBC\inout\LatLonMissing.csv"

outputJSON = {}


#get time and date of inputfile

input_time = os.stat(csvfilepath)[8]  # index 8 contains timestamp of last modification in seconds from epoch
input_timestamp = time.strftime("%b %d, %Y at %H:%M", time.strptime(time.ctime(input_time)))


# column IDs
# Link the fields in the output data to the columns in the CSV spreadsheet
# first field in an imported row is at position 0

# Availables file data fields:

Avail_fields = {
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

# List of fields to export for each element in the output GeoJSON file

outputfields = ["PROPNAME", "PROPTYPE", "ADDRESS", "CITY", "STATE", "ZIPCODE", "AGENT1NAME"]

proptypes = ["indust", "retail", "office", "land", "multif", "other"]


# create lists to store formatted GeoJSON elements, according to type

outputlists = {}

for proptype in proptypes:
    outputlists[proptype] = list()

def appendField(fields, outputlists):
    "function determines the correct output list for a given property type and appends the formatted element"
    
    outputlist = outputlists[fields[Avail_fields["PROPTYPE"]]]
    
    element = '''
      { "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [%S, %S]}''' % (fields[Avail_fields["LON"]], fields[Avail_fields["LAT"]])
    
    if len(outputfields) > 0:
        pass
        # add the formatted elements
    else:
        element = element + "/n      }"  # close out the element without adding any elements


values = (
                                   fields[Avail_fields["PROPNAME"]],
                                   fields[Avail_fields["PROPTYPE"]],
                                   fields[Avail_fields["ADDRESS"]],
                                   fields[Avail_fields["CITY"]],
                                   fields[Avail_fields["STATE"]],
                                   fields[Avail_fields["ZIPCODE"]],
                                   fields[Avail_fields["AGENT1NAME"]],
                                   
                                   )
    # create the GeoJSON element




    
    element_list.append(element) # save the element to the appropriate output file (office, retail, industrial)
    


#Begin processing the input file

# open the input file

csvfile = open(csvfilepath, 'r')


# read the input file into a list of lines

csvrecords = csvfile.readlines()


# remove and save the first line of the input file (column headers)

fieldnames = csvrecords.pop(0)


# open the text file to write the records with missing Lat Lon

latlon_out = open(LatLonList, 'w')
latlon_out.write(fieldnames)


# read the records and write them to GeoJSON features

for record in csvrecords:
    
    # clean the input data
    
    # strip off the newline character at the end of the line and remove any superfluous '=' signs
    record = re.sub('[=\n]', '', record)
    
    # split the line into a list
    fields = record.split('","')
    
    #remove the quote character from the beginning of the first fields and the end of the last field
    fields[0] = fields[0][1:]
    fields[len(fields)-1] = fields[len(fields)-1][:-1]
    
    # check for lat/lon values. if not present, write the current record to a CSV file and skip to next record    
    if (fields[Avail_fields["LAT"]] == "" or fields[Avail_fields["LON"]] == "" ):
        latlon_out.write(record + '\n')
        continue
        
    # clean the field values
    # REApps seems to export dates improperly, with an '=' in front, which also screws up the quotation marks
    # example:  '="6/16/2014"'
    
    # remove the quotation marks that sometimes get added to field values
    
    for i in range(len(fields)):
        fields[i] = fields[i].strip('"')
    
    # replace the ampersand character (&) with the HTML character sequence ($amp;)
    
    for i in range(len(fields)):
        if fields[i].find("&") > 0:
            fields[i] = fields[i].replace("&", "&amp;")
    
    # write the record to the appropriate output list
    appendField(fields, outputlists)
    
    
# close the input file and the missing lat/lon file

csvfile.close()
latlon_out.close()


# Open the output file

JSON = open(JSONoutput, 'w')


# write JSON header, schema, and styles (this code never changes)

JSONheader = """{ "type": "FeatureCollection",
    "features": [
"""

JSON.write(JSONheader)


# write separate JSON files for each industry type

#  industrial

Header_indust = """
        <Folder>
            <name>Industrial</name>"""

JSON.write(Header_indust)

for element in JSON_indust:
    JSON.write(element)


#  office

Header_office = """
        </Folder>
        <Folder>
            <name>Office</name>"""

JSON.write(Header_office)

for element in JSON_office:
    JSON.write(element)


#  retail

Header_retail = """
        </Folder>
        <Folder>
            <name>Retail</name>"""

JSON.write(Header_retail)

for element in JSON_retail:
    JSON.write(element)


#  land

Header_land = """
        </Folder>
        <Folder>
            <name>Land</name>"""

JSON.write(Header_land)

for element in JSON_land:
    JSON.write(element)


#  multi family

Header_multif = """
        </Folder>
        <Folder>
            <name>Multi-Family</name>"""

JSON.write(Header_multif)

for element in JSON_multif:
    JSON.write(element)



# close the remaining tags

JSON.write("""
    ]
}
""")


# close the output file

JSON.close()

print("done")
#done







