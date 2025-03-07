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
    
if __name__ == '__main__':
    freezer.freeze()
    print("静态网站已生成到 docs 目录")