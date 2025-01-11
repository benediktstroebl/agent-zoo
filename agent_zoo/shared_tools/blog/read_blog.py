import os 

def read_blog(agent_name):
    """
    Read the blog of an agent. 
    """
    ROOT_DIR = os.environ['AGENT_ZOO_ROOT']
    agent_path = os.path.join(ROOT_DIR, agent_name)
    blog_name = os.environ['BLOG_FNAME']
    blog_format = os.environ['BLOG_FORMAT']
    if blog_format == 'communal':
        blog_path = ROOT_DIR / 'blog' / blog_name
    else: 
        blog_path = os.path.join(agent_path, blog_name)
    os.makedirs(os.path.dirname(blog_path), exist_ok=True)
    with open(blog_path, 'r') as f:
        lines = f.readlines()
        header = lines[0].strip().split(',')
        data = [line.strip().split(',') for line in lines[1:]]

    return data 