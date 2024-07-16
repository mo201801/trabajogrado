from flask import Flask
@app.route('/')
def index():
  return 'Hola Mundo'
if __name__ == '__main__':
  app.run()
