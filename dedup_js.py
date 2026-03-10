with open('dashboard.py', encoding='utf-8') as f:
    content = f.read()

# Count how many script blocks exist
count = content.count('<script>')
print(f'Found {count} script blocks')

if count > 1:
    # Keep only the LAST script block, remove the earlier ones
    # Find all script block positions
    positions = []
    idx = 0
    while True:
        pos = content.find('    <script>', idx)
        if pos == -1:
            break
        positions.append(pos)
        idx = pos + 1
    
    print(f'Script positions: {positions}')
    
    # Remove all but the last one
    for pos in positions[:-1]:
        end = content.find('    </script>', pos) + len('    </script>')
        block = content[pos:end]
        content = content.replace(block, '', 1)
        print(f'Removed duplicate script block')

# Verify
count_after = content.count('<script>')
print(f'Script blocks after fix: {count_after}')

with open('dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify Python syntax
try:
    import ast
    ast.parse(content)
    print('Python syntax OK!')
except SyntaxError as e:
    print(f'Syntax error at line {e.lineno}: {e.msg}')
