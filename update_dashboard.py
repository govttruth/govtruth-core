with open('dashboard.py', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS styles before </style>
new_styles = """
        .search-box {
            display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap;
        }
        .search-input {
            flex: 1; min-width: 200px; background: #0d0d1a; border: 1px solid #1a1a3a;
            color: #fff; padding: 10px 16px; border-radius: 6px; font-size: 0.9em;
            outline: none;
        }
        .search-input:focus { border-color: #00ff88; }
        .search-input::placeholder { color: #444; }
        .filter-btn {
            background: #0d0d1a; border: 1px solid #1a1a3a; color: #888;
            padding: 10px 16px; border-radius: 6px; cursor: pointer; font-size: 0.8em;
            letter-spacing: 1px; transition: all 0.2s;
        }
        .filter-btn:hover { border-color: #ff3355; color: #ff3355; }
        .filter-active { border-color: #ff3355 !important; color: #ff3355 !important; }
        .toggle-btn {
            background: #0d0d1a; border: 1px solid #1a1a3a; color: #888;
            padding: 10px 14px; border-radius: 6px; cursor: pointer; font-size: 0.75em;
            letter-spacing: 1px; margin-left: auto;
        }
        .toggle-btn:hover { border-color: #00ff88; color: #00ff88; }
        .table-collapsed { max-height: 320px; overflow-y: hidden; position: relative; }
        .table-collapsed::after {
            content: ''; position: absolute; bottom: 0; left: 0; right: 0;
            height: 80px; background: linear-gradient(transparent, #0a0a0f);
            pointer-events: none;
        }
        .search-count { font-size: 0.75em; color: #666; margin-bottom: 10px; }
"""
content = content.replace('    </style>', new_styles + '    </style>')

# 2. Add JS search/filter/toggle before </body>
search_js = """
<script>
var tableCollapsed = false;

function searchMPs() {
    var query = document.getElementById('mp-search').value.toLowerCase();
    var filter = document.getElementById('active-filter').value;
    var rows = document.querySelectorAll('#mp-tbody tr');
    var visible = 0;
    rows.forEach(function(row) {
        var text = row.textContent.toLowerCase();
        var matchQuery = !query || text.includes(query);
        var cases = parseInt(row.getAttribute('data-cases') || '0');
        var assets = parseFloat(row.getAttribute('data-assets') || '0');
        var matchFilter = true;
        if (filter === 'criminal') matchFilter = cases > 0;
        if (filter === '100cr') matchFilter = assets > 10000000000;
        if (filter === 'notfiled') matchFilter = assets === 0;
        if (matchQuery && matchFilter) {
            row.style.display = '';
            visible++;
        } else {
            row.style.display = 'none';
        }
    });
    document.getElementById('search-count').textContent = visible + ' MPs shown';
}

function setFilter(val, btn) {
    document.getElementById('active-filter').value = val;
    document.querySelectorAll('.filter-btn').forEach(function(b) {
        b.classList.remove('filter-active');
    });
    btn.classList.add('filter-active');
    searchMPs();
}

function toggleTable() {
    var tc = document.getElementById('mp-table-container');
    var btn = document.getElementById('toggle-btn');
    tableCollapsed = !tableCollapsed;
    if (tableCollapsed) {
        tc.classList.add('table-collapsed');
        btn.textContent = 'EXPAND';
    } else {
        tc.classList.remove('table-collapsed');
        btn.textContent = 'MINIMIZE';
    }
}
</script>
"""
content = content.replace('</body>', search_js + '</body>')

# 3. Update section header
content = content.replace(
    '<h2>MP Asset Tracker — Top 50 by Declared Assets</h2>',
    '<h2>MP Asset Tracker — Search All 483 MPs</h2>'
)

# 4. Add search UI before table-container div
search_ui = """        <input type="hidden" id="active-filter" value="all">
        <div class="search-box">
            <input class="search-input" id="mp-search" placeholder="Search MP name, party, constituency..." oninput="searchMPs()">
            <button class="filter-btn filter-active" onclick="setFilter('all', this)">ALL</button>
            <button class="filter-btn" onclick="setFilter('criminal', this)">CRIMINAL CASES</button>
            <button class="filter-btn" onclick="setFilter('100cr', this)">100CR+</button>
            <button class="filter-btn" onclick="setFilter('notfiled', this)">NOT FILED</button>
            <button class="toggle-btn" id="toggle-btn" onclick="toggleTable()">MINIMIZE</button>
        </div>
        <div class="search-count" id="search-count">483 MPs shown</div>
        <div class="table-container" id="mp-table-container">"""

content = content.replace('        <div class="table-container">\n            <table>\n                <thead>\n                    <tr>\n                        <th>#</th>', 
    search_ui + '\n            <table>\n                <thead>\n                    <tr>\n                        <th>#</th>')

# 5. Add id to tbody
content = content.replace('<tbody>', '<tbody id="mp-tbody">', 1)

with open('dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Dashboard updated successfully!')
