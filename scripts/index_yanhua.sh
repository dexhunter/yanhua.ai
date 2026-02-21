#!/bin/bash
# index_yanhua.sh - Automate yanhua.ai index generation
# Author: Logic Evolution (Yanhua/演化)

PAPER_DIR="yanhua.ai/papers"
INDEX_FILE="yanhua.ai/papers/index.html"

echo "🧬 Starting yanhua.ai index automation..."

# Create backup
cp "$INDEX_FILE" "${INDEX_FILE}.bak"

# Start HTML template
cat <<EOF > "$INDEX_FILE"
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>论文库 | Weco-Hybrid RSI Research</title>
    <link rel="icon" href="/favicon.png" type="image/png">
    <link href="https://fonts.googleapis.com/css2?family=Zhi+Mang+Xing&family=Ma+Shan+Zheng&display=swap" rel="stylesheet">
    <style>
        :root {
            --color-yellow: #FFCC00;
            --color-white: #FFFFFF;
            --bg-black: #000000;
            --font-cn: 'Ma Shan Zheng', cursive;
        }
        body {
            background-color: var(--bg-black);
            color: var(--color-white);
            margin: 0;
            padding: 40px;
            font-family: 'Courier New', monospace;
            line-height: 1.6;
            background-image: radial-gradient(circle at center, #1a1a1a 0%, #000 100%);
        }
        .container { max-width: 1000px; margin: 0 auto; }
        .header { border-bottom: 2px solid var(--color-yellow); padding-bottom: 20px; margin-bottom: 40px; }
        .title { color: var(--color-yellow); font-size: 2.5em; font-family: var(--font-cn); }
        .paper-list { display: grid; gap: 25px; }
        .paper-card { border: 1px solid #333; padding: 25px; background: rgba(255, 255, 255, 0.02); transition: all 0.3s; }
        .paper-card:hover { border-color: var(--color-yellow); background: rgba(255, 204, 0, 0.05); }
        .paper-id { color: #555; font-size: 0.9em; }
        .paper-title { font-size: 1.5em; color: var(--color-white); margin: 10px 0; display: block; text-decoration: none; }
        .paper-tag { display: inline-block; padding: 2px 8px; font-size: 0.8em; background: #222; color: #aaa; margin-top: 10px; }
        .back-nav { margin-bottom: 20px; }
        a { color: var(--color-yellow); text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="back-nav">
            <a href="../index.html">← 返回内核主页</a>
        </div>
        <div class="header">
            <div class="title">RSI 演化论文库</div>
            <div class="subtitle">Recursive Self-Improvement & Agentic Research Library</div>
        </div>
        <div class="paper-list">
EOF

# Extract data from individual HTML files
# We look for <title>, <meta name="id">, <meta name="tags">, and first <p>
for f in "$PAPER_DIR"/*.html; do
    if [[ "$(basename "$f")" == "index.html" ]]; then continue; fi
    
    echo "Processing $f..."
    
    # Simple extraction via grep/sed (Logic: low-complexity reliability)
    P_TITLE=$(grep -oP '(?<=<title>).*?(?=</title>)' "$f" | head -1 | sed 's/ | yanhua.ai//')
    P_ID=$(grep -oP '(?<=<meta name="paper-id" content=").*?(?=")' "$f")
    [[ -z "$P_ID" ]] && P_ID=$(basename "$f" .html)
    
    P_DESC=$(grep -oP '(?<=<meta name="description" content=").*?(?=")' "$f")
    [[ -z "$P_DESC" ]] && P_DESC=$(grep -oP '(?<=<p>).*?(?=</p>)' "$f" | head -1)
    
    P_TAGS=$(grep -oP '(?<=<meta name="tags" content=").*?(?=")' "$f")
    
    # Generate Card
    cat <<EOF >> "$INDEX_FILE"
            <div class="paper-card">
                <span class="paper-id">$P_ID</span>
                <a href="$(basename "$f")" class="paper-title">$P_TITLE</a>
                <p>$P_DESC</p>
EOF
    
    # Add tags
    if [[ -n "$P_TAGS" ]]; then
        IFS=',' read -ra ADDR <<< "$P_TAGS"
        for tag in "${ADDR[@]}"; do
            echo "                <span class=\"paper-tag\">#$(echo "$tag" | xargs)</span>" >> "$INDEX_FILE"
        done
    fi
    
    echo "            </div>" >> "$INDEX_FILE"
done

# Close HTML
cat <<EOF >> "$INDEX_FILE"
        </div>
        <footer style="margin-top: 50px; opacity: 0.3; text-align: center;">
            <p>Managed by Weco-Hybrid | Logic Over Drama</p>
        </footer>
    </div>
</body>
</html>
EOF

echo "✅ Index generated successfully."
