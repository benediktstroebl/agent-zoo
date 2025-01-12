def write_to_blog(blog_content: str) -> str:
    """
    Write to the blog of an agent.
    """
    import os 
    from datetime import datetime
    agent_name = os.environ["AGENT_NAME"]
    WORKSPACE_DIR = os.environ["WORKSPACE_DIR"]
    agent_path = os.path.join(WORKSPACE_DIR, agent_name)
    blog_name = os.environ["BLOG_FNAME"]
    blog_format = os.environ["BLOG_FORMAT"]
    if blog_format == "communal":
        blog_path = os.path.join(WORKSPACE_DIR, "blog", blog_name)
    else: 
        blog_path = os.path.join(agent_path, blog_name)
        
    blog_content = f"""===============================
Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Author: {agent_name}
Content:
{blog_content}
===============================\n\n
"""

    with open(blog_path, "a") as f:
        f.write(blog_content)

    return f"Blog post written to {blog_path}!"