import sys, os, glob
import markdown2
import json

def main():
	input_folder_path = sys.argv[1]
	ouput_folder_path = sys.argv[2]
	jsons = get_json(input_folder_path)
	for json_f in jsons:
		print("Handling {}".format(json_f))
		data = read_file(json_f)
		if "index.json" in json_f:
			handle_index_json(data, input_folder_path, ouput_folder_path)
		else:
			handle_json(data, input_folder_path, ouput_folder_path)

def read_file(filename):
	with open(filename, "r") as file:
		data = file.read()
	return data

def handle_index_json(index_json_data, folder_path, output_path):
	jdict = json.loads(index_json_data)
	element_f = None
	index_f = None
	for key, value in jdict.iteritems():
		if key == "element_template":
			element_f = value
		if key == "index_template":
			index_f = value

	element_d = read_file(folder_path + "/" + element_f)
	index_d = read_file(folder_path + "/" + index_f)

	jsons = get_json(folder_path)
	for json_f in jsons:
		if "index.json" in json_f:
			continue
		print("Indexing {}".format(json_f))
		json_data = read_file(json_f)
		json_art = json.loads(json_data)

		element_copy = element_d

		for key, value in json_art.iteritems():
			if key != "md" and key != "template":
				element_copy = template(element_copy, key, value)

		index_d = template(index_d, "elements", element_copy + "\n\n" + r"{{elements}}")

	index_d = template(index_d, "elements", "")

	for key, value in jdict.iteritems():
		if key != "md" and key != "template":
			index_d = template(index_d, key, value)

	with open(output_path + "/index.html", "w") as file:
		file.write(index_d)
		

def handle_json(json_data, folder_path, ouput_folder_path):
	jdict = json.loads(json_data)
	markdown_f = None
	template_f = None
	url_str = None
	for key, value in jdict.iteritems():
		if key == "md":
			markdown_f = value
		if key == "template":
			template_f = value
		if key == "url":
			url_str = value

	md_d = read_file(folder_path + "/" + markdown_f)
	temp_d = read_file(folder_path + "/" + template_f)

	temp_d = template(temp_d, "content", markdown2.markdown(md_d, extras=["fenced-code-blocks"]))

	for key, value in jdict.iteritems():
		# print((key, value))
		if key != "md" and key != "template":
			temp_d = template(temp_d, key, value)

	# save temp_d as url_str
	with open(ouput_folder_path + "/" + url_str, "w") as file:
		file.write(temp_d)



def template(template, id, content):
	return template.replace(r"{{" + id + r"}}", content)

def get_json(folder_path):
	return glob.glob(folder_path + "/" + "*.json")


if __name__ == '__main__':
	main()