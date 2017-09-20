#Purpose: To find what points geocoded where placed outside their attribute designated geographies
#Use Case: Checking geocoding accuracy
#I used to see accuracy of the results in a historical geocoding effort
#First use script for "Split By Attributes (Analysis)" for both unique points and geographies
#then ammend the paths  and double check the parameters are set properly in the function calls down below

import arcpy, os
arcpy.env.overwriteOutput = True

#paths
pointF = ""#"C:/Users/Ignacio/Desktop/finaloutside/prec" -> geocoded points split by unique values in attribute table-> folder with the geographies split into individual geometries based on unique value
geographyF ="" #"C:/Users/Ignacio/Desktop/finaloutside/geographies" -> folder with the geographies split into individual geometries based on unique value
mainP = ""#"C:/Users/Ignacio/Desktop/finaloutside/Export.shp" -> a shapefile with the entire point dataset
field = "" #"Precinct" -> field which both geographies and points have in common, in the example the geographies are split by precinct unique values and the points are being split by the same attribute, this means that we are checking that the points geocoded are falling within the geographic bounds of what the tabular data specifies

#auto get all unique values from field into var myValues | in my case getting all unique precinct values
with arcpy.da.SearchCursor(mainP, field) as cursor:
    myValues = sorted({row[0] for row in cursor})
#loop through all the values in designated fields and create selections by locations and then invert to get outside points.
for value in myValues:
    #make feature layer management for each unique valued points layer
    arcpy.MakeFeatureLayer_management(pointF+"/"+str(value)+".shp", "geog")
    #see what from the point layer intersects the unique valued geography layer with a 150 ft search distance and then invert selection so we are only gettin what is outside
    arcpy.SelectLayerByLocation_management ("geog", "intersect", geographyF+"/"+str(value)+".shp","150 feet", "", "INVERT" )
    #ssave each iteration of the analysis into a selected folder (FOLDER PATH needs to be changed to your own results folder)
    arcpy.FeatureClassToFeatureClass_conversion("geog", "C:/Users/Ignacio/Desktop/finaloutside/results", str(value)+"_outside")
print "Finished"
