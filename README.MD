# `canvas_dump`

Python (3) scripts to dump all the files from all the courses you've ever been enrolled in using the Canvas LMS API.
You'll need to provide a token in a file called `token.txt`,
located in
the current working directory when the script runs.
You'll also need to specify an api endpoint in a file called `canvas_api_endpoint.txt`,
which should look something like `https://canvas.vt.edu/api/v1/`
You can generate one by navigating to
"Account" -> "Settings" -> "Approved Integrations"
and using the "New Access Token" button.
You'll also need `requests` installed.

Both the `courses` and `personal` scripts will dump to a folder called `output`,
which contains subfolders for all the classes (or `my files` in the case of `personal.py`).
The script will then replicate the file structure from the class into that folder,
including various metadata `json` files containing the raw API responses.

To get both course files and your own submissions/uploads, run both `courses.py` and `personal.py`
