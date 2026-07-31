from fastapi import FastAPI


app = FastAPI()


@app.get('/check')
def check():
    return {'message': "TaskFlow-Api"}
