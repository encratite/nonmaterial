import re
import sys
import xml.etree.ElementTree as ET

from component import Component

def print_bom(xml_path):
	tree = ET.parse(xml_path)
	root = tree.getroot()
	components = []
	for component in root.findall(".//comp"):
		reference = component.attrib["ref"]
		match = re.match("^(.+?)(\\d+)$", reference)
		reference = match.group(1)
		index = int(match.group(2))
		componentValue = component.find("./value").text
		fields = []
		for field in component.findall("./fields/field"):
			field_name = field.attrib["name"]
			field_value = field.text
			fields.append((field_name, field_value))
		component = Component(reference, index, componentValue, fields)
		components.append(component)

	components.sort(key = Component.getKey)
	for component in components:
		parts = [component.reference + str(component.index)]
		if len(component.value) > 0:
			parts.append(component.value)
		for field_name, field_value in component.fields:
			parts.append(field_value)
		print(", ".join(parts))


if len(sys.argv) != 2:
	print("Usage:")
	print("<KiCad XML input>")
	exit(1)

xml_path = sys.argv[1]
print_bom(xml_path)
