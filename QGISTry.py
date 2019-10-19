import sys
import os

from qgis.core import QgsApplication
import qgis.core as qt

# Initialize QGIS
qt.QgsApplication.setPrefixPath("C:\\OSGeo4W64\\apps\\qgis", True)
qgs = qt.QgsApplication([], False)
qgs.initQgis()

# Add the path to processing
sys.path.append('C:\OSGeo4W64\apps\qgis\python\plugins')

# Import processing
import processing


def create_map(shp_file, csv_f):

	assert os.path.exists(shp_file), "I could not locate the shape file. Was the path typed correctly?"
	s = open(shp_file, 'r+')
	print("Shape File Located")
	# Add Georgia Map to Canvas
	ga_map = qt.QgsVectorLayer(shp_file, "GA Map", "ogr")
	qt.QgsProject.instance().addMapLayer(ga_map)
	s.close()

	csv_uri = csv_f + "?encoding=UTF-8&delimiter=,"
	assert os.path.exists(csv_uri), "I could not locate the csv file. Was the path typed correctly?"
	c = open(csv_uri, 'r+')
	print("Csv File Located")
	csv_layer = qt.QgsVectorLayer(csv_uri, "2018_SH119", "delimitedtext")
	qt.QgsProject.instance().addMapLayer(csv_layer)
	c.close()

	# Join the layers that are a part of the Map Canvas
	join_field = 'County'
	target_field = 'PRECINCT_N'
	join_object = qt.QgsVectorLayerJoinInfo()
	join_object.setJoinLayer(csv_layer)
	join_object.joinLayerId = csv_layer.id()
	join_object.setJoinFieldName(join_field)
	join_object.setTargetFieldName(target_field)
	join_object.setUsingMemoryCache(True)
	ga_map.addJoin(join_object)

	# Color Map
	map_canvas = qt.QgsProject.instance().mapLayersByName("GA Map")[0]
	map_canvas.renderer().symbol().setColor(QColor("white"))
	map_canvas.triggerRepaint()
	print("Map Has Been Initialized")

	return map_canvas


shape_file = input("Enter the path to desired shape file: ")

csv_file = input("Enter the path to desired csv file: ")

# This is the initialized map
init_map = create_map(shape_file, csv_file)

print(init_map)
print("we're done here")

QGSApplication.exitQgis()















