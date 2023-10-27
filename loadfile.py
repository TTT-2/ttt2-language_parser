import re

# Define regular expressions to match different components
comment_pattern = r'--\s(.+)'
lang_pattern = r'local L = LANG\.CreateLanguage\("([^"]+)"\)'
singleline_text_pattern = r'L\.([a-zA-Z_][a-zA-Z_0-9]*)\s*=\s*"((?:\\"|[^"])*)"'
multiline_text_pattern_open = r'L\.([a-zA-Z_][a-zA-Z_0-9]*)\s*=\s*\[\[([^\]]*)'
multiline_text_pattern_close = r'(.*?)\]\]'
multiline_single_line = r'L\.([a-zA-Z_][a-zA-Z_0-9]*)\s*=\s*\[\[(.*?)\]\]'

def loadfile(path):
	# Create a list to store the data
	lines = []
	data = []

	# Open and read the file
	with open(path, "r", encoding="utf-8") as file:
		try:
			lines = file.readlines()
		except UnicodeDecodeError:
			print("ERROR: " + path)

			return

	line_counter = 0
	is_multiline = False

	# Iterate through the lines
	for line in lines:
		line = line.strip()

		# Check for comments
		lang_match = re.match(lang_pattern, line)
		if lang_match:
			data.append({
				"type" : "code",
				"identifier": "local",
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
		if singleline_text_match and line[0:2] != "--":
			data.append({
				"type" : "single",
				"identifier": singleline_text_match.group(1),
				"content" : singleline_text_match.group(2)
			})

			line_counter += 1

			continue
		
		multisingleline_text_match = re.search(multiline_single_line, line)
		if multisingleline_text_match and line[0:2] != "--":
			data.append({
				"type" : "multi",
				"identifier": multisingleline_text_match.group(1),
				"content" : multisingleline_text_match.group(2)
			})

			line_counter += 1

			continue

		multiline_text_match_open = re.search(multiline_text_pattern_open, line)

		if multiline_text_match_open and line[0:2] != "--":
			data.append({
				"type" : "multi",
				"identifier": multiline_text_match_open.group(1),
				"content" : multiline_text_match_open.group(2)
			})

			is_multiline = True

			continue

		multiline_text_match_close = re.search(multiline_text_pattern_close, line)
		if multiline_text_match_close and line[0:2] != "--":
			data[line_counter]["content"] += "\n" + multiline_text_match_close.group(1)

			line_counter += 1

			is_multiline = False

			continue

		if is_multiline and line[0:2] != "--":
			data[line_counter]["content"] += "\n" + line

			continue

		data.append({
			"type": "empty",
			"content": ""
		})

		line_counter += 1

	return data
