import sys

import json
import re
import xml.etree.ElementTree as ET
import os

LAUNCHER_DIR = "/usr/local/bin/charm"
RECENT_XPATH = ".//component[@name='RecentProjectsManager']/option[@name='additionalInfo']/map/entry"


def parse_start_script(path=LAUNCHER_DIR):
    run_path, config_path = None, None
    for line in open(path, "r"):
        line = line.strip()
        if line.startswith("CONFIG_PATH = "):
            config_path = line.split("=")[1].strip().replace("u'", "").rstrip("'")
        elif line.startswith("RUN_PATH = "):
            run_path = line.split("=")[1].strip().replace("u'", "").rstrip("'")
    return run_path, config_path


def match_name(path_with_names, query):
    fuzzy_re = ".*".join(query)
    for path, name in path_with_names:
        if re.match(fuzzy_re, name, re.IGNORECASE):
            yield path, name


def main():
    pycharm_path, config_path = parse_start_script()
    home_dir = os.path.expanduser("~")

    root = ET.parse(config_path + "/options/recentProjects.xml")
    project_paths = (
        el.attrib["key"].replace("$USER_HOME$", home_dir)
        for el in root.findall(RECENT_XPATH)
    )

    path_with_names = ((path, os.path.basename(path)) for path in project_paths)

    query = sys.argv[1]
    alfred_results = []
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
