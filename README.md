Google Takeout Metadata Date

This script is designed to merge the 'phototimetaken' and 'creationtime' fields from .json metadata files with their corresponding image or video files. It is important to note that this script only adds the 'phototimetaken' and 'creationtime' fields from the metadata and does not modify any other attributes of the files.

I recently changed cloud providers and decided to stop using Google Photos. When I downloaded all my pictures through Google Takeout (takeout.google.com), I noticed that the photos and videos were separated from their metadata. It was important for me to retain the original 'phototimetaken' and 'creationtime' values. Manually merging these files would have taken far too long, so I decided to automate the process. Since I have no prior coding experience, I relied entirely on ChatGPT to generate the script.

When you run the script, it first prompts you to select the .zip files from Google Takeout that you want to process. Next, it asks you to choose an output folder. Within this folder, the script creates three separate subfolders: metadata_only, combined_files, and no_metadata. Once the output folder is selected, the script unzips the chosen .zip files. This step may take some time, and no progress bar will be displayed. After the files are unzipped, the metadata merging process begins, and the terminal will display the name of each file as it is processed. When the process is complete, a pop-up window will appear to indicate that the operation is finished.

The files with corresponding .json metadata are placed in the combined_files folder. Metadata files themselves are stored in the metadata_only folder, and files without matching metadata are placed in the no_metadata folder. The original .zip files remain untouched and exactly as they were.

I hope this script can be helpful to others. If it does help you or if you have any questions, feel free to email me at my public GitHub email address: githubpublic.outpost377@passmail.net.
