import os
import glob
import shutil
import sys

"""
Author: Marcus Cook

Purpose: Automate cleaning up unmanageble files in
any given OS.

"""


class CleanUp:
    def get_extension_type(self: None) -> list:
        """Find all extension types in any directory"""
        self.ext_type = set(x.split(".")[1] for x in glob.glob("*") if "." in x)
        return self.ext_type

    def sort_by_extension(self, dirs: list) -> None:
        """Make a unique folder for each possible extension, and group"""

        file_count = 0

        for dir in dirs:
            os.chdir(dir)
            for ext in self.get_extension_type():
                for item in glob.glob(f"*{ext}"):
                    folder_name = f"AllFiles{ext.title()}"

                    if not os.path.exists(folder_name):
                        os.mkdir(folder_name)

                    shutil.move(item, folder_name)

                    file_count += 1

        if file_count < 1:
            print("no lingering files exist")
        else:
            print(f"{file_count} files moved!")


def main():
    arg_size = len(sys.argv)
    if arg_size < 2:
        raise Exception(
            "Need at least one directory to clean, please pass it into the command line"
        )

    for dir in sys.argv[1:]:
        try:
            os.chdir(dir)
        except FileNotFoundError:
            raise

    clean = CleanUp()
    clean.sort_by_extension(sys.argv[1:])


if __name__ == "__main__":
    main()
