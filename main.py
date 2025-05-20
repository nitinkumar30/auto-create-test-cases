import os
# import sys
# from pathlib import Path
from framework_generator import *
from framework_generator import FrameworkGenerator
from generated_file_contents import generate_post_put_payload


def main():
    # Get user inputs
    yaml_path = input("📄 Enter path to OpenAPI YAML (e.g. openapi/petstore.yaml): ").strip()
    feature_title = input("📝 Enter feature title (e.g. Petstore API Testing): ").strip()

    # Parse OpenAPI spec
    spec = parse_openapi_yaml(yaml_path)
    base_url = spec.get("servers", [{}])[0].get("url", "")

    print(f"🌐 Detected base URL: {base_url}")
    use_auth = input("🔐 Does this API require an auth token? (y/n): ").strip().lower() == 'y'
    auth_token = input("🔑 Enter the auth token (leave blank to skip): ").strip() if use_auth else ""
    timeout = input("⏱️ Enter request timeout in seconds (default 10): ").strip() or "10"
    env = input("🌍 Enter environment label (e.g. dev, qa, prod) [default=dev]: ").strip() or "dev"
    log_level = input("📢 Logging level (DEBUG, INFO, WARNING) [default=INFO]: ").strip().upper() or "INFO"

    # Generate framework files
    generate_config_properties(spec, auth_token, timeout, env, log_level)
    generate_config_reader()
    generate_utils()
    create_init_files()
    generate_requirements_file()
    install_requirements()
    generate_bdd_files(feature_title.strip())
    generate_readme(feature_title, yaml_path, base_url)

    print("✅ Framework generation complete. Now, you can generate the README manually using the "
          "original method.")
    print(f"📁 Feature: '{feature_title}'")
    print("🧰 Configuration, utilities, and dependencies are ready.\n")
    if not os.path.exists(yaml_path):
        print(f"❌ Error: The file '{yaml_path}' does not exist.")
        return

    # Generate the framework (feature file and step definitions)
    framework_generator = FrameworkGenerator(yaml_path, feature_title)
    framework_generator.generate_all_files()

    def prompt_test_runner():
        print("\n🧪 Choose how you'd like to run the test:")
        print("1. Behave (default)")
        print("2. Pytest")
        print("3. Skip test execution")

        choice = input("Enter choice [1/2/3]: ").strip()
        return choice or "1"

    choice = prompt_test_runner()

    if choice == "1":
        try:
            # print("Generating JSON payload for POST/PUT requests...")
            # payload = generate_post_put_payload()
            # print("Payload generated and saved to post_put_payload.json:")
            # print(payload)
            subprocess.run(["behave"], check=True)
        except Exception as e:
            print(f"❌ Failed to run with Behave: {e}")

    elif choice == "2":
        try:
            # print("Generating JSON payload for POST/PUT requests...")
            # payload = generate_post_put_payload()
            # print("Payload generated and saved to post_put_payload.json:")
            # print(payload)
            subprocess.run(["pytest"], check=True)
        except Exception as e:
            print(f"❌ Failed to run with Pytest: {e}")

    else:
        print("🚫 Skipping test execution.")


if __name__ == "__main__":
    main()
