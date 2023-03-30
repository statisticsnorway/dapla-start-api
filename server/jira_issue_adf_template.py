from typing import List

import yaml
from datetime import date

from .project_details import ProjectDetails, ProjectUser


def convert_display_name_to_uniform_team_name(display_team_name):
    return (display_team_name.lower().replace("team ", "").replace(
        " ", "-").replace("æ", "ae").replace("ø", "oe").replace("å", "aa"))


def get_issue_adf_dict(details: ProjectDetails):
    summary = f"On-boarding: {details.display_team_name}"  # This is the "header" of the Jira issue
    return {
        "fields": {
            "project": {
                "key": "DS"
            },  # DS is the 'key' for the Dapla Start project
            "summary": summary,
            "description": _description(details),
            "issuetype": {
                "name": "Task"
            },
        }
    }


def _description(details: ProjectDetails, current_date: date = None):
    if current_date is None:
        current_date = date.today()

    uniform_team_name_overridden = False
    uniform_team_name = convert_display_name_to_uniform_team_name(
        details.display_team_name)

    if details.uniform_team_name and uniform_team_name != details.uniform_team_name:
        uniform_team_name_overridden = True
        uniform_team_name = convert_display_name_to_uniform_team_name(
            details.uniform_team_name)

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
        "github_repo_name": iac_git_project_name,
    }

    if details.enabled_services and isinstance(details.enabled_services, list):
        for service in details.enabled_services:
            technical_details[f"enable_{service}"] = "yes"

    reporter_description = [
        {
            "type":
            "text",
            "text":
            f"Innmeldt av {details.reporter.name if details.reporter else ''} (",
        },
        {
            "type":
            "text",
            "text":
            f"{details.reporter.email if details.reporter else ''}",
            "marks": [{
                "type": "link",
                "attrs": {
                    "href":
                    f"mailto:{details.reporter.email if details.reporter else ''}"
                },
            }],
        },
        {
            "type": "text",
            "text": f") den {current_date.strftime('%d.%m.%Y')}",
        },
    ]

    access_groups = {
        "type":
        "table",
        "attrs": {
            "isNumberColumnEnabled": False,
            "layout": "default"
        },
        "content": [
            {
                "type":
                "tableRow",
                "content": [
                    {
                        "type":
                        "tableHeader",
                        "attrs": {},
                        "content": [{
                            "type":
                            "paragraph",
                            "content": [{
                                "type": "text",
                                "text": "Gruppenavn",
                                "marks": [{
                                    "type": "strong"
                                }],
                            }],
                        }],
                    },
                    {
                        "type":
                        "tableHeader",
                        "attrs": {},
                        "content": [{
                            "type":
                            "paragraph",
                            "content": [{
                                "type": "text",
                                "text": "Medlemmer",
                                "marks": [{
                                    "type": "strong"
                                }],
                            }],
                        }],
                    },
                ],
            },
            {
                "type": "tableRow",
                "content": _table_group_cells(mgm_group, [details.manager]),
            },
            {
                "type": "tableRow",
                "content": _table_group_cells(dad_group, details.data_admins),
            },
            {
                "type": "tableRow",
                "content": _table_group_cells(dev_group, details.developers),
            },
            {
                "type": "tableRow",
                "content": _table_group_cells(con_group, details.consumers),
            },
            {
                "type": "tableRow",
                "content": _table_group_cells(sup_group, details.support),
            },
        ],
    }

    description = {
        "version":
        1,
        "type":
        "doc",
        "content": [
            {
                "type":
                "heading",
                "attrs": {
                    "level": 1
                },
                "content": [{
                    "type":
                    "text",
                    "text":
                    f"{details.display_team_name} ({uniform_team_name})",
                }],
            },
            {
                "type":
                "panel",
                "attrs": {
                    "panelType": "note"
                },
                "content": [{
                    "type":
                    "paragraph",
                    "content":
                    reporter_description + [
                        {
                            "type": "hardBreak"
                        },
                        {
                            "type":
                            "text",
                            "text":
                            f"GUI-versjon: {details.ui_version}, API-versjon: {details.api_version}, teknisk teamnavn overstyrt: {'Ja' if uniform_team_name_overridden else 'Nei'}",
                            "marks": [{
                                "type": "subsup",
                                "attrs": {
                                    "type": "sub"
                                }
                            }],
                        },
                    ],
                }],
            },
            {
                "type":
                "panel",
                "attrs": {
                    "panelType": "note"
                },
                "content": [{
                    "type":
                    "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "Hovedansvarlig seksjon:"
                        },
                        {
                            "type": "hardBreak"
                        },
                        {
                            "type":
                            "text",
                            "text":
                            f"{details.org_info.name if details.org_info else '-'} ({details.org_info.code if details.org_info else '-'})",
                            "marks": [{
                                "type": "subsup",
                                "attrs": {
                                    "type": "sub"
                                }
                            }],
                        },
                    ],
                }],
            },
            {
                "type":
                "panel",
                "attrs": {
                    "panelType": "info"
                },
                "content": [{
                    "type":
                    "paragraph",
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
                        },
                    ],
                }],
            },
            {
                "type":
                "paragraph",
                "content": [{
                    "type":
                    "text",
                    "text":
                    "Her følger en liste med manuelle steg som må utføres før teamet er klart på Dapla.",
                }],
            },
            {
                "type":
                "paragraph",
                "content": [{
                    "type":
                    "text",
                    "text":
                    "Disse stegene utføres av Team Statistikktjenester!",
                    "marks": [
                        {
                            "type": "strong"
                        },
                        {
                            "type": "textColor",
                            "attrs": {
                                "color": "#bf2600"
                            }
                        },
                    ],
                }],
            },
            {
                "type": "rule"
            },
            {
                "type":
                "heading",
                "attrs": {
                    "level": 2
                },
                "content": [{
                    "type": "text",
                    "text": "1. Seksjonsleder godkjenner"
                }],
            },
            {
                "type":
                "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Sende en epost til "
                    },
                    {
                        "type":
                        "text",
                        "text":
                        "seksjonslederen for bestilleren",
                        "marks": [{
                            "type": "link",
                            "attrs": {
                                "href":
                                f"https://ssbno.sharepoint.com/sites/byraanettet/_layouts/15/search.aspx/people?q=seksjonssjef%20{details.org_info.code if details.org_info else '-'}"
                            },
                        }],
                    },
                    {
                        "type": "text",
                        "text": " med følgende tekst:"
                    },
                ],
            },
            {
                "type":
                "blockquote",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{
                            "type": "text",
                            "text": "Hei,"
                        }],
                    },
                    {
                        "type":
                        "paragraph",
                        "content": [{
                            "type":
                            "text",
                            "text":
                            "Vi har fått en forespørsel om oppretting av Dapla team fra noen i din seksjon. Trenger en godkjenning før vi kan gå videre.",
                        }],
                    },
                    {
                        "type":
                        "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text":
                                f"Teamnavn: {details.display_team_name}",
                            },
                            {
                                "type": "hardBreak"
                            },
                            {
                                "type": "text",
                                "text":
                                f"Teknisk teamnavn: {uniform_team_name}",
                            },
                            {
                                "type": "hardBreak"
                            },
                        ] + reporter_description,
                    },
                    {
                        "type": "paragraph",
                        "content": [{
                            "type": "text",
                            "text": "AD grupper:"
                        }],
                    },
                ],
            },
            access_groups,
            {
                "type":
                "heading",
                "attrs": {
                    "level": 2
                },
                "content": [{
                    "type": "text",
                    "text": "2. Opprette tilgangsgrupper"
                }],
            },
            {
                "type":
                "paragraph",
                "content": [
                    {
                        "type":
                        "text",
                        "text":
                        "Følgende tilgangsgrupper må opprettes ved å sende en e-post til ",
                    },
                    {
                        "type":
                        "text",
                        "text":
                        "kundeservice@ssb.no",
                        "marks": [{
                            "type": "link",
                            "attrs": {
                                "href": "mailto:kundeservice@ssb.no"
                            },
                        }],
                    },
                    {
                        "type":
                        "text",
                        "text":
                        ". Presiser gjerne at gruppene skal i OU=SSB/Grupper/Skytjenester/BIP.",
                    },
                ],
            },
            {
                "type":
                "blockquote",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{
                            "type": "text",
                            "text": "Hei Kundeservice,"
                        }],
                    },
                    {
                        "type":
                        "paragraph",
                        "content": [{
                            "type":
                            "text",
                            "text":
                            f"Det nye Dapla teamet '{details.display_team_name}' trenger AD grupper satt opp for seg og synkronisert til Google i sky. Dette betyr at gruppene skal inn i OU=SSB/Grupper/Skytjenester/BIP og må synkroniseres fra Azure Cloud til Google. Teamet tilhører seksjon: {details.org_info.name if details.org_info else '-'} ({details.org_info.code if details.org_info else '-'})",
                        }],
                    },
                    {
                        "type":
                        "paragraph",
                        "content": [{
                            "type":
                            "text",
                            "text":
                            "Følgende grupper med medlemmer ønskes:",
                        }],
                    },
                ],
            },
            access_groups,
            {
                "type":
                "blockquote",
                "content": [
                    {
                        "type":
                        "paragraph",
                        "content": [{
                            "type": "text",
                            "text": "Fint om dere kan ordne det!"
                        }],
                    },
                    {
                        "type":
                        "paragraph",
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
                            },
                        ],
                    },
                ],
            },
            {
                "type":
                "heading",
                "attrs": {
                    "level": 2
                },
                "content": [{
                    "type":
                    "text",
                    "text":
                    "3. Legge teamet til konfigurasjonsfil i Byråets IT-plattform (BIP)",
                }],
            },
            {
                "type":
                "paragraph",
                "content": [{
                    "type":
                    "text",
                    "text":
                    "Etter at tilgangsgruppene er opprettet må man legge til følgende linje:",
                }],
            },
            {
                "type":
                "codeBlock",
                "attrs": {},
                "content": [{
                    "type":
                    "text",
                    "text":
                    f'"{uniform_team_name}" : "{mgm_group}{domain}"',
                }],
            },
            {
                "type":
                "paragraph",
                "content": [{
                    "type": "text",
                    "text": "...til konfigurasjonen som ligger her:"
                }],
            },
            {
                "type":
                "paragraph",
                "content": [{
                    "type":
                    "text",
                    "text":
                    "https://github.com/statisticsnorway/bip-gcp-base-config/blob/main/terraform.tfvars",
                    "marks": [{
                        "type": "link",
                        "attrs": {
                            "href":
                            "https://github.com/statisticsnorway/bip-gcp-base-config/blob/main/terraform.tfvars"
                        },
                    }],
                }],
            },
            {
                "type":
                "heading",
                "attrs": {
                    "level": 2
                },
                "content": [{
                    "type":
                    "text",
                    "text":
                    "4. Opprette GitHub prosjekt for plattformressurser og Github data-admins team",
                }],
            },
            {
                "type":
                "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Prosjektet vil ha følgende navn i GitHub: ",
                    },
                    {
                        "type": "text",
                        "text": f"{iac_git_project_name}",
                        "marks": [{
                            "type": "strong"
                        }],
                    },
                ],
            },
            {
                "type":
                "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Bruk verktøyet "
                    },
                    {
                        "type":
                        "text",
                        "text":
                        "dapla-start-toolkit",
                        "marks": [{
                            "type": "link",
                            "attrs": {
                                "href":
                                "https://github.com/statisticsnorway/dapla-start-toolkit"
                            },
                        }],
                    },
                    {
                        "type": "text",
                        "text": " til dette."
                    },
                ],
            },
            {
                "type":
                "paragraph",
                "content": [{
                    "type":
                    "text",
                    "text":
                    "Når repoet er opprettet, følg disse stegene for å opprette et data admins team på Github:"
                }]
            },
            {
                "type":
                "orderedList",
                "attrs": {
                    "order": 1
                },
                "content": [{
                    "type":
                    "listItem",
                    "content": [{
                        "type":
                        "paragraph",
                        "content": [{
                            "type": "text",
                            "text": "Følg "
                        }, {
                            "type":
                            "text",
                            "text":
                            "denne lenken",
                            "marks": [{
                                "type": "link",
                                "attrs": {
                                    "href":
                                    "https://github.com/orgs/statisticsnorway/new-team"
                                }
                            }]
                        }, {
                            "type":
                            "text",
                            "text":
                            " for å starte opprettelsen av et nytt Github team"
                        }]
                    }]
                }, {
                    "type":
                    "listItem",
                    "content": [{
                        "type":
                        "paragraph",
                        "content": [{
                            "type":
                            "text",
                            "text":
                            "I “Identity Provider Groups” dropdown-menyen velg "
                        }, {
                            "type": "text",
                            "text": f"{uniform_team_name}-data-admins",
                            "marks": [{
                                "type": "strong"
                            }]
                        }, {
                            "type": "text",
                            "text": ". Under “Team Name” skriv "
                        }, {
                            "type": "text",
                            "text": f"{uniform_team_name}-data-admins",
                            "marks": [{
                                "type": "strong"
                            }]
                        }, {
                            "type": "text",
                            "text": "."
                        }]
                    }]
                }, {
                    "type":
                    "listItem",
                    "content": [{
                        "type":
                        "paragraph",
                        "content": [{
                            "type":
                            "text",
                            "text":
                            "Gå til Github siden til repoet du opprettet med dapla-start-toolkit i begynnelsen av dette steget. Fra der, naviger til: Settings > Collaborators and Teams > Add Teams. "
                        }]
                    }]
                }, {
                    "type":
                    "listItem",
                    "content": [{
                        "type":
                        "paragraph",
                        "content": [{
                            "type":
                            "text",
                            "text":
                            f"I søkefeltet, søk etter teamet du nettopp opprettet ({uniform_team_name}-data-admins). Velg teamet og huk av for “Admin” tilgang."
                        }]
                    }]
                }]
            },
            {
                "type":
                "heading",
                "attrs": {
                    "level": 2
                },
                "content": [{
                    "type":
                    "text",
                    "text":
                    "5. Sette opp automatisering av plattformressurser",
                }],
            },
            {
                "type":
                "paragraph",
                "content": [{
                    "type":
                    "text",
                    "text":
                    "Etter at GitHub repoet har blitt opprettet må det kobles til i en automatiseringsløsning som heter Atlantis. Det er tre hoved steg for å få dette til:",
                }],
            },
            {
                "type":
                "orderedList",
                "content": [
                    {
                        "type":
                        "listItem",
                        "content": [
                            {
                                "type":
                                "paragraph",
                                "content": [{
                                    "type":
                                    "text",
                                    "text":
                                    "Legge repoet til listen i Github appen",
                                }],
                            },
                            {
                                "type":
                                "orderedList",
                                "content": [
                                    {
                                        "type":
                                        "listItem",
                                        "content": [{
                                            "type":
                                            "paragraph",
                                            "content": [
                                                {
                                                    "type": "text",
                                                    "text": "Åpne "
                                                },
                                                {
                                                    "type":
                                                    "text",
                                                    "text":
                                                    "https://github.com/apps/atlantis-dapla-felles-ssb-no",
                                                    "marks": [{
                                                        "type": "link",
                                                        "attrs": {
                                                            "href":
                                                            "https://github.com/apps/atlantis-dapla-felles-ssb-no"
                                                        },
                                                    }],
                                                },
                                            ],
                                        }],
                                    },
                                    {
                                        "type":
                                        "listItem",
                                        "content": [{
                                            "type":
                                            "paragraph",
                                            "content": [
                                                {
                                                    "type": "text",
                                                    "text": "Klikk "
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "Configure",
                                                    "marks": [{
                                                        "type": "code"
                                                    }],
                                                },
                                            ],
                                        }],
                                    },
                                    {
                                        "type":
                                        "listItem",
                                        "content": [{
                                            "type":
                                            "paragraph",
                                            "content": [
                                                {
                                                    "type":
                                                    "text",
                                                    "text":
                                                    f"Søke etter {iac_git_project_name} under ",
                                                },
                                                {
                                                    "type": "text",
                                                    "text":
                                                    "Select repository",
                                                    "marks": [{
                                                        "type": "code"
                                                    }],
                                                },
                                                {
                                                    "type": "text",
                                                    "text": " feltet"
                                                },
                                            ],
                                        }],
                                    },
                                    {
                                        "type":
                                        "listItem",
                                        "content": [{
                                            "type":
                                            "paragraph",
                                            "content": [{
                                                "type":
                                                "text",
                                                "text":
                                                "Lagre endringen",
                                            }],
                                        }],
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "type":
                        "listItem",
                        "content": [
                            {
                                "type":
                                "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "Legge repoet til "
                                    },
                                    {
                                        "type": "text",
                                        "text": "allowlist",
                                        "marks": [{
                                            "type": "code"
                                        }],
                                    },
                                    {
                                        "type": "text",
                                        "text": " på Atlantis konfigurasjonen",
                                    },
                                ],
                            },
                            {
                                "type":
                                "orderedList",
                                "content": [
                                    {
                                        "type":
                                        "listItem",
                                        "content": [{
                                            "type":
                                            "paragraph",
                                            "content": [
                                                {
                                                    "type":
                                                    "text",
                                                    "text":
                                                    "Legge til repo URL på slutten av ",
                                                },
                                                {
                                                    "type":
                                                    "text",
                                                    "text":
                                                    "denne linjen",
                                                    "marks": [{
                                                        "type": "link",
                                                        "attrs": {
                                                            "href":
                                                            "https://github.com/statisticsnorway/atlantis-team-config/blob/b4e018d5bf6944b73aa061aa07462a65f3d7d0d0/kubernetes-manifests/dapla-felles/atlantis-statefulset/atlantis-statefulset.yaml#L35"
                                                        },
                                                    }],
                                                },
                                            ],
                                        }],
                                    },
                                    {
                                        "type":
                                        "listItem",
                                        "content": [{
                                            "type":
                                            "paragraph",
                                            "content": [{
                                                "type":
                                                "text",
                                                "text":
                                                "Åpne og merge en PR med endringen",
                                            }],
                                        }],
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "type":
                        "listItem",
                        "content": [
                            {
                                "type":
                                "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "Apply’e "
                                    },
                                    {
                                        "type": "text",
                                        "text": "allowlist",
                                        "marks": [{
                                            "type": "code"
                                        }],
                                    },
                                    {
                                        "type":
                                        "text",
                                        "text":
                                        " endringene til Atlantis instansen",
                                    },
                                ],
                            },
                            {
                                "type":
                                "orderedList",
                                "content": [
                                    {
                                        "type":
                                        "listItem",
                                        "content": [{
                                            "type":
                                            "paragraph",
                                            "content": [{
                                                "type":
                                                "text",
                                                "text":
                                                "Clone eller pulle endringene på main grenen",
                                            }],
                                        }],
                                    },
                                    {
                                        "type":
                                        "listItem",
                                        "content": [{
                                            "type":
                                            "paragraph",
                                            "content": [
                                                {
                                                    "type": "text",
                                                    "text": "Kjøre "
                                                },
                                                {
                                                    "type": "text",
                                                    "text":
                                                    "gcloud container clusters get-credentials atlantis-prod --zone europe-north1 --project atlantis-prod-0073",
                                                    "marks": [{
                                                        "type": "code"
                                                    }],
                                                },
                                            ],
                                        }],
                                    },
                                    {
                                        "type":
                                        "listItem",
                                        "content": [{
                                            "type":
                                            "paragraph",
                                            "content": [
                                                {
                                                    "type": "text",
                                                    "text": "Kjøre "
                                                },
                                                {
                                                    "type": "text",
                                                    "text":
                                                    "kubectl apply -f kubernetes-manifests/dapla-felles/atlantis-statefulset/atlantis-statefulset.yaml",
                                                    "marks": [{
                                                        "type": "code"
                                                    }],
                                                },
                                            ],
                                        }],
                                    },
                                    {
                                        "type":
                                        "listItem",
                                        "content": [{
                                            "type":
                                            "paragraph",
                                            "content": [
                                                {
                                                    "type":
                                                    "text",
                                                    "text":
                                                    "Verifisere at instansen er oppdatert ved å kjøre ",
                                                },
                                                {
                                                    "type": "text",
                                                    "text":
                                                    "kubectl describe statefulset atlantis-dapla-felles",
                                                    "marks": [{
                                                        "type": "code"
                                                    }],
                                                },
                                            ],
                                        }],
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
            {
                "type":
                "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Se siden her for mer detaljer: "
                    },
                    {
                        "type":
                        "text",
                        "text":
                        "https://docs.bip.ssb.no/how-to/gitops/",
                        "marks": [{
                            "type": "link",
                            "attrs": {
                                "href":
                                "https://docs.bip.ssb.no/how-to/gitops/"
                            },
                        }],
                    },
                ],
            },
            {
                "type":
                "heading",
                "attrs": {
                    "level": 2
                },
                "content": [{
                    "type": "text",
                    "text": "6. Opprette teamets infrastruktur"
                }],
            },
            {
                "type":
                "paragraph",
                "content": [{
                    "type":
                    "text",
                    "text":
                    f"Nå er teamets infrastruktur klar til å opprettes fra Atlantis. Opprett en pull request i '{iac_git_project_name}' og få en godkjenning av Team Statistikktjenester.",
                }],
            },
            {
                "type":
                "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Deretter kan man skrive kommandoen "
                    },
                    {
                        "type": "text",
                        "text": "atlantis apply",
                        "marks": [{
                            "type": "code"
                        }],
                    },
                    {
                        "type":
                        "text",
                        "text":
                        " i pull requesten før man kjører merge og sletter branchen. Dette vil opprette teamets infrastruktur på Google Cloud Platform.",
                    },
                ],
            },
            {
                "type": "heading",
                "attrs": {
                    "level": 2
                },
                "content": [{
                    "type": "text",
                    "text": "7. Flere tjenester"
                }],
            },
            {
                "type":
                "paragraph",
                "content": [{
                    "type":
                    "text",
                    "text":
                    f"Tjenester som er forespurt: {details.enabled_services or 'Ingen'}",
                }],
            },
            {
                "type":
                "paragraph",
                "content": [
                    {
                        "type":
                        "text",
                        "text":
                        "Hvis Transfer Service er forespurt, send en epost til ",
                    },
                    {
                        "type":
                        "text",
                        "text":
                        "Kundeservice",
                        "marks": [{
                            "type": "link",
                            "attrs": {
                                "href": "mailto:kundeservice@ssb.no"
                            },
                        }],
                    },
                    {
                        "type": "text",
                        "text": "."
                    },
                ],
            },
            {
                "type":
                "paragraph",
                "content": [{
                    "type":
                    "text",
                    "text":
                    "Kundeservice må sette opp en Transfer Service agent og katalog på Linuxstammen.",
                }],
            },
            {
                "type":
                "blockquote",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{
                            "type": "text",
                            "text": "Hei Kundeservice,"
                        }],
                    },
                    {
                        "type":
                        "paragraph",
                        "content": [{
                            "type":
                            "text",
                            "text":
                            f"Det nye Dapla teamet '{details.display_team_name}' trenger Transfer "
                            f"Service satt opp for seg. Johnny Niklasson, Tore Vestbekken eller Stian "
                            f"Henriksen på Kundeservice kan utføre jobben. Teamet tilhører seksjon: {details.org_info.name if details.org_info else '-'} ({details.org_info.code if details.org_info else '-'})",
                        }],
                    },
                    {
                        "type":
                        "paragraph",
                        "content": [{
                            "type":
                            "text",
                            "text":
                            "AD-gruppe som skal ha tilgang til synk område on-prem:",
                        }],
                    },
                    {
                        "type": "paragraph",
                        "content": [{
                            "type": "text",
                            "text": f"    {dad_group}"
                        }],
                    },
                    {
                        "type":
                        "paragraph",
                        "content": [{
                            "type": "text",
                            "text": "Prosjektnavn i GCP:"
                        }],
                    },
                    {
                        "type":
                        "paragraph",
                        "content": [{
                            "type": "text",
                            "text": f"    {uniform_team_name}-ts"
                        }],
                    },
                    {
                        "type":
                        "paragraph",
                        "content": [{
                            "type": "text",
                            "text": "Fint om dere kan ordne det!"
                        }],
                    },
                    {
                        "type":
                        "paragraph",
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
                            },
                        ],
                    },
                ],
            },
            {
                "type":
                "paragraph",
                "content": [{
                    "type":
                    "text",
                    "text":
                    "Etter at Kundeservice har satt opp agenten og opprettet en katalogstruktur på "
                    "Linuxstammen kan du henvise en Data Admin til følgende dokument som beskriver hvordan "
                    "man setter opp Transfer Service på Google Cloud Platform:",
                }],
            },
            {
                "type":
                "paragraph",
                "content": [{
                    "type":
                    "text",
                    "text":
                    "https://docs.dapla.ssb.no/dapla-user/how-to/transfer-data/",
                    "marks": [{
                        "type": "link",
                        "attrs": {
                            "href":
                            "https://docs.dapla.ssb.no/dapla-user/how-to/transfer-data/"
                        },
                    }],
                }],
            },
            {
                "type":
                "heading",
                "attrs": {
                    "level": 2
                },
                "content": [{
                    "type": "text",
                    "text": "8. Opplyse bestilleren at teamet er klar"
                }],
            },
            {
                "type":
                "paragraph",
                "content": [
                    {
                        "type":
                        "text",
                        "text":
                        f"Sende en epost eller melding til {details.reporter.name if details.reporter else ''} (",
                    },
                    {
                        "type":
                        "text",
                        "text":
                        f"{details.reporter.email if details.reporter else ''}",
                        "marks": [{
                            "type": "link",
                            "attrs": {
                                "href":
                                f"mailto:{details.reporter.email if details.reporter else ''}"
                            },
                        }],
                    },
                    {
                        "type": "text",
                        "text": ") med følgende tekst:"
                    },
                ],
            },
            {
                "type":
                "blockquote",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{
                            "type": "text",
                            "text": "Hei,"
                        }],
                    },
                    {
                        "type":
                        "paragraph",
                        "content": [
                            {
                                "type":
                                "text",
                                "text":
                                "Opplyser at Dapla teamet du bestilt er nå klar. Informasjon over hva det betyr og hvordan å ta Dapla i bruk finnes her: ",
                            },
                            {
                                "type":
                                "text",
                                "text":
                                "https://manual.dapla.ssb.no/dapla-team.html",
                                "marks": [{
                                    "type": "link",
                                    "attrs": {
                                        "href":
                                        "https://manual.dapla.ssb.no/dapla-team.html"
                                    },
                                }],
                            },
                        ],
                    },
                    {
                        "type":
                        "paragraph",
                        "content": [{
                            "type": "text",
                            "text": "Lykke til med reisen til skyen!"
                        }],
                    },
                ],
            },
            {
                "type":
                "heading",
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
                        },
                    },
                    {
                        "type": "text",
                        "text": " "
                    },
                ],
            },
            {
                "type":
                "paragraph",
                "content": [{
                    "type":
                    "text",
                    "text":
                    "Gratulerer! Hvis alt har gått etter planen er alt ferdig, og klar til bruk.",
                }],
            },
            {
                "type": "paragraph",
                "content": []
            },
            {
                "type": "paragraph",
                "content": [{
                    "type": "text",
                    "text": "Teknisk informasjon:"
                }],
            },
            {
                "type":
                "codeBlock",
                "attrs": {
                    "language": "yaml"
                },
                "content": [{
                    "type":
                    "text",
                    "text":
                    f"{yaml.dump(technical_details, sort_keys=False, allow_unicode=True)}",
                }],
            },
            {
                "type": "paragraph",
                "content": []
            },
        ],
    }

    return description


def _table_group_cells(group_name: str, users: List[ProjectUser]):
    sorted_users = None if users is None else sorted(
        users, key=lambda user: user.name)
    return [
        {
            "type":
            "tableCell",
            "attrs": {},
            "content": [{
                "type": "paragraph",
                "content": [{
                    "type": "text",
                    "text": f"{group_name}"
                }],
            }],
        },
        {
            "type":
            "tableCell",
            "attrs": {},
            "content": [{
                "type":
                "paragraph" if sorted_users is None else "bulletList",
                "content":
                list(
                    map(
                        lambda user: {
                            "type":
                            "listItem",
                            "content": [{
                                "type":
                                "paragraph",
                                "content": [{
                                    "type":
                                    "text",
                                    "text":
                                    f"{user.name} ({user.email_short})",
                                }],
                            }],
                        },
                        sorted_users or [],
                    )),
            }],
        },
    ]
