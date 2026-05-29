#!/usr/bin/env sh

envsubst '$$EXTERNAL_PORT' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

exec "${@}"
