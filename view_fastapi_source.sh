#!/bin/bash
# Script to explore FastAPI source code in Docker container

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         🔍 How to View FastAPI Source Code in Container       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Get container name
CONTAINER="python-python-app-1"

# Get FastAPI location
FASTAPI_PATH="/usr/local/lib/python3.11/site-packages/fastapi"

echo "📍 FastAPI is installed at:"
echo "   $FASTAPI_PATH"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 METHOD 1: Access Container Shell Interactively"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Run this command to enter the container:"
echo "  $ docker exec -it $CONTAINER /bin/bash"
echo ""
echo "Then inside the container, you can:"
echo "  $ cd $FASTAPI_PATH"
echo "  $ ls -la"
echo "  $ cat __init__.py"
echo "  $ cat applications.py"
echo "  $ cat routing.py"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 METHOD 2: View Specific Files from Outside"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "View FastAPI main file:"
echo "  $ docker exec $CONTAINER cat $FASTAPI_PATH/__init__.py"
echo ""
echo "View FastAPI application class:"
echo "  $ docker exec $CONTAINER cat $FASTAPI_PATH/applications.py"
echo ""
echo "View routing logic:"
echo "  $ docker exec $CONTAINER cat $FASTAPI_PATH/routing.py"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 METHOD 3: Copy Files to Your Local Machine"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Copy entire FastAPI folder:"
echo "  $ docker cp $CONTAINER:$FASTAPI_PATH ./fastapi_source"
echo ""
echo "Then you can browse it with VS Code:"
echo "  $ code ./fastapi_source"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 METHOD 4: Use Python to Inspect"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "View FastAPI class source:"
echo "  $ docker exec $CONTAINER python -c \"import inspect; import fastapi; print(inspect.getsource(fastapi.FastAPI))\""
echo ""

