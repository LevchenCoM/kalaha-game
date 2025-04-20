# Use the official Python base image
FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Add uv to PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy project files
COPY . .

# Install dependencies using uv
RUN uv sync --frozen

# Expose port 8000
EXPOSE 8000

# Start FastAPI app
CMD ["uv", "run", "fastapi", "run", "main.py", "--port", "8000"]
