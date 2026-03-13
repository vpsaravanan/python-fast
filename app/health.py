# @app.get("/health", response_model=HealthResponse)
# async def health_check():
#     """Health check endpoint"""
#     uptime = datetime.now() - start_time
#     logger.info("Health check requested")
#     print(typing.__file__)
#     print(f"sys is: {sys}")
#     print(f"user site packages are: {site.getusersitepackages()}")

#     return HealthResponse(
#         status="healthy",
#         uptime=str(uptime),
#         timestamp=datetime.now().isoformat(),
#         output= sys.path.__str__() + ", --- " + sys.argv.__str__()
#     )