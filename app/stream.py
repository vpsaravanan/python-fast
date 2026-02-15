# Streaming responses
@app.get("/stream")
async def stream_data():
    def generate():
        for i in range(10):
            yield f"data: {i}\n\n"
    return StreamingResponse(generate())