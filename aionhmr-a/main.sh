#!/bin/bash

# Check if the root directory argument is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <DATA_ROOT>"
    echo "Example: ./main.sh /path/to/project_data"
    exit 1
fi

# Set DATA_ROOT from argument and derive IMG_DIR
DATA_ROOT="$1"
IMG_DIR="$DATA_ROOT/images"

# Ensure the images directory exists
if [ ! -d "$IMG_DIR" ]; then
    echo "Error: Directory $IMG_DIR does not exist."
    exit 1
fi

process_image() {
  local file="$1"
  local filename=$(basename "$file")
  local filename_no_ext="${filename%.*}"

  # Create subfolder for image-to-video simulation
  mkdir -p "$IMG_DIR/$filename_no_ext"
  
  echo "Processing image: $filename"

  # Copy the single image 9 times to satisfy sequence requirements
  for i in {1..9}; do
    padded_i=$(printf "%06d" "$i") 
    cp "$file" "$IMG_DIR/$filename_no_ext/$padded_i.jpg"
  done

  # Run the python command
  local run_opt_command="python src/run_opt.py data=video data.seq=\"$filename_no_ext\" data.root=\"$DATA_ROOT\" run_opt=True run_vis=True"
  echo "Executing: $run_opt_command"
  
  eval "$run_opt_command"
  
  if [ $? -ne 0 ]; then
    echo "Error: src/run_opt.py failed for $filename"
    rm -rf "$IMG_DIR/$filename_no_ext"
    return 1
  fi

  # Cleanup temporary image sequence
  rm -rf "$IMG_DIR/$filename_no_ext"
  return 0
}

# Main loop: Iterate through files in the images directory
for file in "$IMG_DIR"/*; do
  if [ -f "$file" ]; then
    filename=$(basename "$file")
    extension="${filename##*.}"

    case "${extension,,}" in
      jpg|jpeg)
        process_image "$file"
        ;;
        
      png)
        echo "Converting PNG to JPG using Python: $file"
  
        python src/util/png2jpg.py "$file"
        
        if [ $? -ne 0 ]; then
          echo "Error converting $file"
          continue
        fi
        
        jpg_file="${file%.*}.jpg"
        process_image "$jpg_file"
        ;;
        
      mp4|avi|mov|mkv)
        FOLDER_NAME="${filename%.*}"
        CMD="python src/run_opt.py data=video data.seq=\"$FOLDER_NAME\" data.video_dir=images data.ext=\"$extension\" data.root=\"$DATA_ROOT\" run_opt=True run_vis=True"
        echo "Running video command: $CMD"
        eval "$CMD"
        ;;
        
      *)
        echo "Skipping unknown file type: $file"
        ;;
    esac
  fi
done


/home/gchatz/aionhmr/aionhmr-a/src/util/png2jpg.py