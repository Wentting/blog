from flask_frozen import Freezer
from app import app
import os

# 设置输出目录为 docs
app.config['FREEZER_DESTINATION'] = 'docs'
# 确保静态文件路径正确
app.config['FREEZER_RELATIVE_URLS'] = True

freezer = Freezer(app)

# @freezer.register_generator
# def note():
#     notes_dir = os.path.join(app.root_path, 'content', 'notes')
#     for filename in os.listdir(notes_dir):
#         if filename.endswith('.md'):
#             yield {'note_id': filename.replace('.md', '')}


@freezer.register_generator
def home():
    # 确保生成首页
    yield {}

@freezer.register_generator
def publications():
    yield {}

@freezer.register_generator
def projects():
    yield {}


# 出版物详情页面生成器
@freezer.register_generator
def publication():
    publications_dir = os.path.join(app.root_path, 'content', 'publications')
    if os.path.exists(publications_dir):
        for filename in os.listdir(publications_dir):
            if filename.endswith('.md'):
                yield {'publication_id': filename.replace('.md', '')}


    
if __name__ == '__main__':
    
    # 导入abort函数，修复app.py中的错误
    if 'abort' not in globals():
        from flask import abort
        app.abort = abort
        
    # 确保静态文件夹存在
    static_dir = os.path.join(app.root_path, 'static')
    if not os.path.exists(static_dir):
        print(f"警告: 静态文件夹 {static_dir} 不存在!")
    # 生成静态网站
    print("开始生成静态网站...")
    freezer.freeze()
    print("静态网站已生成到 docs 目录")
    
    # 检查生成的文件
    docs_dir = os.path.join(app.root_path, 'docs')
    if os.path.exists(os.path.join(docs_dir, 'index.html')):
        print("首页已生成")
    else:
        print("警告: 首页未生成!")
    
    if os.path.exists(os.path.join(docs_dir, 'static')):
        print("静态资源已复制")
    else:
        print("警告: 静态资源未复制!")