# hacks-ai-courses

> Сервис подбора онлайн-курсов, позволяющий составить пользователю образовательную программу на основе данных вакансии.

Входные данные:
- Ссылка на вакансию
- или название вакансии
- или описание требований вакансии

Выходные данные:
- Список наиболее подходящих курсов GeekBrains под данную вакансию

## Frontend
---
Frontend написан на Vite + Vue3  
Находится в директории [frontend](https://github.com/obryadov111/hacks-ai-courses/tree/main/frontend/)  
Переход в директорию:  
`cd frontend`  
Установка зависимостей:  
`npm install`  
Запуск версии для разработчика:  
`npm run dev`  
Сборка и упаковка для развертывания:  
`npm run build`  
Адрес по умолчанию:  
`http://localhost:5173/`  

## Backend
---
Backend реализован с помощью Flask  
Находится в директории [microservice](https://github.com/obryadov111/hacks-ai-courses/tree/main/microservice/)  
Переход в директорию:  
`cd microservice`  
Установка зависимостей:  
`python -m pip install -r requirements.txt`  
Запуск:  
`python app.py`  
Сборка и упаковка для развертывания:  
`docker build .`  
Адрес по умолчанию:  
`http://localhost:5000/`  

## Docker-compose
---
Развёртывание приложения используя docker-compose:  
`docker compose up -d`  
Адрес Web интерфейса:  
`http://localhost:666/`  
Адрес API:  
`http://localhost:404/`  

## Стек технологий
---
 - Python
 - regexp
 - natasha
 - nltk
 - BeautifulSoup
 - transliterate
 - flask
 - vite 
 - vue3