from .project_details import ProjectDetails
import yaml


def convert_display_name_to_uniform_team_name(display_team_name):
    rm_prefix_and_spaces = display_team_name.lower().replace("team ", "").replace(" ", "-")
    replace_norwegian_letters = rm_prefix_and_spaces.replace("æ", "ae").replace("ø", "oe").replace("å", "aa")
    return replace_norwegian_letters


def get_issue_adf_dict(details: ProjectDetails):
    summary = f"On-boarding: {details.display_team_name}"  # This is the "header" of the Jira issue
    uniform_team_name = convert_display_name_to_uniform_team_name(details.display_team_name)
    iac_git_project_name = f"dapla-team-{uniform_team_name}"
    domain = "@groups.ssb.no"
    mgm_group = f"{uniform_team_name}-managers{domain}"
    dpo_group = f"{uniform_team_name}-data-protection-officers{domain}"
    dev_group = f"{uniform_team_name}-developers{domain}"
    con_group = f"{uniform_team_name}-consumers{domain}"
    services_dict = {"display_team_name": details.display_team_name}

    if details.enabled_services and isinstance(details.enabled_services, list):
        for service in details.enabled_services:
            services_dict[f"enable_{service}"] = "yes"

    description = {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "YAML:"
                    }
                ]
            },
            {
                "type": "codeBlock",
                "attrs": {},
                "content": [
                    {
                        "type": "text",
                        "text": f"{yaml.dump(services_dict)}"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": []
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": f"Uniform team name: '{uniform_team_name}'"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": f"“Infrastructure as Code” GitHub project name: '{iac_git_project_name}'"
                    }
                ]
            },
            {
                "type": "heading",
                "attrs": {
                    "level": 2
                },
                "content": [
                    {
                        "type": "text",
                        "text": "1. AD group creation"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "These AD groups should be created for the team. Send the request to "
                    },
                    {
                        "type": "text",
                        "text": "kundeservice@ssb.no",
                        "marks": [
                            {
                                "type": "link",
                                "attrs": {
                                    "href": "mailto:kundeservice@ssb.no"
                                }
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": "."
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": f"AD group: {mgm_group}"
                    }
                ]
            },
            {
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"members: {details.manager}"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": []
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": f"AD group: {dpo_group}"
                    }
                ]
            },
            {
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"members: {details.data_protection_officers}"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "    "
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": f"AD group: {dev_group}"
                    }
                ]
            },
            {
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"members: {details.developers}"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "    "
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": f"AD group: {con_group}"
                    }
                ]
            },
            {
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"members: {details.consumers}"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "type": "heading",
                "attrs": {
                    "level": 2
                },
                "content": [
                    {
                        "type": "text",
                        "text": "2. bip-gcp-base-config"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "AFTER AD groups have been created, add the following line:"
                    }
                ]
            },
            {
                "type": "codeBlock",
                "attrs": {},
                "content": [
                    {
                        "type": "text",
                        "text": f"\"{uniform_team_name}\" : \"{mgm_group}\""
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "...to the dictionary in this file: "
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "https://github.com/statisticsnorway/bip-gcp-base-config/blob/main/terraform.tfvars",
                        "marks": [
                            {
                                "type": "link",
                                "attrs": {
                                    "href": "https://github.com/statisticsnorway/bip-gcp-base-config/blob/main/terraform.tfvars"
                                }
                            }
                        ]
                    }
                ]
            },
            {
                "type": "heading",
                "attrs": {
                    "level": 2
                },
                "content": [
                    {
                        "type": "text",
                        "text": "3. Create GCP Team IaC GitHub repository"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": f"IaC GitHub project name: '{iac_git_project_name}'"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Use the dapla-start-toolkit for this."
                    }
                ]
            },
            {
                "type": "heading",
                "attrs": {
                    "level": 2
                },
                "content": [
                    {
                        "type": "text",
                        "text": "4. Atlantis Whitelist"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Once the IaC GitHub repository has been created, it needs to be whitelisted by BIP Atlantis. This request can be made to the "
                    },
                    {
                        "type": "text",
                        "text": "#hjelp_bip",
                        "marks": [
                            {
                                "type": "link",
                                "attrs": {
                                    "href": "https://ssb-norge.slack.com/archives/C915HHACX"
                                }
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": " Slack channel"
                    }
                ]
            },
            {
                "type": "blockquote",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Hei Stratus, kan dere whiteliste repoet '{iac_git_project_name}' i Atlantis?"
                            }
                        ]
                    }
                ]
            },
            {
                "type": "heading",
                "attrs": {
                    "level": 2
                },
                "content": [
                    {
                        "type": "text",
                        "text": "5. Apply terraform with Atlantis"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": f"Create a pull request in '{iac_git_project_name}', get approval from Team Stratus"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "and then run the "
                    },
                    {
                        "type": "text",
                        "text": "atlantis apply",
                        "marks": [
                            {
                                "type": "code"
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": " command in the pull request before you merge and delete the branch."
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "This will cause Atlantis to build our requested infrastructure in GCP."
                    }
                ]
            },
            {
                "type": "heading",
                "attrs": {
                    "level": 2
                },
                "content": [
                    {
                        "type": "text",
                        "text": "6. Additional Services"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": f"Requested services: {details.enabled_services}"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "If Transfer Service is requested, send a request to "
                    },
                    {
                        "type": "text",
                        "text": "Kundeservice",
                        "marks": [
                            {
                                "type": "link",
                                "attrs": {
                                    "href": "mailto:kundeservice@ssb.no"
                                }
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": ". "
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Kundeservice needs to set up the Transfer Service agent and directory in Linuxstammen."
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": []
            },
            {
                "type": "blockquote",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": "Hei Kundeservice,"
                            }
                        ]
                    },
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Det nye dapla teamet '{details.display_team_name}' trenger transfer service satt opp for seg."
                            }
                        ]
                    },
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": "AD-gruppe som skal ha tilgang til synk område on-prem:"
                            }
                        ]
                    },
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": f"    {dpo_group}"
                            }
                        ]
                    },
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": "Prosjektnavn i GCP:"
                            }
                        ]
                    },
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": f"    {uniform_team_name}-ts"
                            }
                        ]
                    },
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": "Fint om dere kan ordne det!"
                            }
                        ]
                    },
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": "Vennlig hilsen,"
                            }
                        ]
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": []
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "After Kundeservice has activated the agent and created the directory structure in Linuxstammen, "
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": f"you can refer the managers ({details.manager}) and/or DPOs ({details.data_protection_officers}) to the docs"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "for activating the transfer service on the GCP side:"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "https://docs.dapla.ssb.no/dapla-user/transfer/",
                        "marks": [
                            {
                                "type": "link",
                                "attrs": {
                                    "href": "https://docs.dapla.ssb.no/dapla-user/transfer/"
                                }
                            }
                        ]
                    }
                ]
            },
            {
                "type": "heading",
                "attrs": {
                    "level": 2
                },
                "content": [
                    {
                        "type": "text",
                        "text": "Done!"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Congratulations, if everything went according to plan, you are now done!"
                    }
                ]
            }
        ]
    }

    issue_dict = {
        "fields": {
            "project": {
                "key": "DS"  # DS is the 'key' for the Dapla Start project
            },
            "summary": summary,
            "description": description,
            "issuetype": {
                "name": "Task"
            }
        }
    }
    return issue_dict
