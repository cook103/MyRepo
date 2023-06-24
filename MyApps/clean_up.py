import os
import glob
import shutil
import sys
from optparse import OptionParser
from datetime import datetime

"""
Author: Marcus Cook

Purpose: Automate cleaning up unmanagable files in
any given OS.

"""


class CleanUp:
    def get_extension_type(self: None) -> list:
        """Find all extension types"""
        self.ext_type = set(x.split(".")[1] for x in glob.glob("*") if "." in x)
        return self.ext_type

    def sort_by_extension(self, dir: str) -> None:
        """Make a unique folder for each possible extension, and group"""

        file_count = 0

        os.chdir(dir)

        for ext in self.get_extension_type():
            for file in glob.glob("*"):
                folder_name = f"AllFiles{ext.title()}"

                if not os.path.exists(folder_name):
                    try:
                        os.mkdir(folder_name)
                    except Exception as e:
                        raise Exception(e.args)

                if file.endswith(ext):
                    try:
                        shutil.move(file, folder_name)
                    except Exception as e:
                        raise Exception(e.args)

                file_count += 1

        if file_count < 1:
            print("no lingering files exist")
        else:
            print(f"{file_count} files moved!")

    def sort_by_date(self, dir: str) -> None:
        """Make unique folder for file date creation Year/Month, and group"""
        file_count = 0

        os.chdir(dir)

        for file in glob.glob("*"):
            ct = os.path.getctime(file)

            created_time = str(datetime.fromtimestamp(ct)).split()[0][:-3]

            if not os.path.exists(created_time):
                try:
                    os.mkdir(created_time)
                except Exception as e:
                    raise Exception(e.args)

            try:
                shutil.move(file, created_time)
            except Exception as e:
                raise Exception(e.args)

            file_count += 1

        if file_count < 1:
            print("no lingering files exist")
        else:
            print(f"{file_count} files moved!")


def parse_command_line():
    parser = OptionParser()

    parser.add_option(
        "-d",
        "--date",
        dest="do_date",
        action="store_true",
        help="organize by date created",
    )

    parser.add_option(
        "-e",
        "--extension",
        dest="do_extension",
        action="store_true",
        help="organize by extension type",
    )

    (options, args) = parser.parse_args()

    clean = CleanUp()

    if options.do_date:
        print("sorting by date created:")
        print("-" * 30)

        clean.sort_by_date(sys.argv[1])

    if options.do_extension:
        print("sorting by extension type:")
        print("-" * 30)
        clean.sort_by_extension(sys.argv[1])


def main():
    arg_size = len(sys.argv)
    if arg_size <= 1:
        raise Exception(
            "Need one directory to clean, please pass it into the command line"
        )
    elif arg_size > 3:
        raise Exception(
            "Exactly three argument needed: file, directory, parser, for help use --help"
        )

    try:
        os.chdir(sys.argv[1])
    except FileNotFoundError:
        raise

    parse_command_line()


if __name__ == "__main__":
    main()
