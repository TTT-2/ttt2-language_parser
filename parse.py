import argparse, os, re

parser = argparse.ArgumentParser("parse language files")
parser.add_argument("--in", help="A path to the input folder", type=str, dest="input")
parser.add_argument("--out", help="A path to the output folder", type=str, dest="output")
parser.add_argument("--base", help="The name of the base language", type=str)
args = parser.parse_args()

lang_file_list = os.listdir(args.input)
base_file = args.base + ".lua"
base_file_path = args.input + "/" + base_file

if not base_file in lang_file_list:
	print("Basefile not found. Ending")
	exit()

# Define regular expressions to match different components
comment_pattern = r'--\s(.+)'
lang_pattern = r'local L = LANG\.CreateLanguage\("([^"]+)"\)'
identifier_pattern = r'L\.([a-zA-Z_][a-zA-Z_0-9]*)\s=\s'
singleline_text_pattern = r'L\.([a-zA-Z_][a-zA-Z_0-9]*)\s=\s"([^"]*)"'
multiline_text_pattern_open = r'L\.([a-zA-Z_][a-zA-Z_0-9]*)\s=\s\[\[(.*?)'
multiline_text_pattern_close = r'(.*?)\]\]'

# Create a list to store the data
data = []

# Open and read the file
with open(base_file_path, "r") as file:
	lines = file.readlines()

line_counter = 0
is_multiline = False

# Iterate through the lines
for i, line in enumerate(lines):
	line = line.strip()

	# Check for comments
	lang_match = re.match(lang_pattern, line)
	if lang_match:
		data.append({
			"type" : "code",
			"content" : lang_match.group(0)
		})

		line_counter += 1

		continue

	# Check for comments
	comment_match = re.match(comment_pattern, line)
	if comment_match:
		data.append({
			"type" : "comment",
			"content" : comment_match.group(1)
		})

		line_counter += 1

		continue

	singleline_text_match = re.search(singleline_text_pattern, line)
	if singleline_text_match:
		data.append({
			"type" : "single",
			"identifier": singleline_text_match.group(1),
			"content" : singleline_text_match.group(2)
		})

		line_counter += 1

		continue

	multiline_text_match_open = re.search(multiline_text_pattern_open, line)
	if multiline_text_match_open:
		data.append({
			"type" : "multi",
			"identifier": multiline_text_match_open.group(1),
			"content" : multiline_text_match_open.group(2)
		})

		is_multiline = True

		continue

	multiline_text_match_close = re.search(multiline_text_pattern_close, line)
	if multiline_text_match_close:
		data[line_counter]["content"] += "\n" + multiline_text_match_close.group(1)

		line_counter += 1

		is_multiline = False

		continue

	if is_multiline:
		print(data[line_counter])

		data[line_counter]["content"] += "\n" + line

		continue

	data.append({
		"type": "empty"
	})

	line_counter += 1

# Print the parsed data
for i, data_line in enumerate(data):
	print(data_line)
