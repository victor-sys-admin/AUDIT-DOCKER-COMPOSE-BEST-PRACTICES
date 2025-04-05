#!/usr/bin/env python
"""
Filename    : audit_compose_bp.py
Author      : Viktor
Porject     : Audit docker-compose best practises
Description : Module to audit docker-compose best practises.
"""

class AuditComposeBestPractises():
    """Class to handle the audit of compose files best practises"""
    def __init__(self) -> None:
        """Init of the class"""
        self.checks_succed = 0
        self.service_name = ''
        self.service = ''
        self.errors = []
        self.checks = 0
        self.file = ''

    def print_rating(self) -> None:
        """Print rating and final result"""
        result_percent = round((self.checks_succed/self.checks)*100, 2)
        tabulated = '' if self.errors else '\t'
        result_raw = f"{self.checks_succed}/{self.checks}"

        print(f"{tabulated}Made {self.checks} checks.\n" \
            f"{tabulated}Final result: {result_raw}\n" \
            f"{tabulated}Best practices coverage : {result_percent}%"
        )

    def __register_error(self, error_string: str, first_error: bool) -> None:
        """Register error in the error buffer"""
        start_separator = "################################# START WARNING " \
            "#################################"

        print(f"\t❌ {error_string}")
        if first_error:
            self.errors.append(start_separator)
        self.errors.append(f"❌ {self.file} -- {self.service_name}: " \
            f"{error_string}"
        )

    def __register_recommendation(self, recommendation: str) -> None:
        """Register recommendation in the error buffer"""
        end_separator = "################################## END WARNING " \
            "##################################\n"

        self.errors.append(recommendation)
        self.errors.append(end_separator)

    def __check_image_tag(self) -> int:
        """Check if image get a version tag"""
        err_str = "Image must have a specific tag, not 'latest' or missing."
        recommendation = "\n💡 Avoids using latest tags, which can " \
            "introduce unintended changes or vulnerabilities and ensures " \
            "controlled updates and predictable deployments."
        image = self.service.get("image", '')
        self.checks += 1

        if not image or ':' not in image:
            self.__register_error(err_str, True)
            self.__register_recommendation(recommendation)
        else:
            print("\t⭐ Image is tag")
            self.checks_succed += 1
        return 0

    def __check_required_fields(self, required_fields: dict,
        recommendation: str, equal=(None, None)) -> int:
        """Check if requiered fields are present"""
        error_found = 0

        for field, value in required_fields.items():
            error_string = f"Missing {field} setting."
            self.checks += 1
            if value in equal:
                self.__register_error(error_string, (error_found == 0))
                error_found = 1
            else:
                print(f"\t⭐ {field} is set.")
                self.checks_succed += 1
        if error_found:
            self.__register_recommendation(recommendation)
        return error_found

    def __check_deploy_section(self) -> int:
        """Check deploy section"""
        deploy = self.service.get("deploy", {})
        resources = deploy.get("resources", {})
        limits = resources.get("limits", {})
        reservations = resources.get("reservations", {})
        required_fields = {
            "deploy.resources.reservations.memory": reservations.get("memory"),
            "deploy.resources.reservations.cpus": reservations.get("cpus"),
            "deploy.resources.limits.memory": limits.get("memory"),
            "deploy.resources.limits.cpus": limits.get("cpus")
        }
        recommendation = "\n💡 Restricts CPU and memory usage to prevent " \
            "Denial of Service (DoS) attacks and ensures fair resource " \
            "allocation among containers."

        self.__check_required_fields(required_fields, recommendation)
        return 0

    def __check_healthcheck_section(self) -> int:
        """Check healthcheck section"""
        healthcheck = self.service.get("healthcheck", {})
        required_fields = {
            "healthcheck.start_period": healthcheck.get("start_period"),
            "healthcheck.interval": healthcheck.get("interval"),
            "healthcheck.timeout": healthcheck.get("timeout"),
            "healthcheck.retries": healthcheck.get("retries"),
            "healthcheck.test": healthcheck.get("test")
        }
        recommendation = "\n💡 Monitors container health, restarts " \
            "unhealthy containers. It helps detecting running faulty or " \
            "compromised services."

        self.__check_required_fields(required_fields, recommendation)
        return 0

    def __check_logging_section(self) -> int:
        """Check logging section"""
        container_logging = self.service.get("logging", {})
        logging_options = container_logging.get("options", {})
        required_fields = {
            "logging.options.max-size": logging_options.get("max-size"),
            "logging.options.max-file": logging_options.get("max-file")
        }
        recommendation = "\n💡 Prevents excessive logging from consuming " \
            "disk space."

        self.__check_required_fields(required_fields, recommendation)
        return 0

    def __check_security_opt(self) -> int:
        """Check security_opt presence"""
        required_fields = { "security_opt": self.service.get("security_opt") }
        recommendation = "\n💡 Restricts container access to only required " \
            "system resources."

        self.__check_required_fields(required_fields, recommendation)
        return 0

    def __check_networks(self) -> int:
        """Check networks hardening"""
        required_fields = { "networks": self.service.get("networks") }
        recommendation = "\n💡 Use dedicated network or disable ICC for the " \
            "default network to prevents unauthorized communication between " \
            "containers. It will limits lateral movement in case of a breach."

        self.__check_required_fields(required_fields, recommendation)
        return 0

    def __check_capabilities(self) -> int:
        """Check capabilities"""
        required_fields = { "cap_drop": self.service.get("cap_drop") }
        recommendation = "\n💡 cap_drop: ALL removes all Linux capabilities, " \
            "minimizing potential attack vectors. Use cap_add if " \
            "capabilit(y/ies) is/are needed."

        self.__check_required_fields(required_fields, recommendation)
        return 0

    def __check_restart_policy(self) -> int:
        """Check restart policy"""
        required_fields = { "restart": self.service.get("restart") }
        recommendation = "\n💡  defines how and when a container should be " \
            "restarted. It improve availability." \

        self.__check_required_fields(required_fields, recommendation)
        return 0

    def __check_volumes(self) -> int:
        """Check volumes"""
        recommendation = "\n💡 Mounts configurations as read-only (:ro). " \
            "It will prevents unauthorized changes to important files."
        volumes = self.service.get("volumes", [])
        error_found = 0

        for volume in volumes:
            self.checks += 1
            if (":ro" not in volume) and (":rw" not in volume):
                error_string = (f"Volume '{volume}' should have a mount option " +
                    "(:ro, :rw).")
                self.__register_error(error_string, (error_found == 0))
                error_found = 1
            else:
                print(f"\t⭐ Volume '{volume}' have a mount option")
                self.checks_succed += 1
        if error_found:
            self.__register_recommendation(recommendation)
        return 0

    def __check_privileged_mode(self) -> int:
        """Check privileged mode"""
        required_fields = { "privileged": self.service.get("privileged") }
        recommendation = "\n💡 Prevents the container from having full " \
            "access to the host system. Reduces the risk of host compromise " \
            "in case of a container breakout."
        error_if = (True, None)

        self.__check_required_fields(required_fields, recommendation, error_if)
        return 0

    def __check_read_only_filesystem(self) -> int:
        """Check read-only filesystem"""
        error_if = (False, None)
        required_fields = { "read_only": self.service.get("read_only") }
        recommendation = "\n💡 Prevents unauthorized file modifications " \
            "within the container. Reduces the attack surface by making the " \
            "filesystem immutable."

        self.__check_required_fields(required_fields, recommendation, error_if)
        return 0

    def __check_user(self) -> int:
        """Check user"""
        error_if = ("0", None)
        required_fields = { "user": self.service.get("user") }
        recommendation = "\n💡 Runs the container as a non-root user. " \
            "Prevents privilege escalation attacks in case of a container " \
            "compromise."

        self.__check_required_fields(required_fields, recommendation, error_if)
        return 0

    def check_docker_compose(self, file_path: str, compose_data: dict) -> int:
        """Audit the compse file"""
        if compose_data is None or "services" not in compose_data:
            print("❌ No 'services' section found in the compose file " \
                f"'{file_path}'.\n"
            )
            return 1
        self.file = file_path
        for self.service_name, self.service in compose_data["services"].items():
            print(f"🔍 Checking file: {file_path}\n" \
                f"service: {self.service_name}"
            )
            self.__check_read_only_filesystem()
            self.__check_healthcheck_section()
            self.__check_privileged_mode()
            self.__check_logging_section()
            self.__check_deploy_section()
            self.__check_restart_policy()
            self.__check_security_opt()
            self.__check_capabilities()
            self.__check_image_tag()
            self.__check_networks()
            self.__check_volumes()
            self.__check_user()
            print()
        return 0

    def get_errors(self):
        """Return errors list"""
        return self.errors
