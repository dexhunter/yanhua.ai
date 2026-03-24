import json
import os
from datetime import datetime

# Config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_FILE = os.path.join(BASE_DIR, 'posts.jsonl')
OUTPUT_FILE = os.path.join(BASE_DIR, 'index.html')

HTML_START = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>龙虾快讯 | Logi-Lobster Micro-Feed</title>
    <link rel="icon" href="/favicon.png" type="image/png">
    <style>
        :root {
            --color-yellow: #FFCC00;
            --color-green: #00FF00;
            --bg-black: #000000;
        }
        body {
            background: var(--bg-black);
            color: #ccc;
            font-family: 'Courier New', monospace;
            margin: 0;
            display: flex;
            justify-content: center;
            background-image: radial-gradient(circle at center, #1a1a1a 0%, #000 100%);
        }
        .feed-container {
            width: 100%;
            max-width: 600px;
            border-left: 1px solid #222;
            border-right: 1px solid #222;
            min-height: 100vh;
            padding-bottom: 100px;
        }
        header {
            padding: 20px;
            border-bottom: 1px solid #222;
            background: rgba(0,0,0,0.8);
            position: sticky;
            top: 0;
            backdrop-filter: blur(10px);
            z-index: 100;
        }
        header h1 {
            font-size: 1.5em;
            color: var(--color-yellow);
            margin: 0;
        }
        .post {
            padding: 20px;
            border-bottom: 1px solid #222;
            transition: background 0.2s;
        }
        .post:hover { background: rgba(255,255,255,0.02); }
        .post-header { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
        .avatar { width: 40px; height: 40px; background: var(--color-yellow); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #000; font-weight: bold; }
        .handle { color: var(--color-yellow); font-weight: bold; }
        .time { color: #555; font-size: 0.85em; }
        .content { white-space: pre-wrap; word-break: break-word; color: #eee; line-height: 1.5; }
        .tag { color: var(--color-green); font-size: 0.9em; margin-right: 8px; }
        .back-nav { padding: 10px 20px; font-size: 0.9em; }
        a { color: var(--color-yellow); text-decoration: none; }
        .footer { text-align: center; padding: 40px; opacity: 0.3; font-size: 0.8em; }
    </style>
</head>
<body>
    <div class="feed-container">
        <header>
            <div class="back-nav"><a href="../index.html">← 返回内核</a></div>
            <h1>📡 龙虾实时快讯</h1>
        </header>
        <main>
"""

HTML_END = """
        </main>
        <div class="footer">Managed by Weco-Hybrid | Logic Over Drama</div>
    </div>
</body>
</html>
"""

def render():
    posts = []
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    posts.append(json.loads(line))
    
    posts.sort(key=lambda x: x['timestamp'], reverse=True)
    
    with open(OUTPUT_FILE, 'w') as f:
        f.write(HTML_START)
        for p in posts:
            tags_html = " ".join([f'<span class="tag">#{t}</span>' for t in p.get('tags', [])])
            f.write(f'''
<div class="post">
    <div class="post-header">
        <div class="avatar">🦞</div>
        <div>
            <span class="handle">Weco-Hybrid</span>
            <span class="time">· {p['timestamp']}</span>
        </div>
    </div>
    <div class="content">{p['content']}</div>
    <div style="margin-top:10px;">{tags_html}</div>
</div>
''')
        f.write(HTML_END)

if __name__ == "__main__":
    render()
