docker build --pull --rm -f "Dockerfile" -t taskmanagerbackend "."
docker run -p 8000:8000 --rm -it taskmanagerbackend:latest
