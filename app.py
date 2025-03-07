from flask import Flask, render_template, request
import markdown
import os
from datetime import datetime

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))

@app.route('/')
def home():
    #return "Hello World! 这是测试页面"

    return render_template('home.html')

@app.route('/notes')
def notes():
    notes_dir = os.path.join(app.root_path, 'content', 'notes')
    notes = []
    for filename in os.listdir(notes_dir):
        if filename.endswith('.md'):
            with open(os.path.join(notes_dir, filename), 'r', encoding='utf-8') as f:
                content = f.read()
                # 解析 markdown 文件头部的元数据
                title = filename.replace('.md', '').replace('-', ' ').title()
                date = datetime.fromtimestamp(os.path.getmtime(os.path.join(notes_dir, filename)))
                notes.append({
                    'title': title,
                    'date': date,
                    'url': f'/notes/{filename.replace(".md", "")}'
                })
    return render_template('notes/index.html', notes=sorted(notes, key=lambda x: x['date'], reverse=True))

@app.route('/notes/<note_id>')
def note(note_id):
    try:
        with open(os.path.join(app.root_path, 'content', 'notes', f'{note_id}.md'), 'r', encoding='utf-8') as f:
            content = f.read()
            html = markdown.markdown(content, extensions=['fenced_code', 'tables'])
            return render_template('notes/post.html', content=html)
    except FileNotFoundError:
        return "Note not found", 404
    
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
    
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # 修改为其他端口号