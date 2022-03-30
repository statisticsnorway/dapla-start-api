from typing import List

import yaml
from datetime import date

from .project_details import ProjectDetails, ProjectUser


def convert_display_name_to_uniform_team_name(display_team_name):
    rm_prefix_and_spaces = display_team_name.lower().replace("team ", "").replace(" ", "-")
    replace_norwegian_letters = rm_prefix_and_spaces.replace("æ", "ae").replace("ø", "oe").replace("å", "aa")
    return replace_norwegian_letters


def get_issue_adf_dict(details: ProjectDetails):
    summary = f"On-boarding: {details.display_team_name}"  # This is the "header" of the Jira issue
    return {
        "fields": {
            "project": {
                "key": "DS"  # DS is the 'key' for the Dapla Start project
            },
            "summary": summary,
            "description":
                _description(details)
            ,
            "issuetype": {
                "name": "Task"
            }
        }
    }


def _description(details: ProjectDetails, current_date=date.today()):
    uniform_team_name = convert_display_name_to_uniform_team_name(details.display_team_name)
    iac_git_project_name = f"{uniform_team_name}-iac"
    domain = "@groups.ssb.no"
    mgm_group = f"{uniform_team_name}-managers"
    dad_group = f"{uniform_team_name}-data-admins"
    dev_group = f"{uniform_team_name}-developers"
    con_group = f"{uniform_team_name}-consumers"
    sup_group = f"{uniform_team_name}-support"
    technical_details = {
        "display_team_name": details.display_team_name,
        "uniform_team_name": uniform_team_name,
        "github_repo_name": iac_git_project_name
    }

    if details.enabled_services and isinstance(details.enabled_services, list):
        for service in details.enabled_services:
            technical_details[f"enable_{service}"] = "yes"

    description = {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "heading",
                "attrs": {
                    "level": 1
                },
                "content": [
                    {
                        "type": "text",
                        "text": f"{details.display_team_name}"
                    }
                ]
            },
            {
                "type": "panel",
                "attrs": {
                    "panelType": "note"
                },
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Innmeldt av {details.reporter.name if details.reporter else ''} ("
                            },
                            {
                                "type": "text",
                                "text": f"{details.reporter.email if details.reporter else ''}",
                                "marks": [
                                    {
                                        "type": "link",
                                        "attrs": {
                                            "href": f"mailto:{details.reporter.email if details.reporter else ''}"
                                        }
                                    }
                                ]
                            },
                            {
                                "type": "text",
                                "text": f") den {current_date.strftime('%d.%m.%Y')}"
                            },
                            {
                                "type": "hardBreak"
                            },
                            {
                                "type": "text",
                                "text": f"GUI-versjon: {details.ui_version}, API-versjon {details.api_version}",
                                "marks": [
                                    {
                                        "type": "subsup",
                                        "attrs": {
                                            "type": "sub"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "type": "panel",
                "attrs": {
                    "panelType": "info"
                },
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": "Annen informasjon"
                            },
                            {
                                "type": "hardBreak"
                            },
                            {
                                "type": "text",
                                "text": f"{details.other_info or '-'}"
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
                        "text": "Her følger en liste med manuelle steg som må utføres før teamet er klart på Dapla."
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Disse stegene utføres av Team Argus!",
                        "marks": [
                            {
                                "type": "strong"
                            },
                            {
                                "type": "textColor",
                                "attrs": {
                                    "color": "#bf2600"
                                }
                            }
                        ]
                    }
                ]
            },
            {
                "type": "rule"
            },
            {
                "type": "heading",
                "attrs": {
                    "level": 2
                },
                "content": [
                    {
                        "type": "text",
                        "text": "1. Opprette tilgangsgrupper"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Følgende tilgangsgrupper må opprettes ved å sende en e-post til "
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
                        "text": ". Presiser gjerne at gruppene skal i OU=SSB/Grupper/Skytjenester/BIP."
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
                                "text": "Hei Kundeservice,"
                            }
                        ]
                    },
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Det nye Dapla teamet '{details.display_team_name}' trenger AD grupper satt opp for seg og synkronisert til Google i sky. Dette betyr at gruppene skal inn i OU=SSB/Grupper/Skytjenester/BIP og må synkroniseres fra Azure Cloud til Google."
                            }
                        ]
                    },
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": "Følgende grupper med medlemmer ønskes:"
                            }
                        ]
                    }
                ]
            },
            {
                "type": "table",
                "attrs": {
                    "isNumberColumnEnabled": False,
                    "layout": "default",
                    "localId": "72372212-4247-4646-818b-11f4681f924c"
                },
                "content": [
                    {
                        "type": "tableRow",
                        "content": [
                            {
                                "type": "tableHeader",
                                "attrs": {},
                                "content": [
                                    {
                                        "type": "paragraph",
                                        "content": [
                                            {
                                                "type": "text",
                                                "text": "Gruppenavn",
                                                "marks": [
                                                    {
                                                        "type": "strong"
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "tableHeader",
                                "attrs": {},
                                "content": [
                                    {
                                        "type": "paragraph",
                                        "content": [
                                            {
                                                "type": "text",
                                                "text": "Medlemmer",
                                                "marks": [
                                                    {
                                                        "type": "strong"
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "type": "tableRow",
                        "content": _table_group_cells(mgm_group, [details.manager])
                    },
                    {
                        "type": "tableRow",
                        "content": _table_group_cells(dad_group, details.data_admins)
                    },
                    {
                        "type": "tableRow",
                        "content": _table_group_cells(dev_group, details.developers)
                    },
                    {
                        "type": "tableRow",
                        "content": _table_group_cells(con_group, details.consumers)
                    },
                    {
                        "type": "tableRow",
                        "content": _table_group_cells(sup_group, details.support)
                    },
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
                            },
                            {
                                "type": "hardBreak"
                            },
                            {
                                "type": "text",
                                "text": "…"
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
                        "text": "2. Legge teamet til konfigurasjonsfil i Byråets IT-plattform (BIP)"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Etter at tilgangsgruppene er opprettet må man legge til følgende linje:"
                    }
                ]
            },
            {
                "type": "codeBlock",
                "attrs": {},
                "content": [
                    {
                        "type": "text",
                        "text": f"\"{uniform_team_name}\" : \"{mgm_group}{domain}\""
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "...til konfigurasjonen som ligger her:"
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
                        "text": "3. Opprette GitHub prosjekt for plattformressurser"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Prosjektet vil ha følgende navn i GitHub: "
                    },
                    {
                        "type": "text",
                        "text": f"{iac_git_project_name}",
                        "marks": [
                            {
                                "type": "strong"
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
                        "text": "Bruk verktøyet "
                    },
                    {
                        "type": "text",
                        "text": "dapla-start-toolkit",
                        "marks": [
                            {
                                "type": "link",
                                "attrs": {
                                    "href": "https://github.com/statisticsnorway/dapla-start-toolkit"
                                }
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": " til dette."
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
                        "text": "4. Sette opp automatisering av plattformressurser"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Etter at GitHub-prosjektet har blitt opprettet må det legges til i en automatiseringsløsning som heter Atlantis. Dette gjøres ved å følge instruksjonene i "
                    },
                    {
                        "type": "text",
                        "text": "denne lenken",
                        "marks": [
                            {
                                "type": "link",
                                "attrs": {
                                    "href": "https://docs.bip.ssb.no/how-to/gitops"
                                }
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": ". <team_name> i kontekst av instruksjonene skal være dapla-felles."
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
                        "text": "5. Opprette teamets infrastruktur"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": f"Nå er teamets infrastruktur klar til å opprettes fra Atlantis. Opprett en pull request in '{iac_git_project_name}' og få en godkjenning av Team Argus."
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Deretter kan man skrive kommandoen "
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
                        "text": " i pull requesten før man kjører merge og sletter branchen. Dette vil opprette teamets infrastruktur på Google Cloud Platform."
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
                        "text": "6. Flere tjenester"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": f"Tjenester som er forespurt: {details.enabled_services or 'Ingen'}"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Hvis Transfer Service er forespurt, send en epost til "
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
                        "text": "."
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Kundeservice må sette opp en Transfer Service agent og katalog på Linuxstammen."
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
                                "text": "Hei Kundeservice,"
                            }
                        ]
                    },
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Det nye Dapla teamet '{details.display_team_name}' trenger Transfer "
                                        f"Service satt opp for seg. Johnny Niklasson, Tore Vestbekken eller Stian "
                                        f"Henriksen på Kundeservice kan utføre jobben."
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
                                "text": f"    {dad_group}"
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
                            },
                            {
                                "type": "hardBreak"
                            },
                            {
                                "type": "text",
                                "text": "…"
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
                        "text": "Etter at Kundeservice har satt opp agenten og opprettet en katalogstruktur på "
                                "Linuxstammen kan du henvise en Data Admin til følgende dokument som beskriver hvordan "
                                "man setter opp Transfer Service på Google Cloud Platform:"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "https://docs.dapla.ssb.no/dapla-user/how-to/transfer-data/",
                        "marks": [
                            {
                                "type": "link",
                                "attrs": {
                                    "href": "https://docs.dapla.ssb.no/dapla-user/how-to/transfer-data/"
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
                        "text": "Ferdig "
                    },
                    {
                        "type": "emoji",
                        "attrs": {
                            "shortName": ":tada:",
                            "id": "1f389",
                            "text": "🎉"
                        }
                    },
                    {
                        "type": "text",
                        "text": " "
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Gratulerer! Hvis alt har gått etter planen er alt ferdig, og klar til bruk."
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
                        "text": "Teknisk informasjon:"
                    }
                ]
            },
            {
                "type": "codeBlock",
                "attrs": {
                    "language": "yaml"
                },
                "content": [
                    {
                        "type": "text",
                        "text": f"{yaml.dump(technical_details, sort_keys=False, allow_unicode=True)}"
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": []
            }
        ]
    }

    return description


def _table_group_cells(group_name: str, users: List[ProjectUser]):
    sorted_users = None if users is None else sorted(users, key=lambda user: user.name)
    return [
        {
            "type": "tableCell",
            "attrs": {},
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{group_name}"
                        }
                    ]
                }
            ]
        },
        {
            "type": "tableCell",
            "attrs": {},
            "content": [
                {
                    "type": "paragraph" if sorted_users is None else "bulletList",
                    "content": list(map(lambda user: {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"{user.name} ({user.email_short})"
                                    }
                                ]
                            }
                        ]
                    }, sorted_users or []))
                }
            ]
        }
    ]
