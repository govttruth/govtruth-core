with open('dashboard.py', encoding='utf-8') as f:
    content = f.read()

# Add data attributes to tr tag in build_mp_rows function
old = '        <tr>'
new = '        <tr data-cases="{cases}" data-assets="{assets}">'

if old in content:
    content = content.replace(old, new, 1)
    with open('dashboard.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Done! data-cases attribute added.')
else:
    print('ERROR: could not find tr tag')
    # Show context around mp_rows
    idx = content.find('rows +=')
    print('Context:', content[idx:idx+200])
