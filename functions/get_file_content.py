import os

import config


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        is_valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not is_valid_target_file:
            return (
                f'Error: Cannot read "{file_path}" as it is outside '
                f'the permitted working directory'
            )

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as file:
            file_content = file.read(config.MAX_CHARS)
            if file.read(1):
                file_content += (
                    f'[...File "{file_path}" truncated at '
                    f'{config.MAX_CHARS} characters]'
                )

        return file_content

    except Exception as exception:  # noqa: BLE001
        return f"Error: {exception}"
