from fastapi import FastAPI


app = FastAPI()


@app.get('/check')
def check():
    return {'message': "TaskFlow-Api"}


@app.get('/check')
def check():
    return {'Greetings': "Say Hell0 !"}
