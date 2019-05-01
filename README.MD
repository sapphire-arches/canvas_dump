# `canvas_dump`

A python script to dump all the files from all the courses you've ever been enrolled in using the Canvas LMS API.
You'll need to provide a token in a file called `token.txt`,
located in
the current working directory when the script runs.
You can generate one by navigating to
"Account" -> "Settings" -> "Approved Integrations"
and using the "New Access Token" button.

The script will dump to a folder called `output`,
which contains subfolders for all the classes.
The script will then replicate the file structure from the class into that folder,
including various metadata `json` files containing the raw API responses.
It does not dump files from "My Files" at this time, though that is planned
