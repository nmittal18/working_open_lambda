def handler(conn, event):
    try:
        return "Hello, Neha!"
    except Exception as e:
        return {'error': str(e)} 
