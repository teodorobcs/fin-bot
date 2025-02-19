from fastapi import FastAPI

app = FastAPI() # Create a FastAPI application object

"""
        Decorators:
        The @app.get("/") decorator registers a GET HTTP method for the root path (/).
        This means when you navigate to http://127.0.0.1:8000/ in a browser or use tools like curl or Postman, the code under this decorator is executed.

        Function Definition:
        An asynchronous function (async) named root is defined. Because FastAPI allows asynchronous programming, you can use tools like await if needed. This makes handling concurrent requests more efficient.
        The function returns a dictionary: {"message": "FinBot is Running!"}. This will be sent as a JSON response to the browser/client.
"""

@app.get("/")
async def root():
    return {"message": "FinBot is Running!"}


"""
        if __name__ == "__main__":
            This statement ensures the script is executed directly (not imported as a module in another program or script).

        Importing Uvicorn:
            Uvicorn is an ASGI (Asynchronous Server Gateway Interface) server for running asynchronous Python applications like FastAPI.

        Running the Server:
            uvicorn.run(...) is used to start the FastAPI application.
            Parameters:
                app: The FastAPI application object to run.
                host="127.0.0.1": Specifies the server will run locally on the loopback address (localhost).
                port=8000: The port where the server listens for incoming requests. The API will be available at http://127.0.0.1:8000.
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
