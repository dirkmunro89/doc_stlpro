FROM pymesh/pymesh
LABEL maintainer="dirkmunro8@gmail.com" 
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 libstdc++6 -y
COPY requirements.txt ./
COPY import.py ./
RUN pip3 install -r requirements.txt
CMD ["python3", "-i", "import.py"]
