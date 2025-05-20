import re
import yaml
import subprocess
import sys
from pathlib import Path
from generated_file_contents import GeneratedFileContents


def parse_openapi_yaml(path):
    with open(path, 'r', encoding="utf-8") as f:
        return yaml.safe_load(f)


def generate_config_properties(spec, auth_token, timeout, env, log_level):
    base_url = spec.get("servers", [{}])[0].get("url", "")
    content = GeneratedFileContents.config_properties(base_url, auth_token, timeout, env, log_level)
    Path("config").mkdir(parents=True, exist_ok=True)
    Path("config/config.properties").write_text(content, encoding="utf-8")
    print("✅ Generated config/config.properties")


def generate_config_reader():
    content = GeneratedFileContents.config_reader()
    Path("config/config_reader.py").write_text(content, encoding="utf-8")
    print("✅ Generated config/config_reader.py")


def generate_utils():
    content = GeneratedFileContents.utils()
    Path("core").mkdir(parents=True, exist_ok=True)
    Path("core/utils.py").write_text(content, encoding="utf-8")
    print("✅ Generated core/utils.py")


def generate_requirements_file():
    content = GeneratedFileContents.requirements()
    Path("requirements.txt").write_text(content, encoding="utf-8")
    print("✅ Generated requirements.txt")


def install_requirements():
    confirm = input("📦 Do you want to install required packages from requirements.txt? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("❌ Skipping package installation.")
        return

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All required modules installed.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")


def create_init_files():
    for directory in ["config", "core"]:
        Path(directory).mkdir(exist_ok=True)
        init_path = Path(directory) / "__init__.py"
        if not init_path.exists():
            init_path.touch()
            print(f"✅ Created {init_path}")


def generate_readme(feature_title, yaml_path, base_url):
    template_path = Path("template_readme.txt")
    if not template_path.exists():
        print("❌ template_readme.txt not found. README not generated.")
        return

    content = template_path.read_text(encoding="utf-8")

    content = content.format(
        feature_title=feature_title,
        yaml_path=yaml_path,
        base_url=base_url,
        yaml_file_name=Path(yaml_path).name
    )

    Path("README.md").write_text(content, encoding="utf-8")
    print("✅ Generated README.md from template")


def generate_bdd_files(feature_title):
    # Sanitize feature title to use as filename
    safe_filename = re.sub(r'\W+', '_', feature_title.strip())
    feature_filename = f"{safe_filename}.feature"

    # Define paths
    feature_dir = Path("features/steps")
    feature_dir.mkdir(parents=True, exist_ok=True)

    feature_path = Path("features") / feature_filename
    steps_path = feature_dir / "api_steps.py"

    # Write feature and step definition files
    feature_path.write_text(GeneratedFileContents.sample_feature_file(), encoding="utf-8")
    steps_path.write_text(GeneratedFileContents.sample_step_definitions(), encoding="utf-8")

    print(f"✅ BDD files generated: features/{feature_filename}, features/steps/api_steps.py")


class FrameworkGenerator:

    def __init__(self, openapi_file, feature_title):
        self.openapi_file = openapi_file
        self.feature_title = feature_title

    def generate_feature_file(self):
        with open(self.openapi_file, 'r', encoding='utf-8') as f:
            spec = yaml.safe_load(f)

        paths = spec.get("paths", {})
        feature_lines = [f"Feature: {self.feature_title}\n"]

        for path, methods in paths.items():
            for method, details in methods.items():
                scenario = self.create_scenario_from_path(method, path, details)
                feature_lines.append(scenario)
                feature_lines.append("")  # blank line between scenarios

        # Convert feature title to safe filename
        safe_title = re.sub(r'\W+', '_', self.feature_title.strip())
        feature_file = Path(f"features/{safe_title}.feature")
        Path("features").mkdir(exist_ok=True)
        feature_file.write_text("\n".join(feature_lines), encoding="utf-8")
        print(f"✅ Feature file generated: features/{feature_file.name}")

    def create_scenario_from_path(self, method, path, details):
        method = method.upper()
        summary = details.get('summary', f"{method} {path}")
        scenario_name = re.sub(r'\W+', ' ', summary).strip()

        steps = [
            f"  Scenario: {scenario_name}",
            f'    Given I have the API endpoint "{path}"',
        ]

        # Add query parameters if available
        parameters = details.get('parameters', [])
        for param in parameters:
            if param.get("in") == "query":
                key = param["name"]
                default = param.get("schema", {}).get("default", "value")
                steps.append(f'    And I set query parameter "{key}" to "{default}"')

        # Handle request body if it's a POST/PUT/PATCH method
        if method in ['POST', 'PUT', 'PATCH']:
            steps.append(f'    And I send the request body with required data')

        # Sending the request
        steps.append(f"    When I send a {method} request")
        steps.append("    Then the response code should be 200")

        return "\n".join(steps)

    def generate_step_definitions(self):
        # Get the reusable step definitions from GeneratedFileContents
        step_defs = GeneratedFileContents.sample_step_definitions()

        # Write the step definitions to api_steps.py
        step_def_file = Path("features/steps/api_steps.py")
        Path("features/steps").mkdir(parents=True, exist_ok=True)
        step_def_file.write_text(step_defs, encoding="utf-8")
        print(f"✅ Step definitions generated: features/steps/api_steps.py")

    def generate_all_files(self):
        # Generate feature file
        self.generate_feature_file()

        # Generate step definitions
        self.generate_step_definitions()