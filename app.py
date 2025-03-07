from flask import Flask, render_template, request,abort
import markdown
import os
from datetime import datetime
import yaml
from flask_paginate import Pagination

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))

@app.route('/')
def home():
    #return "Hello World! 这是测试页面"

    return render_template('home.html')

# 添加新的 publications 路由
@app.route('/publications')
def publications():
    publications_dir = os.path.join(app.root_path, 'content', 'publications')
    publications_by_year = {}
    
    # 确保目录存在
    if not os.path.exists(publications_dir):
        os.makedirs(publications_dir)
        
    for filename in os.listdir(publications_dir):
        if filename.endswith('.md'):
            with open(os.path.join(publications_dir, filename), 'r', encoding='utf-8') as f:
                content = f.read()
                # 从文件名获取年份（假设文件名格式为 YYYY-title.md）
                year = filename.split('-')[0] if '-' in filename else 'Unknown'
                # 解析 markdown 内容
                html = markdown.markdown(content, extensions=['fenced_code', 'tables'])
                
                # 按年份分组
                if year not in publications_by_year:
                    publications_by_year[year] = []
                
                publications_by_year[year].append({
                    'content': html,
                    'filename': filename
                })
    
    # 将年份分为数字和非数字两组，分别排序
    numeric_years = [year for year in publications_by_year.keys() if year.isdigit()]
    non_numeric_years = [year for year in publications_by_year.keys() if not year.isdigit()]
    
    # 自定义非年份的排序顺序
    custom_order = ['CNCB','Cooperative']
    
    # 按照自定义顺序对非年份进行排序
    sorted_non_numeric = sorted(non_numeric_years, key=lambda x: custom_order.index(x) if x in custom_order else len(custom_order))
    
    # 合并数字年份（降序）和已排序的非数字年份
    sorted_years = sorted(numeric_years, reverse=True) + sorted_non_numeric
    
    return render_template('publications.html', publications_by_year=publications_by_year, sorted_years=sorted_years)

@app.route('/projects')
def projects():
    # 放的是数据库还有工具

    return render_template('projects.html')

@app.route('/publications/<publication_id>')
def publication(publication_id):
    # 从content/publications目录读取对应的markdown文件
    publication_path = os.path.join(app.root_path, 'content', 'publications', f'{publication_id}.md')
    if not os.path.exists(publication_path):
        abort(404)
    
    # 读取并解析markdown内容
    with open(publication_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用markdown库将内容转换为HTML
    html_content = markdown.markdown(content, extensions=['extra', 'codehilite'])
    
    # 渲染模板
    return render_template('publication.html', content=html_content, title=publication_id)

@app.route('/projects/<project_id>')
def project(project_id):
    # 从content/projects目录读取对应的markdown文件
    project_path = os.path.join(app.root_path, 'content', 'projects', f'{project_id}.md')
    if not os.path.exists(project_path):
        abort(404)
    
    # 读取并解析markdown内容
    with open(project_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用markdown库将内容转换为HTML
    html_content = markdown.markdown(content, extensions=['extra', 'codehilite'])
    
    # 渲染模板
    return render_template('project.html', content=html_content, title=project_id)

# 添加笔记相关路由
# 添加笔记相关路由
@app.route('/notes')
@app.route('/notes/')
def notes():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # 每页显示的笔记数量
    
    # 获取所有笔记
    all_notes = get_all_notes()
    
    # 分页
    total = len(all_notes)
    start = (page - 1) * per_page
    end = min(start + per_page, total)
    notes_page = all_notes[start:end]
    
    # 创建分页对象
    pagination = Pagination(page=page, total=total, per_page=per_page, 
                           css_framework='bootstrap4')
    
    # 获取所有标签
    all_tags = get_all_tags(all_notes)
    
    # 计算总页数
    total_pages = (total + per_page - 1) // per_page
    
    return render_template('notes.html', notes=notes_page, 
                          pagination=pagination, all_tags=all_tags,
                          page=page, total_pages=total_pages)

@app.route('/notes/tag/<tag>')
def notes_by_tag(tag):
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # 获取所有笔记
    all_notes = get_all_notes()
    
    # 过滤指定标签的笔记
    filtered_notes = [note for note in all_notes if tag in note['tags']]
    
    # 分页
    total = len(filtered_notes)
    start = (page - 1) * per_page
    end = min(start + per_page, total)
    notes_page = filtered_notes[start:end]
    
    # 创建分页对象
    pagination = Pagination(page=page, total=total, per_page=per_page, 
                           css_framework='bootstrap4')
    
    # 获取所有标签
    all_tags = get_all_tags(all_notes)
    
    # 计算总页数
    total_pages = (total + per_page - 1) // per_page
    
    return render_template('notes.html', notes=notes_page, 
                          pagination=pagination, all_tags=all_tags, 
                          current_tag=tag, page=page, total_pages=total_pages)

@app.route('/notes/<note_id>')
def note(note_id):
    note = get_note_by_id(note_id)
    if not note:
        abort(404)
    return render_template('note.html', note=note)

# 辅助函数
def get_all_notes():
    notes = []
    notes_dir = os.path.join(app.root_path, 'content', 'notes')
    
    if not os.path.exists(notes_dir):
        return []
    
    for filename in os.listdir(notes_dir):
        if filename.endswith('.md'):
            note_id = filename[:-3]  # 移除.md后缀
            note = get_note_by_id(note_id)
            if note:
                notes.append(note)
    
    # 按日期排序，最新的在前
    notes.sort(key=lambda x: x['date'], reverse=True)
    return notes

def get_note_by_id(note_id):
    note_path = os.path.join(app.root_path, 'content', 'notes', f'{note_id}.md')
    
    if not os.path.exists(note_path):
        return None
    
    with open(note_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析YAML前置元数据和Markdown内容
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            front_matter = yaml.safe_load(parts[1])
            markdown_content = parts[2]
        else:
            front_matter = {}
            markdown_content = content
    else:
        front_matter = {}
        markdown_content = content
    
    # 将Markdown转换为HTML
    html_content = markdown.markdown(
        markdown_content,
        extensions=['extra', 'codehilite', 'toc', 'tables']
    )
    
    # 提取元数据
    title = front_matter.get('title', note_id)
    date_str = front_matter.get('date', datetime.now().strftime('%Y-%m-%d'))
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except:
        date = datetime.now()
    
    tags = front_matter.get('tags', [])
    description = front_matter.get('description', '')
    reading_time = front_matter.get('reading_time', estimate_reading_time(markdown_content))
    
    return {
        'id': note_id,
        'title': title,
        'date': date,
        'tags': tags,
        'description': description,
        'content': html_content,
        'reading_time': reading_time
    }

def get_all_tags(notes):
    tags = set()
    for note in notes:
        for tag in note['tags']:
            tags.add(tag)
    return sorted(list(tags))

def estimate_reading_time(content):
    # 估计阅读时间：假设平均阅读速度为每分钟200个单词
    words = len(content.split())
    minutes = max(1, round(words / 200))
    return minutes
    
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # 修改为其他端口号