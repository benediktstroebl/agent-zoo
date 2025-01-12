def write_to_blog(blog_content: str) -> str:
    """
    Write to the blog of an agent.
    """
    import os 
    agent_name = os.environ["AGENT_NAME"]
    WORKSPACE_DIR = os.environ["WORKSPACE_DIR"]
    agent_path = os.path.join(WORKSPACE_DIR, agent_name)
    blog_name = os.environ["BLOG_FNAME"]
    blog_format = os.environ["BLOG_FORMAT"]
    if blog_format == "communal":
        blog_path = WORKSPACE_DIR / "blog" / blog_name
    else: 
        blog_path = os.path.join(agent_path, blog_name)

    with open(blog_path, "a") as f:
        f.write(blog_content)

    return f"Blog post written to {blog_path}: {blog_content}"
