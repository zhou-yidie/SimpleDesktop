import matplotlib.font_manager as fm

print("Listing some available fonts in Matplotlib:")
fonts = sorted([f.name for f in fm.fontManager.ttflist])

# Print a sample of fonts, especially checking for SimSun, SimSun-ExtB, Songti, Microsoft YaHei
target_fonts = ["SimSun", "Song", "STSong", "Microsoft YaHei", "SimHei", "DengXian", "KaiTi"]
found = []
for tf in target_fonts:
    matches = [f for f in fonts if tf.lower() in f.lower()]
    if matches:
        print(f"Matches for '{tf}': {list(set(matches))}")
        found.append(tf)

print("\nFirst 30 fonts available:")
for f in fonts[:30]:
    print(f)
