# MISP Galaxies to STIX 2.0 mapping

MISP galaxies are exported in `Attack Pattern`, `Course of Action`, `Malware`, `Threat Actor`, `Tool` or `Vulnerability` objects.

Sometimes 2 different Galaxies are mapped into the same STIX 2.0 object, the following examples don't show each Galaxy type, but only one for each resulting STIX object. If you want to see the complete mapping, the [MISP Galaxies to STIX 2.0 mapping summary](README.md#Galaxies-to-STIX-20-mapping) gives all the Galaxy types that are mapped into each STIX object type

Since not all the fields of the galaxies and their clusters are exported into STIX 2.0, the following examples are given with the fields that are exported only, if you want to have a look at the full definitions, you can visit the [MISP Galaxies repository](https://github.com/MISP/misp-galaxy).

- Attack Pattern
  - MISP
    ```json
    {
        "uuid": "c4e851fa-775f-11e7-8163-b774922098cd",
        "name": "Attack Pattern",
        "type": "mitre-attack-pattern",
        "description": "ATT&CK Tactic",
        "GalaxyCluster": [
            {
                "uuid": "dcaa092b-7de9-4a21-977f-7fcb77e89c48",
                "type": "mitre-attack-pattern",
                "value": "Access Token Manipulation - T1134",
                "description": "Windows uses access tokens to determine the ownership of a running process.",
                "meta": {
                    "external_id": [
                        "CAPEC-633"
                    ]
                }
            }
        ]
    }
    ```
  - STIX
    ```json
    {
        "type": "attack-pattern",
        "id": "attack-pattern--dcaa092b-7de9-4a21-977f-7fcb77e89c48",
        "created": "2020-25-10:16:22:00.000Z",
        "modified": "2020-25-10:16:22:00.000Z",
        "name": "Access Token Manipulation - T1134",
        "description": "ATT&CK Tactic | Windows uses access tokens to determine the ownership of a running process.",
        "kill_chain_phases": [
            {
                "kill_chain_name": "misp-category",
                "phase_name": "mitre-attack-pattern"
            }
        ],
        "labels": [
            "misp:name=\"Attack Pattern\""
        ],
        "external_references": [
            {
                "source_name": "capec",
                "external_id": "CAPEC-633"
            }
        ],
        "Attack Pattern": {
            "type": "attack-pattern",
            "id": "attack-pattern--dcaa092b-7de9-4a21-977f-7fcb77e89c48",
            "created": "2020-10-25T16:22:00.000Z",
            "modified": "2020-10-25T16:22:00.000Z",
            "name": "Access Token Manipulation - T1134",
            "description": "ATT&CK Tactic | Windows uses access tokens to determine the ownership of a running process.",
            "kill_chain_phases": [
                {
                    "kill_chain_name": "misp-category",
                    "phase_name": "mitre-attack-pattern"
                }
            ],
            "labels": [
                "misp:galaxy-name=\"Attack Pattern\"",
                "misp:galaxy-type=\"mitre-attack-pattern\""
            ],
            "external_references": [
                {
                    "source_name": "capec",
                    "external_id": "CAPEC-633"
                }
            ]
        }
    }
    ```

- Branded Vulnerability
  - MISP
    ```json
    {
        "uuid": "fda8c7c2-f45a-11e7-9713-e75dac0492df",
        "name": "Branded Vulnerability",
        "type": "branded-vulnerability",
        "description": "List of known vulnerabilities and exploits",
        "GalaxyCluster": [
            {
                "uuid": "a1640081-aa8d-4070-84b2-d23e2ae82799",
                "type": "branded-vulnerability",
                "value": "Ghost",
                "description": "The GHOST vulnerability is a serious weakness in the Linux glibc library.",
                "meta": {
                    "aliases": [
                        "CVE-2015-0235"
                    ]
                }
            }
        ]
    }
    ```
  - STIX
    ```json
    {
        "type": "vulnerability",
        "id": "vulnerability--a1640081-aa8d-4070-84b2-d23e2ae82799",
        "created": "2020-25-10:16:22:00.000Z",
        "modified": "2020-25-10:16:22:00.000Z",
        "name": "Ghost",
        "description": "List of known vulnerabilities and exploits | The GHOST vulnerability is a serious weakness in the Linux glibc library.",
        "labels": [
            "misp:name=\"Branded Vulnerability\""
        ],
        "external_references": [
            {
                "source_name": "cve",
                "external_id": "CVE-2015-0235"
            }
        ],
        "Vulnerability": {
            "type": "vulnerability",
            "id": "vulnerability--a1640081-aa8d-4070-84b2-d23e2ae82799",
            "created": "2020-10-25T16:22:00.000Z",
            "modified": "2020-10-25T16:22:00.000Z",
            "name": "Ghost",
            "description": "The GHOST vulnerability is a serious weakness in the Linux glibc library.",
            "labels": [
                "misp:galaxy-name=\"Branded Vulnerability\"",
                "misp:galaxy-type=\"branded-vulnerability\""
            ],
            "external_references": [
                {
                    "source_name": "cve",
                    "external_id": "CVE-2015-0235"
                }
            ]
        }
    }
    ```

- Course of Action
  - MISP
    ```json
    {
        "uuid": "6fcb4472-6de4-11e7-b5f7-37771619e14e",
        "name": "Course of Action",
        "type": "mitre-course-of-action",
        "description": "ATT&CK Mitigation",
        "GalaxyCluster": [
            {
                "uuid": "2497ac92-e751-4391-82c6-1b86e34d0294",
                "type": "mitre-course-of-action",
                "value": "Automated Exfiltration Mitigation - T1020",
                "description": "Identify unnecessary system utilities, scripts, or potentially malicious software that may be used to transfer data outside of a network",
                "meta": {
                    "external_id": "T1020",
                    "refs": [
                        "http://technet.microsoft.com/en-us/magazine/2008.06.srp.aspx",
                        "http://www.sans.org/reading-room/whitepapers/application/application-whitelisting-panacea-propaganda-33599",
                        "https://apps.nsa.gov/iaarchive/library/ia-guidance/tech-briefs/application-whitelisting-using-microsoft-applocker.cfm",
                        "https://attack.mitre.org/mitigations/T1020",
                        "https://blogs.jpcert.or.jp/en/2016/01/windows-commands-abused-by-attackers.html",
                        "https://technet.microsoft.com/en-us/library/ee791851.aspx"
                    ]
                }
            }
        ]
    }
    ```
  - STIX
    ```json
    {
        "type": "course-of-action",
        "id": "course-of-action--2497ac92-e751-4391-82c6-1b86e34d0294",
        "created": "2020-25-10:16:22:00.000Z",
        "modified": "2020-25-10:16:22:00.000Z",
        "name": "Automated Exfiltration Mitigation - T1020",
        "description": "ATT&CK Mitigation | Identify unnecessary system utilities, scripts, or potentially malicious software that may be used to transfer data outside of a network",
        "labels": [
            "misp:name=\"Course of Action\""
        ],
        "Course of Action": {
            "type": "course-of-action",
            "id": "course-of-action--2497ac92-e751-4391-82c6-1b86e34d0294",
            "created": "2020-10-25T16:22:00.000Z",
            "modified": "2020-10-25T16:22:00.000Z",
            "name": "Automated Exfiltration Mitigation - T1020",
            "description": "Identify unnecessary system utilities, scripts, or potentially malicious software that may be used to transfer data outside of a network",
            "labels": [
                "misp:galaxy-name=\"Course of Action\"",
                "misp:galaxy-type=\"mitre-course-of-action\""
            ],
            "external_references": [
                {
                    "source_name": "mitre-attack",
                    "external_id": "T1020"
                },
                {
                    "source_name": "url",
                    "url": "http://technet.microsoft.com/en-us/magazine/2008.06.srp.aspx"
                },
                {
                    "source_name": "url",
                    "url": "http://www.sans.org/reading-room/whitepapers/application/application-whitelisting-panacea-propaganda-33599"
                },
                {
                    "source_name": "url",
                    "url": "https://apps.nsa.gov/iaarchive/library/ia-guidance/tech-briefs/application-whitelisting-using-microsoft-applocker.cfm"
                },
                {
                    "source_name": "url",
                    "url": "https://attack.mitre.org/mitigations/T1020"
                },
                {
                    "source_name": "url",
                    "url": "https://blogs.jpcert.or.jp/en/2016/01/windows-commands-abused-by-attackers.html"
                },
                {
                    "source_name": "url",
                    "url": "https://technet.microsoft.com/en-us/library/ee791851.aspx"
                }
            ]
        }
    }
    ```

- Intrusion Set
  - MISP
    ```json
    {
        "uuid": "1023f364-7831-11e7-8318-43b5531983ab",
        "name": "Intrusion Set",
        "type": "mitre-intrusion-set",
        "description": "Name of ATT&CK Group",
        "GalaxyCluster": [
            {
                "uuid": "d6e88e18-81e8-4709-82d8-973095da1e70",
                "type": "mitre-intrusion-set",
                "value": "APT16 - G0023",
                "description": "APT16 is a China-based threat group that has launched spearphishing campaigns targeting Japanese and Taiwanese organizations.",
                "meta": {
                    "external_id": "G0023",
                    "refs": [
                        "https://attack.mitre.org/groups/G0023",
                        "https://www.fireeye.com/blog/threat-research/2015/12/the-eps-awakens-part-two.html"
                    ],
                    "synonyms": [
                        "APT16"
                    ]
                }
            }
        ]
    }
    ```
  - STIX
    ```json
    {
        "type": "intrusion-set",
        "id": "intrusion-set--d6e88e18-81e8-4709-82d8-973095da1e70",
        "created": "2020-10-25T16:22:00.000Z",
        "modified": "2020-10-25T16:22:00.000Z",
        "name": "APT16 - G0023",
        "description": "Name of ATT&CK Group | APT16 is a China-based threat group that has launched spearphishing campaigns targeting Japanese and Taiwanese organizations.",
        "aliases": [
            "APT16"
        ],
        "labels": [
            "misp:name=\"Intrusion Set\""
        ],
        "Intrusion Set": {
            "type": "intrusion-set",
            "id": "intrusion-set--d6e88e18-81e8-4709-82d8-973095da1e70",
            "created": "2020-10-25T16:22:00.000Z",
            "modified": "2020-10-25T16:22:00.000Z",
            "name": "APT16 - G0023",
            "description": "APT16 is a China-based threat group that has launched spearphishing campaigns targeting Japanese and Taiwanese organizations.",
            "aliases": [
                "APT16"
            ],
            "labels": [
                "misp:galaxy-name=\"Intrusion Set\"",
                "misp:galaxy-type=\"mitre-intrusion-set\""
            ],
            "external_references": [
                {
                    "source_name": "mitre-attack",
                    "external_id": "G0023"
                },
                {
                    "source_name": "url",
                    "url": "https://attack.mitre.org/groups/G0023"
                },
                {
                    "source_name": "url",
                    "url": "https://www.fireeye.com/blog/threat-research/2015/12/the-eps-awakens-part-two.html"
                }
            ]
        }
    }
    ```

- Malware
  - MISP
    ```json
    {
        "uuid": "d752161c-78f6-11e7-a0ea-bfa79b407ce4",
        "name": "Malware",
        "type": "mitre-malware",
        "description": "Name of ATT&CK software",
        "GalaxyCluster": [
            {
                "uuid": "b8eb28e4-48a6-40ae-951a-328714f75eda",
                "type": "mitre-malware",
                "value": "BISCUIT - S0017",
                "description": "BISCUIT is a backdoor that has been used by APT1 since as early as 2007.",
                "meta": {
                    "external_id": "S0017",
                    "mitre_platforms": [
                        "Windows"
                    ],
                    "refs": [
                        "https://attack.mitre.org/software/S0017",
                        "https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report-appendix.zip",
                        "https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"
                    ],
                    "synonyms": [
                        "BISCUIT"
                    ]
                }
            }
        ]
    }
    ```
  - STIX
    ```json
    {
        "type": "malware",
        "id": "malware--b8eb28e4-48a6-40ae-951a-328714f75eda",
        "created": "2020-25-10:16:22:00.000Z",
        "modified": "2020-25-10:16:22:00.000Z",
        "name": "BISCUIT - S0017",
        "description": "Name of ATT&CK software | BISCUIT is a backdoor that has been used by APT1 since as early as 2007.",
        "kill_chain_phases": [
            {
                "kill_chain_name": "misp-category",
                "phase_name": "mitre-malware"
            }
        ],
        "labels": [
            "misp:name=\"Malware\""
        ],
        "Malware": {
            "type": "malware",
            "id": "malware--b8eb28e4-48a6-40ae-951a-328714f75eda",
            "created": "2020-10-25T16:22:00.000Z",
            "modified": "2020-10-25T16:22:00.000Z",
            "name": "BISCUIT - S0017",
            "description": "BISCUIT is a backdoor that has been used by APT1 since as early as 2007.",
            "labels": [
                "misp:galaxy-name=\"Malware\"",
                "misp:galaxy-type=\"mitre-malware\""
            ],
            "external_references": [
                {
                    "source_name": "mitre-attack",
                    "external_id": "S0017"
                },
                {
                    "source_name": "url",
                    "url": "https://attack.mitre.org/software/S0017"
                },
                {
                    "source_name": "url",
                    "url": "https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report-appendix.zip"
                },
                {
                    "source_name": "url",
                    "url": "https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf"
                }
            ],
            "x_misp_mitre_platforms": [
                "Windows"
            ],
            "x_misp_synonyms": [
                "BISCUIT"
            ]
        }
    }
    ```

- Pre Attack - Attack Pattern
  - MISP
    ```json
    {
        "uuid": "c4e851fa-775f-11e7-8163-b774922098cd",
        "name": "Pre Attack - Attack Pattern",
        "type": "mitre-pre-attack-attack-pattern",
        "description": "ATT&CK Tactic",
        "GalaxyCluster": [
            {
                "uuid": "e042a41b-5ecf-4f3a-8f1f-1b528c534772",
                "type": "mitre-pre-attack-attack-pattern",
                "value": "Test malware in various execution environments - PRE-T1134",
                "description": "Malware may perform differently on different platforms and different operating systems.",
                "meta": {
                    "external_id": "PRE-T1134",
                    "kill_chain": [
                        "mitre-pre-attack:pre-attack:test-capabilities"
                    ],
                    "refs": [
                        "https://attack.mitre.org/pre-attack/index.php/Technique/PRE-T1134"
                    ]
                }
            }
        ]
    }
    ```
  - STIX
    ```json
    {
        "Attack Pattern": {
            "type": "attack-pattern",
            "id": "attack-pattern--e042a41b-5ecf-4f3a-8f1f-1b528c534772",
            "created": "2020-10-25T16:22:00.000Z",
            "modified": "2020-10-25T16:22:00.000Z",
            "name": "Test malware in various execution environments - PRE-T1134",
            "description": "Malware may perform differently on different platforms and different operating systems.",
            "kill_chain_phases": [
                {
                    "kill_chain_name": "mitre-pre-attack",
                    "phase_name": "test-capabilities"
                }
            ],
            "labels": [
                "misp:galaxy-name=\"Pre Attack - Attack Pattern\"",
                "misp:galaxy-type=\"mitre-pre-attack-attack-pattern\""
            ],
            "external_references": [
                {
                    "source_name": "mitre-pre-attack",
                    "external_id": "PRE-T1134"
                },
                {
                    "source_name": "url",
                    "url": "https://attack.mitre.org/pre-attack/index.php/Technique/PRE-T1134"
                }
            ]
        }
    }
    ```

- Threat Actor
  - MISP
    ```json
    {
        "uuid": "698774c7-8022-42c4-917f-8d6e4f06ada3",
        "name": "Threat Actor",
        "type": "threat-actor",
        "description": "Threat actors are characteristics of malicious actors.",
        "GalaxyCluster": [
            {
                "uuid": "11e17436-6ede-4733-8547-4ce0254ea19e",
                "type": "threat-actor",
                "value": "Cutting Kitten",
                "description": "These convincing profiles form a self-referenced network of seemingly established LinkedIn users.",
                "meta": {
                    "cfr-type-of-incident": [
                        "Denial of service"
                    ],
                    "synonyms": [
                        "Ghambar"
                    ]
                }
            }
        ]
    }
    ```
  - STIX
    ```json
    {
        "type": "threat-actor",
        "id": "threat-actor--11e17436-6ede-4733-8547-4ce0254ea19e",
        "created": "2020-25-10:16:22:00.000Z",
        "modified": "2020-25-10:16:22:00.000Z",
        "name": "Cutting Kitten",
        "description": "Threat actors are characteristics of malicious actors. | These convincing profiles form a self-referenced network of seemingly established LinkedIn users.",
        "aliases": [
            "Ghambar"
        ],
        "labels": [
            "misp:name=\"Threat Actor\""
        ],
        "Threat Actor": {
            "type": "threat-actor",
            "id": "threat-actor--11e17436-6ede-4733-8547-4ce0254ea19e",
            "created": "2020-10-25T16:22:00.000Z",
            "modified": "2020-10-25T16:22:00.000Z",
            "name": "Cutting Kitten",
            "description": "These convincing profiles form a self-referenced network of seemingly established LinkedIn users.",
            "aliases": [
                "Ghambar"
            ],
            "labels": [
                "misp:galaxy-name=\"Threat Actor\"",
                "misp:galaxy-type=\"threat-actor\""
            ],
            "x_misp_cfr_type_of_incident": [
                "Denial of service"
            ]
        }
    }
    ```

- Tool
  - MISP
    ```json
    {
        "uuid": "d5cbd1a2-78f6-11e7-a833-7b9bccca9649",
        "name": "Tool",
        "type": "mitre-tool",
        "description": "Name of ATT&CK software",
        "GalaxyCluster": [
            {
                "uuid": "bba595da-b73a-4354-aa6c-224d4de7cb4e",
                "type": "mitre-tool",
                "value": "cmd - S0106",
                "description": "cmd is the Windows command-line interpreter that can be used to interact with systems and execute other processes and utilities.",
                "meta": {
                    "external_id": "S0106",
                    "mitre_platforms": [
                        "Windows"
                    ],
                    "refs": [
                        "https://attack.mitre.org/software/S0106",
                        "https://technet.microsoft.com/en-us/library/bb490880.aspx",
                        "https://technet.microsoft.com/en-us/library/bb490886.aspx",
                        "https://technet.microsoft.com/en-us/library/cc755121.aspx",
                        "https://technet.microsoft.com/en-us/library/cc771049.aspx"
                    ],
                    "synonyms": [
                        "cmd",
                        "cmd.exe"
                    ]
                }
            }
        ]
    }
    ```
  - STIX
    ```json
    {
        "type": "tool",
        "id": "tool--bba595da-b73a-4354-aa6c-224d4de7cb4e",
        "created": "2020-25-10:16:22:00.000Z",
        "modified": "2020-25-10:16:22:00.000Z",
        "name": "cmd - S0106",
        "description": "Name of ATT&CK software | cmd is the Windows command-line interpreter that can be used to interact with systems and execute other processes and utilities.",
        "kill_chain_phases": [
            {
                "kill_chain_name": "misp-category",
                "phase_name": "mitre-tool"
            }
        ],
        "labels": [
            "misp:name=\"Tool\""
        ],
        "Tool": {
            "type": "tool",
            "id": "tool--bba595da-b73a-4354-aa6c-224d4de7cb4e",
            "created": "2020-10-25T16:22:00.000Z",
            "modified": "2020-10-25T16:22:00.000Z",
            "name": "cmd - S0106",
            "description": "cmd is the Windows command-line interpreter that can be used to interact with systems and execute other processes and utilities.",
            "labels": [
                "misp:galaxy-name=\"Tool\"",
                "misp:galaxy-type=\"mitre-tool\""
            ],
            "external_references": [
                {
                    "source_name": "mitre-attack",
                    "external_id": "S0106"
                },
                {
                    "source_name": "url",
                    "url": "https://attack.mitre.org/software/S0106"
                },
                {
                    "source_name": "url",
                    "url": "https://technet.microsoft.com/en-us/library/bb490880.aspx"
                },
                {
                    "source_name": "url",
                    "url": "https://technet.microsoft.com/en-us/library/bb490886.aspx"
                },
                {
                    "source_name": "url",
                    "url": "https://technet.microsoft.com/en-us/library/cc755121.aspx"
                },
                {
                    "source_name": "url",
                    "url": "https://technet.microsoft.com/en-us/library/cc771049.aspx"
                }
            ],
            "x_misp_mitre_platforms": [
                "Windows"
            ],
            "x_misp_synonyms": [
                "cmd",
                "cmd.exe"
            ]
        }
    }
    ```


## The other detailed mappings

For more detailed mappings, click on one of the link below:
- [Events export to STIX 2.0 mapping](misp_events_to_stix20.md)
- [Attributes export to STIX 2.0 mapping](misp_attributes_to_stix20.md)
- [Objects export to STIX 2.0 mapping](misp_objects_to_stix20.md)

([Go back to the main documentation](README.md))
