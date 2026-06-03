import re
import os

main_tex_path = r"d:\Graduation_Project\SimpleDesktop\latexpdf\main.tex"
chapters = [
    "contents/chapter1.tex",
    "contents/chapter2.tex",
    "contents/chapter3.tex",
    "contents/chapter4.tex",
    "contents/chapter5.tex"
]
chapters_full_paths = [os.path.join(r"d:\Graduation_Project\SimpleDesktop\latexpdf", c) for c in chapters]

# 1. Parse current main.tex bibliography
with open(main_tex_path, "r", encoding="utf-8") as f:
    main_text = f.read()

bib_section_match = re.search(r"\\begin\{thebibliography\}\{\d+\}(.*?)\\end\{thebibliography\}", main_text, re.DOTALL)
if not bib_section_match:
    raise ValueError("Could not find bibliography section in main.tex")

bib_content = bib_section_match.group(1)

# Find all \bibitem{key} and their text
# We scan from the first \bibitem to the end.
# We split by \bibitem
items = re.split(r"\\bibitem\{(\d+)\}", bib_content)
# items[0] is the text before the first \bibitem (usually whitespace/formatting)
# items[1] is the key of 1st bibitem, items[2] is the content of 1st bibitem
# items[3] is the key of 2nd bibitem, items[4] is the content of 2nd bibitem...

bib_dict = {}
for i in range(1, len(items), 2):
    key = items[i]
    content = items[i+1]
    # Clean content (trailing whitespace/newlines)
    bib_dict[key] = content.strip()

print(f"Parsed {len(bib_dict)} bibitems from main.tex.")

# 2. Find order of first appearance of citations in chapters
new_order = []
for cp in chapters_full_paths:
    if os.path.exists(cp):
        with open(cp, "r", encoding="utf-8") as f:
            text = f.read()
        matches = re.findall(r"\\upcite\{([^\}]+)\}", text)
        for m in matches:
            keys = [k.strip() for k in m.split(",")]
            for k in keys:
                if k not in new_order:
                    new_order.append(k)

print("Citation appearance order:")
print(new_order)
print(f"Total unique citations found in text: {len(new_order)}")

# Check if there are any bibitems not cited or any citations not in bibitems
not_cited = set(bib_dict.keys()) - set(new_order)
not_in_bib = set(new_order) - set(bib_dict.keys())
if not_cited:
    print(f"Warning: bibitems not cited: {not_cited}")
if not_in_bib:
    print(f"Warning: citations not in bibliography: {not_in_bib}")

# 3. Create mapping from old keys to new sequential keys (1-based index in new_order)
old_to_new = {}
for idx, old_key in enumerate(new_order):
    old_to_new[old_key] = str(idx + 1)

# For any bibitems that were somehow not cited, append them at the end
current_index = len(new_order) + 1
for old_key in sorted(list(bib_dict.keys())):
    if old_key not in old_to_new:
        old_to_new[old_key] = str(current_index)
        current_index += 1
        new_order.append(old_key)

print("Key mapping (old -> new):")
for old, new in sorted(old_to_new.items(), key=lambda x: int(x[1])):
    print(f"  {old} -> {new}")

# 4. Update Chapter files with new keys
def update_upcite_match(match):
    content = match.group(1)
    old_keys = [k.strip() for k in content.split(",")]
    new_keys = []
    for ok in old_keys:
        nk = old_to_new.get(ok, None)
        if nk:
            new_keys.append(nk)
    unique_keys = sorted(list(set(new_keys)), key=int)
    return f"\\upcite{{{','.join(unique_keys)}}}"

for cp in chapters_full_paths:
    if os.path.exists(cp):
        print(f"Updating citations in: {os.path.basename(cp)}")
        with open(cp, "r", encoding="utf-8") as f:
            text = f.read()
        updated_text = re.sub(r"\\upcite\{([^\}]+)\}", update_upcite_match, text)
        with open(cp, "w", encoding="utf-8") as f:
            f.write(updated_text)

# 5. Reconstruct main.tex bibliography in new order
new_bib_entries = []
for old_key in new_order:
    new_key = old_to_new[old_key]
    content = bib_dict[old_key]
    new_bib_entries.append(f"\\bibitem{{{new_key}}} {content}")

new_bib_content = "\n" + "\n".join(new_bib_entries) + "\n"

# Replace the old bibliography in main_text
def replace_bib(match):
    prefix = "\\begin{thebibliography}{99}"
    suffix = "\\end{thebibliography}"
    return prefix + new_bib_content + suffix

updated_main_text = re.sub(r"\\begin\{thebibliography\}\{\d+\}.*?\\end\{thebibliography\}", replace_bib, main_text, flags=re.DOTALL)

with open(main_tex_path, "w", encoding="utf-8") as f:
    f.write(updated_main_text)

print("Renumbering and reordering completed successfully!")
