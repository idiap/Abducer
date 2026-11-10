# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
# Build only the context produced by integrations.chatgpt.deployment.
FROM ghcr.io/astral-sh/uv:0.8.3 AS uv
FROM python:3.12-slim
COPY --from=uv /uv /usr/local/bin/uv
ENV UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/abducer-venv \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/abducer-venv/bin:$PATH" \
    VIRTUAL_ENV=/opt/abducer-venv \
    PYTHON=/opt/abducer-venv/bin/python \
    PYTHONNOUSERSITE=1 \
    ABDUCER_REPOSITORY_ROOT=/app \
    ABDUCER_DATA_ROOT=/data
WORKDIR /app
COPY source/ /app/
RUN /usr/local/bin/python integrations/chatgpt/setup_runtime.py --environment /opt/abducer-venv \
    && chmod a+r /opt/abducer-venv/abducer-setup.json \
    && python -c 'from pathlib import Path; from integrations.chatgpt.startup import preload; from integrations.chatgpt.execution_registry import ExecutionRegistry; status = preload(ExecutionRegistry(Path("/app"))); assert status["packages"]["status"] == "ready", status["packages"]' \
    && useradd --uid 10001 --create-home abducer \
    && mkdir /data && chown abducer:abducer /data
USER abducer
EXPOSE 8000
CMD ["python", "-m", "integrations.chatgpt.server", "serve", "--host", "0.0.0.0", "--port", "8000"]
