#!/usr/bin/env python
import os, sys

import dotenv
dotenv.read_dotenv()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "election_api.settings")
    # Add the apps/ directory to the system path
    sys.path.append("apps")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)