def getelement(haystack, needle):
	for line in haystack:
		try:
			if line["identifier"] == needle:
				return line
		except KeyError:
			continue

def updatelang(base, update):
	newlang = []

	found_alias = False

	for i, line in enumerate(base):
		if line["type"] == "single" and line["identifier"] == "__alias":
			found_alias = True

		if not found_alias and not line["type"] == "code":
			if update[i]["content"] == "":
				newlang.append("\n")
			else:
				newlang.append("-- " + update[i]["content"] + "\n")

			continue

		if line["type"] == "comment" or line["type"] == "empty":
			if line["content"] != "":
				newlang.append("-- " + line["content"] + "\n")
			else:
				newlang.append("\n")

			continue

		if line["type"] == "code":
			old_code = getelement(update, "local")

			if not old_code:
				newlang.append("ERROR: LANGUAGE LINE MISSING\n")
			else:
				newlang.append(old_code["content"] + "\n")

			continue

		# element is already translated
		transline = getelement(update, line["identifier"])

		if transline != None:
			if line["type"] == "single":
				newlang.append("L." + transline["identifier"] + " = \"" + transline["content"] + "\"\n")
			else:
				newlang.append("L." + transline["identifier"] + " = [[" + transline["content"] + "]]\n")
		else:
			if line["type"] == "single":
				newlang.append("--L." + line["identifier"] + " = \"" + line["content"] + "\"\n")
			else:
				sanitized = line["content"].replace("\n", "\n--")

				newlang.append("--L." + line["identifier"] + " = [[" + sanitized + "]]\n")

	return newlang
			