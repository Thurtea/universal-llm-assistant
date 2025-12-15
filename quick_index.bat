@echo off
echo ============================================
echo AetherMUD Codebase Indexer
echo ============================================
echo.
echo This will create a vector database index
echo for fast semantic search.
echo.
echo Press any key to start indexing...
pause >nul

echo.
cd /d E:\LLM-Assistant\workspace-data\llm-assistant
python index_codebase.py

echo.
echo ============================================
echo Indexing complete!
echo ============================================
echo.
echo The GUI will now use fast indexed search.
echo Launch the assistant to see the difference!
echo.
pause
