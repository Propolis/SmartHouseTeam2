# Этап сборки фронтенда
FROM node:16-alpine as build

WORKDIR /app
COPY . .

RUN npm install
RUN npm run build

# Этап раздачи статики через Nginx
FROM nginx:alpine

# Копируем нашу конфигурацию Nginx из папки nginx (на хосте)
COPY nginx/default.conf /etc/nginx/conf.d/default.conf


# Копируем собранную сборку React в директорию, где Nginx раздаёт статику
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
