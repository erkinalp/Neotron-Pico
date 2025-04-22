"""
Script to run the BTX conversion process with proper orientation handling.
"""
import os
import sys
import subprocess
import re

def fix_orientation_handling(script_path):
    """Fix the orientation handling in the conversion script."""
    with open(script_path, 'r') as f:
        content = f.read()
    
    pattern = r"(orientation = footprint\.GetOrientation\(\).*?footprint\.SetOrientation\(new_orientation\))"
    replacement = """# KiCad uses 0.1 degrees for rotation, so 1800 = 180 degrees
            current_angle = footprint.GetOrientation()
            footprint.SetOrientation(-current_angle)"""
    
    modified_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(script_path, 'w') as f:
        f.write(modified_content)
    
    print(f"Fixed orientation handling in {script_path}")

def main():
    """Main function to run the conversion process."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    
    btx_convert_script = os.path.join(script_dir, "btx_convert_proper.py")
    try:
        subprocess.run(["python3", btx_convert_script], check=False)
        print("Generated conversion script")
    except subprocess.CalledProcessError as e:
        print(f"Error generating conversion script: {e}")
        return 1
    
    convert_pcb_script = os.path.join(script_dir, "convert_pcb_proper.py")
    fix_orientation_handling(convert_pcb_script)
    
    input_pcb = os.path.join(repo_dir, "Kicad", "neotron-pico.kicad_pcb")
    output_pcb = os.path.join(repo_dir, "Kicad", "neotron-pico-btx.kicad_pcb")
    specs_file = os.path.join(script_dir, "btx_specs_proper.json")
    
    try:
        result = subprocess.run(
            ["python3", convert_pcb_script, input_pcb, output_pcb, specs_file],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error executing conversion script: {e}")
        print(f"Error output: {e.stderr}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
