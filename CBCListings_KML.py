
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


tsvfilepath = r"C:\projects\Dropbox\code\Python\CBC\inout\Listings06112015.csv"

KMLoutput = r"C:\projects\Dropbox\code\Python\CBC\inout\KMLoutput_listings.kml"

LatLonList = r"C:\projects\Dropbox\code\Python\CBC\inout\LatLonMissing.csv"


#get time and date of inputfile

input_time = os.stat(tsvfilepath)[8]  # index 8 contains timestamp of last modification in seconds from epoch
input_timestamp = time.strftime("%b %d, %Y at %H:%M", time.strptime(time.ctime(input_time)))


# column IDs
# Link the fields in the KMZ data table to the columns in the CSV spreadsheet
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


#Begin processing the input file

# create lists to store formatted KML placemark blocks for each available property, according to type

KML_indust = []
KML_retail = []
KML_office = []
KML_land   = []
KML_multif = []
KML_other  = []


# use the custom icons for property types

icon_indust = r"http://cbcslc.com/gis/KML/paddle/I_red.png"
icon_retail = r"http://cbcslc.com/gis/KML/paddle/R_red.png"
icon_office = r"http://cbcslc.com/gis/KML/paddle/O_red.png"
icon_land   = r"http://cbcslc.com/gis/KML/paddle/L_red.png"
icon_multif = r"http://cbcslc.com/gis/KML/paddle/M_red.png"
icon_other  = r"http://cbcslc.com/gis/KML/paddle/dot_red.png"


# open the input file

tsvfile = open(tsvfilepath, 'r')


# read the input file into a list of lines

tsvrecords = tsvfile.readlines()


# remove and save the first line of the input file (column headers)

fieldnames = tsvrecords.pop(0)


# open the text file to write the records with missing Lat Lon

latlon_out = open(LatLonList, 'w')
latlon_out.write(fieldnames)


# read the field values and write them to an XML placemark

for record in tsvrecords:
    
    # clean the input data
    
    # strip off the newline character at the end of the line and remove the superfluous '=' signs
    record = re.sub('[=\n]', '', record)
    
    # split the line into a list
    fields = record.split('","')
    
    #remove the quote character from the beginning of the first fields and the end of the last field
    fields[0] = fields[0][1:]
    fields[len(fields)-1] = fields[len(fields)-1][:-1]
    
    # check for lat/lon values. if not present, write the current record to a text file and skip to next record    
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
   
    
    icon_URL = ""
    placemark_list = []
    
    if fields[Avail_fields["PROPTYPE"]] == "Industrial":
        icon_URL = icon_indust
        placemark_list = KML_indust
    elif fields[Avail_fields["PROPTYPE"]] == "Retail":
        icon_URL = icon_retail
        placemark_list = KML_retail
    elif fields[Avail_fields["PROPTYPE"]] == "Office":
        icon_URL = icon_office
        placemark_list = KML_office
    elif fields[Avail_fields["PROPTYPE"]] == "Land":
        icon_URL = icon_land
        placemark_list = KML_land
    elif fields[Avail_fields["PROPTYPE"]] == "Multi-Family":
        icon_URL = icon_multif
        placemark_list = KML_multif
    else:
        icon_URL = icon_other
        placemark_list = KML_other
    
    placemark = '''
                <Placemark>
                    <name>%s</name>
                    <styleUrl>#pointStyleMap1</styleUrl>
                    <Style id="inline">
                        <IconStyle>
                            <color>ffffffff</color>
                            <colorMode>normal</colorMode>
                            <scale>1.50</scale>
                            <Icon>
                                <href>%s</href>
                            </Icon>
                        </IconStyle>
                        <LineStyle>
                            <color>ffffffff</color>
                            <colorMode>normal</colorMode>
                        </LineStyle>
                        <PolyStyle>
                            <color>ffffffff</color>
                            <colorMode>normal</colorMode>
                        </PolyStyle>
                    </Style>
                    <ExtendedData>
                        <SchemaData schemaUrl="#S_CBC_Listings">
                            <SimpleData name="PROPNAME">%s</SimpleData>
                            <SimpleData name="PROPTYPE">%s</SimpleData>
                            <SimpleData name="ADDRESS">%s</SimpleData>
                            <SimpleData name="CITY">%s</SimpleData>
                            <SimpleData name="STATE">%s</SimpleData>
                            <SimpleData name="ZIPCODE">%s</SimpleData>
                            <SimpleData name="AGENT1NAME">%s</SimpleData>                        
                        </SchemaData>
                    </ExtendedData>
                    <Point>
                        <coordinates>%s,%s,0</coordinates>
                    </Point>
                </Placemark>''' % (
                                   fields[Avail_fields["PROPNAME"]],
                                   icon_URL,
                                   fields[Avail_fields["PROPNAME"]],
                                   fields[Avail_fields["PROPTYPE"]],
                                   fields[Avail_fields["ADDRESS"]],
                                   fields[Avail_fields["CITY"]],
                                   fields[Avail_fields["STATE"]],
                                   fields[Avail_fields["ZIPCODE"]],
                                   fields[Avail_fields["AGENT1NAME"]],
                                   fields[Avail_fields["LON"]],
                                   fields[Avail_fields["LAT"]]
                                   )
    
    placemark_list.append(placemark) # save the placemark to the appropriate list (office, retail, industrial)
    

# close the input file and the missing lat/lon file

tsvfile.close()
latlon_out.close()


# Open the output file

KML = open(KMLoutput, 'w')


# write KML header, schema, and styles (this code never changes)

KMLheader = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">

