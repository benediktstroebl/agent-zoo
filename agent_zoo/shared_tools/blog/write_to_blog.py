import os 

def write_to_blog(blog_content):
    """
    Write to the blog of an agent.
    """
    agent_name = os.environ['AGENT_NAME']
    ROOT_DIR = os.environ['AGENT_ZOO_ROOT']
    agent_path = os.path.join(ROOT_DIR, agent_name)
    blog_name = os.environ['BLOG_FNAME']
    blog_format = os.environ['BLOG_FORMAT']
    if blog_format == 'communal':
        blog_path = ROOT_DIR / 'blog' 
    else: 
        blog_path = os.path.join(agent_path, blog_name)

    with open(blog_path, 'w') as f:
        f.write(blog_content)
