import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(
            os.path.join(working_dir_abs, directory)
        )

        is_valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        if not is_valid_target_dir:
            return (
                f'Error: Cannot list "{directory}" as it is outside '
                f'the permitted working directory'
            )

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        files_info: list[str] = []

        for file_name in os.listdir(target_dir):
            file_path = os.path.join(target_dir, file_name)
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)

            files_info.append(
                f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}"
            )

        return "\n".join(files_info)

    except Exception as exception:  # noqa: BLE001
        return f"Error: {exception}"
