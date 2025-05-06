#!/bin/bash

INPUT="/root/input_video.mp4"
OUTPUT="/root/output_cut.mp4"

# 1. Проверка наличия входного файла
if [ ! -f "$INPUT" ]; then
  echo "❌ Ошибка: Входной файл $INPUT не найден."
  echo "Загрузи файл вручную командой:"
  echo "scp ПУТЬ_К_ФАЙЛУ root@89.104.68.219:/root/"
  exit 1
fi

# 2. Очистка предыдущих версий
rm -f /root/output_cut.* 2>/dev/null

# 3. Обработка
echo "🚀 Обработка началась..."
auto-editor "$INPUT" \
  --silent-speed 99999 \
  --video-speed 1 \
  --frame-rate 30 \
  -o "$OUTPUT"

# 4. Проверка результата
if [ -f "$OUTPUT" ]; then
  echo "✅ Готово: $OUTPUT"
  ls -lh "$OUTPUT"
else
  echo "❌ Ошибка: Файл $OUTPUT не создан. Проверь лог Auto-Editor."
  exit 1
fi

# 5. Очистка временных файлов
echo "🧹 Очищаю временные файлы..."
rm -rf /root/.cache/auto-editor /root/*.json /root/*.wav /root/*.mp3 2>/dev/null
