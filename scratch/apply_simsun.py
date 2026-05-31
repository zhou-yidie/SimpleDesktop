import os
import re
import subprocess

scratch_dir = r"d:\Graduation_Project\SimpleDesktop\scratch"
# Safe, robust, no-tofu Chinese font block with SimSun first
target_font_block = """plt.rcParams['font.sans-serif'] = ['SimSun', 'Songti SC', 'STSong', 'Microsoft YaHei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False"""

def patch_file(filepath):
    # Skip self
    if os.path.basename(filepath) == 'apply_simsun.py':
        return False
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match the entire font.sans-serif line and optional axes.unicode_minus line
    pattern = r"plt\.rcParams\['font\.sans-serif'\].*?\n(?:plt\.rcParams\['axes\.unicode_minus'\].*?\n)?"
    
    new_content, count = re.subn(pattern, target_font_block + "\n", content)
    
    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully patched font configuration in {os.path.basename(filepath)}")
        return True
    return False

def main():
    py_files = [os.path.join(scratch_dir, f) for f in os.listdir(scratch_dir) if f.endswith('.py')]
    patched_files = []
    
    for filepath in py_files:
        if patch_file(filepath):
            patched_files.append(filepath)
            
    print(f"\nPatched {len(patched_files)} drawing scripts.")
    
    # Now run all the drawing scripts to regenerate the final PNG files
    active_scripts = [
        "draw_compatibility.py",
        "redraw_mvvm.py",
        "redraw_hilt_di.py",
        "redraw_tech_stack.py",
        "redraw_focus_retreat.py",
        "redraw_active_detect.py",
        "scratch_generate_charts.py",
        "scratch_draw_wechat_figs.py",
        "scratch_draw_module.py",
        "scratch_draw_ch2_figs.py",
        "scratch_draw_arch.py"
    ]
    
    print("\nRegenerating figure images...")
    for script_name in active_scripts:
        script_path = os.path.join(scratch_dir, script_name)
        if os.path.exists(script_path):
            print(f"Running {script_name}...")
            res = subprocess.run(["python", script_path], capture_output=True, text=True)
            if res.returncode == 0:
                print(f"Successfully regenerated {script_name} output.")
            else:
                print(f"Error running {script_name}:\n{res.stderr}\n{res.stdout}")

if __name__ == '__main__':
    main()
