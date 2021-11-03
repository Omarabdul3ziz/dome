FROM thevlang/vlang:alpine

WORKDIR /opt/vlang/app

COPY . .

EXPOSE 5000

ENTRYPOINT ["v", "run", "."]

# docker image build --tag i_vserver .
# docker network create --driver bridge n_vdome
# docker volume create v_vdome
# docker container run -d -v v_vdome:/opt/vlang/app/ -p 90:5000 --name c_vserver --network=n_vdome i_vserver