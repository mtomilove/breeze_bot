FROM postgres:16.3

# Устанавливаем необходимые пакеты для поддержки локалей
RUN apt-get update && \
    apt-get install -y locales && \
    rm -rf /var/lib/apt/lists/*

# Генерируем локаль ru_RU.UTF-8
RUN localedef -i ru_RU -c -f UTF-8 -A /usr/share/locale/locale.alias ru_RU.UTF-8

# Устанавливаем переменные окружения для локали
ENV LANG ru_RU.utf8