FROM node:lts-alpine

# install project dependencies
RUN npm install -g @vue/cli

WORKDIR /frontend
# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .


# vue ui --headless --port 8000 --host 0.0.0.0
# CMD [ "vue", "ui", "--headless" , "--port", "8000",  "--host", "0.0.0.0" ]
CMD [ "npm", "run", "serve",  "--", "--port", "8000"]

