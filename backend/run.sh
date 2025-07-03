#./run.sh
# 서버 실행
echo "Starting server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 