import os
import sys
import venv
import platform


def in_venv() -> bool:
    return sys.prefix != getattr(sys, "base_prefix", sys.prefix)


def create_virtualenv(env_name: str = "venv"):
    print(f"\nCreating virtual environment: {env_name}")
    venv.create(env_name, with_pip=True)

    script_path = get_activation_script_path(env_name)
    activation = activation_script(script_path)

    print("\nVirtual environment created successfully!")
    print("To activate it, run:\n")

    print(activation, "\n")


def activation_script(script_path: str):
    if platform.system() == "Windows":
        return f"    {script_path}"

    return f"    source {script_path}"


def get_activation_script_path(env_name: str):
    # Linux activation (idk MacOS)
    if platform.system() != "Windows":
        return os.path.join(env_name, "bin", "activate")

    # Windows activation:
    # PowerShell detection
    ps_process = (
        os.environ.get("PSMODULEPATH")
        or "powershell" in os.environ.get("SHELL", "").lower()
    )

    if ps_process:
        return os.path.join(".", env_name, "Scripts", "Activate.ps1")

    return os.path.join(".", env_name, "Scripts", "activate")


if __name__ == "__main__":
    if in_venv():
        print("\n ⚠️  A virtual environment is already active. ⚠️\n")
        print("   Current environment:", sys.prefix)
        print("   Aborting script to avoid nesting environments.\n")
        sys.exit(1)

    env_name = sys.argv[1] if len(sys.argv) > 1 else None
    if env_name is not None:
        create_virtualenv(env_name)
    else:
        create_virtualenv()
