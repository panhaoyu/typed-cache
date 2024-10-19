import subprocess

from prompt_toolkit.shortcuts import radiolist_dialog


def run_command(command):
    """运行命令并处理错误"""
    result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def process_release(version_type="patch"):
    """处理版本更新、发布、提交和推送的核心逻辑"""
    print(f"Updating project version ({version_type})...")
    run_command(f"poetry version {version_type}")

    version = run_command("poetry version -s")
    print(f"New version: {version}")

    print("Publishing to Python package index...")
    run_command("poetry publish --build")

    print("Adding changes to git...")
    run_command("git add .")

    print(f"Committing changes with message: Release version {version}")
    run_command(f'git commit -m "Release version {version}"')

    print("Pushing changes to remote repository...")
    run_command("git push origin main")

    print("All steps completed successfully.")


def main():
    # 使用 prompt-toolkit 提供一个交互式选择菜单
    version_type = radiolist_dialog(
        title="Select Version Type",
        text="Choose the version type to bump:",
        values=[
            ("patch", "Patch - Small bug fixes"),
            ("minor", "Minor - New features, but backward compatible"),
            ("major", "Major - Breaking changes"),
        ]
    ).run()

    if not version_type:
        print("No version type selected. Exiting.")
        return

    try:
        process_release(version_type)  # 调用处理函数，并传入版本类型
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing command: {e.cmd}")
        print(f"Error message: {e.stderr}")
        print("Terminating script due to error.")
        exit(1)


if __name__ == "__main__":
    main()
