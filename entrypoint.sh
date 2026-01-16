#!/bin/sh

uvicorn main:app --host $APP_HOST --port $APP_PORT --workers 4