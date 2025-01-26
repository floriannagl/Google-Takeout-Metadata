# Google-Takeout-Metadata
This code is only merging the 'phototimetaken' and 'creatontime'from the .json files to their image/video counterpart.

I recently changed cloud provider and got rid of google photos. When downloading all my pictures from google takeout 'takeout.google.com' all the pictures came seperate metadata. It was important for me to have the original 'phototimetaken' and 'creatontime'. Merging these files by hand would have taken too long so I wanted to do it with code.
Sice I have no experience in coding I used ChatGPT for 100% of the code.

What happens when you execute this script:
First it promts you to choose all of the zip files that you want to have merged. Then it prompts you to choose a output folder. In this folder 3 seperate folders will be created: 'metadata_only', 'combined_files', 'no_metadata'.
After selecting the output folder the zip files are being unziped. This may take some time and no status bar will show. As soon as the zip files are unziped the dates will be merged. In the terminal it will show every file it goes through.
When finished a pop up window will appear.
All the files who have a corresponding .json file will be in the 'combined_files' folder, all the metadata will be in the 'metadata_only' folder and all the files who dont have a corresponging .json file will be in the 'no_metadata' folder.
All the original zip files are still there.

I hope that his can help some people.
