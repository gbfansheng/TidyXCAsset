import os
import re

# Define the exclude list file (one directory per line)
exclude_list = "TidyPNG_Exclude.txt"

# Read the exclude list into a set
with open(exclude_list, "r") as f:
    exclude_set = set([line.strip() for line in f])

# Find all PNG files in the current directory and its subdirectories, excluding directories in the exclude list 
exceptFileList = []
for root, dirs, files in os.walk("/path/to/your/project", topdown=True):
    # Remove excluded directories from the search
    dirs[:] = [d for d in dirs if os.path.join(root, d) not in exclude_set]

    for filename in files:
        if not filename.endswith(".png"):
            continue
        # Check if the parent directory is in the exclude list
        if os.path.basename(root) in exclude_set:
            continue # Skip this file if the directory is in the exclude list
        
        fPath = os.path.join(root, filename)
        skip = False
        for line in exclude_set:
            if line in fPath:
                skip = True
                break;
        # print("!!!skip path:" + fPath)
        if "xcasset" not in fPath:
            skip = True
        if skip :
            continue
        

        # Get the name of the parent directory and remove the .xcasset suffix
        parent = os.path.basename(root).replace(".imageset", "")

        # Extract the prefix of the PNG file using a regular expression (without the @2x/@3x suffix)
        match = re.match(r"^(.+)/([^/@]+)@[0-9]+x\.png$", filename)
        if match:
            prefix = match.group(2)
        else:
            prefix = os.path.splitext(filename)[0]

        # Remove the @2x/@3x suffix from the prefix (if it exists)
        # prefix = prefix.replace("@2x", "").replace("@3x", "")
    
        prefix2x = parent + "@2x"
        prefix3x = parent + "@3x"
        # Compare the prefix of the PNG file to the name of the parent directory
        if prefix != prefix2x and prefix != prefix3x:
            # Generate the new filename using the correct prefix
            new_filename = ""
            newPrefix = ""
            if "@2x" in prefix:
                newPrefix = prefix2x
                new_filename = os.path.join(root, prefix2x + ".png")
            if "@3x" in prefix:
                newPrefix = prefix3x
                new_filename = os.path.join(root, prefix3x + ".png")
            if newPrefix == "" :
                exceptFileList.append(os.path.join(root, filename))
                break
            # Rename the file
            os.rename(os.path.join(root, filename), new_filename)
            print(f"Renamed\n{os.path.join(root, filename)}\n{new_filename}")
            contentJsonPath = os.path.join(root, "Contents.json")
            retLines = []
            with open(contentJsonPath, 'r') as contentJson:
                lines = contentJson.readlines()
            for line in lines:
                if prefix in line:
                    # print(line)
                    # print(newPrefix)
                    retLines.append(line.replace(prefix, newPrefix))
                else :
                    retLines.append(line)
            with open(contentJsonPath, 'w') as contentJson:
                contentJson.writelines(retLines)
for file in exceptFileList:
    print("exception file 请手动修改这些文件: "+ file)

