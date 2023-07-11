import sys

import json
import re
import xml.etree.ElementTree as ET
import os

LAUNCHER_DIR = "/usr/local/bin/charm"
RECENT_XPATH = ".//component[@name='RecentProjectsManager']/option[@name='additionalInfo']/map/entry"


def parse_start_script(path=LAUNCHER_DIR):
    config_path = None
    for line in open(path, "r"):
        line = line.strip()
        if line.startswith("CONFIG_PATH = "):
            config_path = line.split("=")[1].strip().replace("u'", "").rstrip("'")
    return config_path


def match_name(path_with_names, query):
    fuzzy_re = re.compile(".*".join(query), re.IGNORECASE)
    for path, name in path_with_names:
        if fuzzy_re.match(name):
            yield path, name


def main():
    config_path = parse_start_script()
    alfred_results = []
    if config_path:
        home_dir = os.path.expanduser("~")

        root = ET.parse(config_path + "/options/recentProjects.xml")
        project_paths = (
            el.attrib["key"].replace("$USER_HOME$", home_dir)
            for el in root.findall(RECENT_XPATH)
        )

        path_with_names = ((path, os.path.basename(path)) for path in project_paths)

        query = sys.argv[1]
        for path, name in match_name(path_with_names, query):
            alfred_results.append(
                {
                    "title": name,
                    "subtitle": path,
                    "arg": path,
                    "uid": path,
                    "autocomplete": path,
                    "icon": {"path": "./icon.png"},
                }
            )
    response = json.dumps({"items": alfred_results})
    sys.stdout.write(response)


if __name__ == "__main__":
    main()
