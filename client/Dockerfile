FROM node:lts-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
# RUN npm run build

# FROM nginx:alpine
# COPY --from=build /app/dist/client /usr/share/nginx/html/

ENTRYPOINT ["npm", "run", "serve"]
# url = docker container inspect c_vserver --format='{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
# docker container run -d -e VUE_APP_API_URL=http://172.20.0.2:5000/ -p 91:8080 --name c_vclient --network=n_vdome i_vclient