#!/usr/bin/env python
"""
Filename    : main.py
Author      : Viktor
Porject     : Audit docker-compose best practises
Description : Main module to audit docker compose best practises.
"""

import os
import sys
import yaml
from audit_compose_bp import AuditComposeBestPractises

def audit_all_yaml_files_in_the_current_directory(
    auditer: AuditComposeBestPractises) -> None:
    """Audit all the yaml files in the current directory"""
    yaml_file_found = 0
    failed_audit = 0

    for file in os.listdir('.'):
        if file.endswith((".yml", ".yaml")):
            yaml_file_found += 1
            with open(file, 'r', encoding = "utf-8") as open_file:
                try:
                    compose_data = yaml.safe_load(open_file)
                except yaml.YAMLError as error:
                    print(f"❌ Error parsing {open_file}: {error}")
            failed_audit += auditer.check_docker_compose(file, compose_data)
    if yaml_file_found == 0:
        print("❌ any yaml file could'nt be found in the current directory!")
        sys.exit(1)
    if yaml_file_found == failed_audit:
        print("❌ The yaml file(s) could'nt be audited!")
        sys.exit(1)

def print_audit_result(auditer: AuditComposeBestPractises) -> None:
    """Print audit result"""
    errors = auditer.get_errors()

    if errors:
        print("🚨 Best Practice Violations Found:")
        for error in errors:
            print(error)
        auditer.print_rating()
        sys.exit(1)
    else:
        print("✅ All checks passed! Your compose file follows best practices.")
        auditer.print_rating()
        sys.exit(0)

if __name__ == "__main__":
    auditer_object = AuditComposeBestPractises()

    audit_all_yaml_files_in_the_current_directory(auditer_object)
    print_audit_result(auditer_object)
