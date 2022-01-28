from datetime import date

import requests
import json


def get_klass_subject_areas():
    yyyy_mm_dd = date.today()
    get_codes_today_url = f"https://data.ssb.no/api/klass/v1/classifications/15/codesAt?date={yyyy_mm_dd}"
    response_dict = json.loads(requests.get(get_codes_today_url, headers={"Accept": "application/json"}).text)
    return response_dict["codes"]


def reformat_node(item):
    new_node = {"key": item["code"], "label": item["name"]}
    if "children" in item:
        reformated_children = [reformat_node(child) for child in item["children"]]
        new_node["children"] = reformated_children
    return new_node


def add_children(parent, items_list):
    for item in items_list:
        if item["parentCode"] == parent["code"]:
            if "children" not in parent:
                parent["children"] = []
            parent["children"].append(add_children(item, items_list))
    return parent


def get_subject_areas_tree_select():
    subject_area_list = get_klass_subject_areas()
    items_top_level_list = [add_children(item, subject_area_list) for item in subject_area_list if item["level"] == "1"]
    tree_select_dict = {"root": list(map(reformat_node, items_top_level_list))}
    return tree_select_dict


if __name__ == "__main__":
    print(get_subject_areas_tree_select())
