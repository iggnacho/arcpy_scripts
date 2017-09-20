#Purpose: To disperse markers/points
#Use Case: Dispersing lots of overlapping points and keep their attributes
#I used to disperse points of individual people

import arcpy
# set work env
arcpy.env.workspace = r"C:\Users\Ignacio\Desktop\test.gdb"
arcpy.env.overwriteOutput = True

def writeGeometries(ptgeom, freq, address):
    #idList is for querying per address to get all unique record ids
    idList=[]
    freq1= freq-1
    #if more than one point we need to create disperse ring otherwise rest of script should not be ran when checking against magicangle line#23
    if freq1>=1:
        magicangle = 360/freq1
    else:
        magicangle = 0
    with arcpy.da.InsertCursor(feature1, ("SHAPE@","FREQ", "ADDRESS","MAGIC", "UOID")) as cursor:#cursor to insert into new feature class
        with arcpy.da.SearchCursor(featuremaster, ("MODERNST_3","Order_No_"), '"MODERNST_3"' + " = '" + address + "'" ) as cursorin:#search cursor to query and get all record no.
            for row in cursorin:
                idList.append(row[1])
        cursor.insertRow([ptgeom,freq,address,magicangle, idList[0]])#insert the main point on actual location based of data x,y
        if magicangle!=0:
            for number in range(0,freq-1):
                # print idList[number+1]
                ptgeomangle = ptgeom.pointFromAngleAndDistance (number*magicangle, distance, "PLANAR")
                cursor.insertRow([ptgeomangle,freq,address,number, idList[number+1]])


#START
#Enter summarized table name of modernst_3(geocoding field) with count and x, y
table1 = "Sum_Output_4"
#feature class name for the input which will be used for retrieved record numbers for each unique modern st
featuremaster = "Export_Output_10ft_new_bounds"
#use spatial reference from feature input class
spatialRef = arcpy.Describe(featuremaster).spatialReference
arcpy.CreateFeatureclass_management (r"C:\Users\Ignacio\Desktop\test.gdb","outputshape","POINT","","","",spatialRef)
feature1 = "outputshape"
arcpy.AddField_management(feature1, "FREQ", "SHORT")
arcpy.AddField_management(feature1, "ADDRESS", "TEXT")
arcpy.AddField_management(feature1, "MAGIC", "SHORT")
arcpy.AddField_management(feature1, "UOID", "SHORT")
distance = input("Please enter desired distance: ")

with arcpy.da.SearchCursor(table1, ["MODERNST_3","Cnt_MODERNST_3","Min_X","Min_Y"]) as cur:
  for row in cur:
      #calls writeGeometries function with SearchCursor parameters
      writeGeometries(arcpy.PointGeometry(arcpy.Point(row[2], row[3]), spatialRef), row[1], row[0])

print "finished"
