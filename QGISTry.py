import sys

import qgis.core as qt

# Initialize QGIS
qt.QgsApplication.setPrefixPath(r'C:\OSGeo4W64\apps\qgis', True)
qt.QgsApplication.initQgis()

# Add the path to processing so we can import it next
sys.path.append(r'C:\OSGeo4W64\apps\qgis\python\plugins')
# Code rest of this for the use of "Processing Algorithms in QGIS"


shape_file = input("Enter the path to desired shape file: ")
csv_file = input("Enter the path to desired csv file: ")


def create_map(shp_file, csv_f):

	# Add Georgia Map to Canvas
	ga_map = qt.QgsVectorLayer(shp_file, "GA Map", "ogr")
	qt.QgsProject.instance().addMapLayer(ga_map)
	csv_uri = csv_f + "?encoding=UTF-8&delimiter=,"
	csv_layer = qt.QgsVectorLayer(csv_uri, "2018_SH119", "delimitedtext")

	# Add data from csv file to Map Canvas if csv is valid
	if not csv_layer.isValid():
		print("CSV Layer not valid")
	else:
		qt.QgsProject.instance().addMapLayer(csv_layer)

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
	map_canvas.renderer().symbol().setColor(qt.QColor("white"))
	map_canvas.triggerRepaint()
	print("Map Has Been Initialized")

	return map_canvas

# This is the initialized map
ga_map = create_map(shape_file, csv_file)
















