def setup_environment():
    import os
    from dotenv import load_dotenv
    dotenv_path = '.env'
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
