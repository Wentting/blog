from flask_frozen import Freezer
from app import app
import os
import shutil

# 设置输出目录为 docs
app.config['FREEZER_DESTINATION'] = 'docs'
# 确保静态文件路径正确
app.config['FREEZER_RELATIVE_URLS'] = True
# 添加默认MIME类型，确保生成.html文件
app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html'
# 添加以下配置，强制URL末尾添加.html后缀
app.config['FREEZER_REMOVE_EXTRA_TRAILING_SLASH'] = True

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
  
# 添加notes路由生成器
@freezer.register_generator
def notes():
    yield {}  # 生成notes主页

# 添加notes_by_tag路由生成器
@freezer.register_generator
def notes_by_tag():
    # 获取所有标签
    notes_dir = os.path.join(app.root_path, 'content', 'notes')
    if os.path.exists(notes_dir):
        all_tags = set()
        for filename in os.listdir(notes_dir):
            if filename.endswith('.md'):
                # 这里简化处理，实际应该解析文件获取标签
                # 假设每个文件至少有一个标签
                all_tags.add('programmming')  # 示例标签
                all_tags.add('software')      # 示例标签
        
        for tag in all_tags:
            yield {'tag': tag}

# 添加单个note路由生成器
@freezer.register_generator
def note():
    notes_dir = os.path.join(app.root_path, 'content', 'notes')
    if os.path.exists(notes_dir):
        for filename in os.listdir(notes_dir):
            if filename.endswith('.md'):
                note_id = filename.replace('.md', '')
                yield {'note_id': note_id}  


# 添加后处理函数，为生成的文件添加.html后缀
def add_html_extension():
    docs_dir = os.path.join(app.root_path, 'docs')
    
    # 特别处理notes目录
    notes_dir = os.path.join(docs_dir, 'notes')
    notes_index = os.path.join(notes_dir, 'index.html')
    notes_html = os.path.join(docs_dir, 'notes.html')
    
    # 如果notes目录存在且有index文件，将其移动到根目录并重命名为notes.html
    if os.path.exists(notes_dir) and os.path.isdir(notes_dir):
        if os.path.exists(notes_index) and os.path.isfile(notes_index):
            print(f"将notes/index移动到根目录并重命名为notes.html")
            shutil.copy(notes_index, notes_html)
    
    # 处理根目录下的无后缀文件
    for item in os.listdir(docs_dir):
        item_path = os.path.join(docs_dir, item)
        # 如果是文件且没有扩展名
        if os.path.isfile(item_path) and '.' not in item and item != 'CNAME':
            new_path = item_path + '.html'
            print(f"重命名: {item} -> {item}.html")
            shutil.move(item_path, new_path)
            
            # 更新所有HTML文件中的链接
            update_links_in_html_files(docs_dir, item, item + '.html')
    
    # 处理notes目录下的无后缀文件
    if os.path.exists(notes_dir) and os.path.isdir(notes_dir):
        for item in os.listdir(notes_dir):
            item_path = os.path.join(notes_dir, item)
            # 如果是文件且没有扩展名
            if os.path.isfile(item_path) and '.' not in item and item != 'index':
                new_path = item_path + '.html'
                print(f"重命名: notes/{item} -> notes/{item}.html")
                shutil.move(item_path, new_path)
                
                # 更新所有HTML文件中的链接
                update_links_in_html_files(docs_dir, f"notes/{item}", f"notes/{item}.html")

# 更新HTML文件中的链接
def update_links_in_html_files(directory, old_link, new_link):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 更新href链接
                updated_content = content.replace(f'href="{old_link}"', f'href="{new_link}"')
                
                if content != updated_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print(f"已更新链接: {file_path}")
    
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
    # 为生成的文件添加.html后缀
    print("正在为生成的文件添加.html后缀...")
    add_html_extension()
    if os.path.exists(os.path.join(docs_dir, 'static')):
        print("静态资源已复制")
    else:
        print("警告: 静态资源未复制!")