<Document>

    <name>CBCListings.kml</name>
    
    <open>1</open>
    
    <description>CBC Listings\nUpdated %s\nExported %s</description>

    <LookAt>
        <longitude>-111.8</longitude>
        <latitude>40.5</latitude>
        <altitude>0</altitude>
        <heading>0</heading>
        <tilt>0</tilt>
        <range>500000</range>
    </LookAt>
    
    <Schema name="CBC_Listings" id="S_CBC_Listings">

        <SimpleField type="string" name="PROPNAME"><displayName><![CDATA[<b>Property Name</b>]]></displayName></SimpleField>
        <SimpleField type="string" name="PROPTYPE"><displayName><![CDATA[<b>Property Type</b>]]></displayName></SimpleField>
        <SimpleField type="string" name="ADDRESS"><displayName><![CDATA[<b>Address</b>]]></displayName></SimpleField>
        <SimpleField type="string" name="CITY"><displayName><![CDATA[<b>City</b>]]></displayName></SimpleField>
        <SimpleField type="string" name="STATE"><displayName><![CDATA[<b>State</b>]]></displayName></SimpleField>
        <SimpleField type="string" name="ZIPCODE"><displayName><![CDATA[<b>ZIP Code</b>]]></displayName></SimpleField>
        <SimpleField type="string" name="AGENT1NAME"><displayName><![CDATA[<b>Broker</b>]]></displayName></SimpleField>
        <SimpleField type="string" name="LAT"><displayName><![CDATA[<b>Latitude</b>]]></displayName></SimpleField>
        <SimpleField type="string" name="LON"><displayName><![CDATA[<b>Longitude</b>]]></displayName></SimpleField>
    </Schema>

    <Style id="normPointStyle1">
        <IconStyle>
            <scale>1.50</scale>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
            </Icon>
        </IconStyle>
        <BalloonStyle>
            <bgColor>aaaaaaaa</bgColor>
            <textColor>ff303030</textColor>
            <text><![CDATA[<table border="0" style="width:400px">
                                <tr><td colspan=2><font size="+2"><b>$[CBC_Listings/PROPNAME]</b></font></td></tr>
                                <tr><td><b>Property Type</b></td><td>$[CBC_Listings/PROPTYPE]</td></tr>
                                <tr><td><b>Address</b></td><td>$[CBC_Listings/ADDRESS]</td></tr>
                                <tr><td><b>City</b></td><td>$[CBC_Listings/CITY]</td></tr>
                                <tr><td><b>State</b></td><td>$[CBC_Listings/STATE]</td></tr>
                                <tr><td><b>ZIP Code</b></td><td>$[CBC_Listings/ZIPCODE]</td></tr>
                                <tr><td><b>Broker</b></td><td>$[CBC_Listings/AGENT1NAME]</td></tr>
                        </table>]]></text>
        </BalloonStyle>
    </Style>

    <Style id="hlightPointStyle1">
        <IconStyle>
            <scale>1.80</scale>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle_highlight.png</href>
            </Icon>
        </IconStyle>
        <BalloonStyle>
            <bgColor>aaaaaaaa</bgColor>
            <textColor>ff303030</textColor>
            <text><![CDATA[<table border="0" style="width:400px">
                                <tr><td colspan=2><font size="+2"><b>$[CBC_Listings/PROPNAME]</b></font></td></tr>
                                <tr><td><b>Property Type</b></td><td>$[CBC_Listings/PROPTYPE]</td></tr>
                                <tr><td><b>Address</b></td><td>$[CBC_Listings/ADDRESS]</td></tr>
                                <tr><td><b>City</b></td><td>$[CBC_Listings/CITY]</td></tr>
                                <tr><td><b>State</b></td><td>$[CBC_Listings/STATE]</td></tr>
                                <tr><td><b>ZIP Code</b></td><td>$[CBC_Listings/ZIPCODE]</td></tr>
                                <tr><td><b>Broker</b></td><td>$[CBC_Listings/AGENT1NAME]</td></tr>
                        </table>]]></text>
        </BalloonStyle>
    </Style>

    <StyleMap id="pointStyleMap1">
        <Pair>
            <key>normal</key>
            <styleUrl>#normPointStyle1</styleUrl>
        </Pair>
        <Pair>
            <key>highlight</key>
            <styleUrl>#hlightPointStyle1</styleUrl>
        </Pair>
    </StyleMap>

    <Folder id="layer 0">
        <name>Availables</name>
        <open>1</open>""" % (time.strftime("%b %d, %Y at %H:%M", time.localtime()), input_timestamp)

KML.write(KMLheader)


# write the KML folders containing the placemarks

#  industrial

Header_indust = """
        <Folder>
            <name>Industrial</name>"""

KML.write(Header_indust)

for placemark in KML_indust:
    KML.write(placemark)


#  office

Header_office = """
        </Folder>
        <Folder>
            <name>Office</name>"""

KML.write(Header_office)

for placemark in KML_office:
    KML.write(placemark)


#  retail

Header_retail = """
        </Folder>
        <Folder>
            <name>Retail</name>"""

KML.write(Header_retail)

for placemark in KML_retail:
    KML.write(placemark)


#  land

Header_land = """
        </Folder>
        <Folder>
            <name>Land</name>"""

KML.write(Header_land)

for placemark in KML_land:
    KML.write(placemark)


#  multi family

Header_multif = """
        </Folder>
        <Folder>
            <name>Multi-Family</name>"""

KML.write(Header_multif)

for placemark in KML_multif:
    KML.write(placemark)



# close the remaining tags

KML.write("""

        </Folder>

    </Folder>

</Document>
</kml>
""")


# close the output file

KML.close()

print("done")
#done
