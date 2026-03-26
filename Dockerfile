# Stage 1: Base Build stage
FROM python 3.13-slim as builder

# create the app
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Set enviroment variabel to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Install dependencies first for caching benefit
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

#stage 2: Production Stage
From python:3.13-slim


RUN useradd -m -r uppuser && \ 
	mkdir /app &&\
	chown -R appuser /app

# Set enviroment variabel to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#switch to non-root user
USER appuser


#expose the application port
EXPOSE 8000


#Make entry file executable
RUN chmod +x /app/entrypoint.prod.sh


#start the applicationn using python
CMD ["app/entrypoint.prod.sh"]