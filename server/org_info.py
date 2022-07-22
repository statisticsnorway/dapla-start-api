import json
from datetime import datetime
from functools import reduce


def get_klass_sectional_division(sectional_division_versions):
    response_dict = json.loads(sectional_division_versions.text)
    versions_list = response_dict["versions"]
    newest_version = reduce((
        lambda a, b:
        a if datetime.strptime(a["validFrom"], '%Y-%m-%d').date() > datetime.strptime(b["validFrom"], '%Y-%m-%d').date()
        else b
    ), versions_list)

    return newest_version["_links"]["self"]["href"]


def produce_org_info(newest_version_data):
    response_dict = json.loads(newest_version_data.text)
    org_info_list = response_dict["classificationItems"]
    sections = list(filter(lambda s: s["level"] == '2', org_info_list))
    simplified_sections = list(map(simplify_sections, sections))

    return simplified_sections


def simplify_sections(section):
    return {
        "code": section["code"],
        "parent_code": section["parentCode"],
        "name": section["name"]
    }
