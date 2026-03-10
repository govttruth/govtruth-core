with open('dashboard.py', encoding='utf-8') as f:
    content = f.read()

# Remove the badly placed JS that's outside the HTML string
bad_js_start = '\n<script>\nvar tableCollapsed = false;'
bad_js_end = '</script>\n'

# Find and remove everything from <script> to </script> that's outside HTML
start_idx = content.find(bad_js_start)
if start_idx == -1:
    print('Could not find bad JS block - trying alternate search')
    start_idx = content.find('\n<script>')
    
if start_idx != -1:
    end_idx = content.find('</script>\n', start_idx) + len('</script>\n')
    bad_block = content[start_idx:end_idx]
    print(f'Found bad block at line ~{content[:start_idx].count(chr(10))}')
    print(f'Block length: {len(bad_block)} chars')
    
    # Remove bad block
    content = content[:start_idx] + content[end_idx:]
    print('Removed bad JS block')
else:
    print('ERROR: Could not find JS block')

# Now find the closing </body> tag inside the HTML string and insert JS there
# The JS needs to be inside the html = f"""...""" string
good_js = """    <script>
    var tableCollapsed = false;

    function searchMPs() {{
        var query = document.getElementById('mp-search').value.toLowerCase();
        var filter = document.getElementById('active-filter').value;
        var rows = document.querySelectorAll('#mp-tbody tr');
        var visible = 0;
        rows.forEach(function(row) {{
            var text = row.textContent.toLowerCase();
            var matchQuery = !query || text.includes(query);
            var cases = parseInt(row.getAttribute('data-cases') || '0');
            var assets = parseFloat(row.getAttribute('data-assets') || '0');
            var matchFilter = true;
            if (filter === 'criminal') matchFilter = cases > 0;
            if (filter === '100cr') matchFilter = assets > 10000000000;
            if (filter === 'notfiled') matchFilter = assets === 0;
            if (matchQuery && matchFilter) {{
                row.style.display = '';
                visible++;
            }} else {{
                row.style.display = 'none';
            }}
        }});
        document.getElementById('search-count').textContent = visible + ' MPs shown';
    }}

    function setFilter(val, btn) {{
        document.getElementById('active-filter').value = val;
        document.querySelectorAll('.filter-btn').forEach(function(b) {{
            b.classList.remove('filter-active');
        }});
        btn.classList.add('filter-active');
        searchMPs();
    }}

    function toggleTable() {{
        var tc = document.getElementById('mp-table-container');
        var btn = document.getElementById('toggle-btn');
        tableCollapsed = !tableCollapsed;
        if (tableCollapsed) {{
            tc.classList.add('table-collapsed');
            btn.textContent = 'EXPAND';
        }} else {{
            tc.classList.remove('table-collapsed');
            btn.textContent = 'MINIMIZE';
        }}
    }}
    </script>
"""

# Insert before <!-- FOOTER --> comment or before </body>
if '<!-- FOOTER -->' in content:
    content = content.replace('<!-- FOOTER -->', good_js + '<!-- FOOTER -->')
    print('Inserted JS before FOOTER comment')
elif '</body>' in content:
    content = content.replace('</body>', good_js + '</body>')
    print('Inserted JS before </body>')
else:
    print('ERROR: No insertion point found')

with open('dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify it's valid Python
try:
    import ast
    ast.parse(content)
    print('Python syntax OK!')
except SyntaxError as e:
    print(f'Still has syntax error at line {e.lineno}: {e.msg}')
