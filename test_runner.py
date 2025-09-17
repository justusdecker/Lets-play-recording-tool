from pycode_info import analyze_all_files_in_workspace
from pycode_info import print_language_summary
from pycode_info import print_flake8_report
print_language_summary()

from bin.data_access import SQLAccess
SQLAccess.create_from_csv()