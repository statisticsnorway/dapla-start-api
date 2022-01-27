from datetime import date

import requests
import json


def get_items():
    yyyy_mm_dd = date.today()
    get_codes_today_url = f"https://data.ssb.no/api/klass/v1/classifications/15/codesAt?date={yyyy_mm_dd}"
    response_dict = json.loads(requests.get(get_codes_today_url, headers={"Accept": "application/json"}).text)
    return response_dict["codes"]


def get_subject_areas_tree_select():
    items = get_items()
    items_tree = [add_children(item, items) for item in items if item["level"] == "1"]
    tree_dict = {"root": list(map(reformat_node, items_tree))}
    json_dumps = json.dumps(tree_dict, indent=4, ensure_ascii=False)
    return json_dumps


def reformat_node(node):
    new_node = {"key": node["code"], "label": node["name"]}
    if "children" in node:
        reformated_children = [reformat_node(child) for child in node["children"]]
        new_node["children"] = reformated_children
    return new_node


def add_children(parent, items_list):
    for item in items_list:
        if item["parentCode"] == parent["code"]:
            if "children" not in parent:
                parent["children"] = []
            parent["children"].append(add_children(item, items_list))
    return parent


if __name__ == "__main__":
    print(get_subject_areas_tree_select())
