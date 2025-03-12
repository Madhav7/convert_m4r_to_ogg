import os
import subprocess
import sys

def convert_m4r_to_ogg(input_folder, output_folder):
    """Convert all M4R files in input_folder to OGG format in output_folder with high quality."""
    try:
        # Validate input folder exists
        if not os.path.exists(input_folder):
            raise FileNotFoundError(f"Input folder not found: {input_folder}")
            
        # Create output folder if needed
        os.makedirs(output_folder, exist_ok=True)
        
        # Count files for progress reporting
        m4r_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.m4r')]
        total_files = len(m4r_files)
        
        if total_files == 0:
            print("No .m4r files found in the input folder.")
            return
            
        print(f"Found {total_files} .m4r files to convert")
        
        # Process files
        for idx, file_name in enumerate(m4r_files, 1):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, 
                                     os.path.splitext(file_name)[0] + '.ogg')
            
            print(f"Converting [{idx}/{total_files}]: {file_name}")
            
            # Conversion command with maximum quality preservation
            subprocess.run([
                'ffmpeg',
                '-i', input_path,
                '-c:a', 'libvorbis',
                '-q:a', '10',     # Highest quality setting for Vorbis
                '-ar', '48000',   # High sample rate
                '-y',             # Overwrite output files
                output_path
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        print(f"✓ Successfully converted {total_files} files to OGG format")
        print(f"Output location: {os.path.abspath(output_folder)}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except subprocess.CalledProcessError:
        print(f"Error: FFmpeg failed to convert {file_name}. Make sure FFmpeg is installed.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # You can replace these paths with command line arguments if preferred
    input_folder = "iphone_16e_ringtones"  # Replace with your input folder path
    output_folder = "output_ogg"    # Replace with your output folder path
    
    convert_m4r_to_ogg(input_folder, output_folder)
