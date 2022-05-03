NSPACE="wjallen"
APP="mldata"
VER="0.1.0"
RPORT="6441"
FPORT="5041"
UID="827385"
GID="815499"

list-targets:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'


list:
	docker ps -a | grep ${NSPACE} || true
	docker images | grep ${NSPACE} || true


build-db:
	docker pull redis:6

build-api:
	docker build -t ${NSPACE}/${APP}-api:${VER} \
                     -f docker/Dockerfile.api \
                     ./

build-wrk:
	docker build -t ${NSPACE}/${APP}-wrk:${VER} \
                     -f docker/Dockerfile.wrk \
                     ./


run-db: build-db
	docker run --name ${NSPACE}-db \
                   -p ${RPORT}:6379 \
                   -d \
                   -u ${UID}:${GID} \
                   -v ${PWD}/data/:/data \
                   redis:6 \
                   --save 1 1


run-api: build-api
	RIP=$$(docker inspect ${NSPACE}-db | grep \"IPAddress\" | head -n1 | awk -F\" '{print $$4}') && \
	docker run --name ${NSPACE}-api \
                   --env REDIS_IP=$${RIP} \
                   -p ${FPORT}:5000 \
                   -d \
                   ${NSPACE}/${APP}-api:${VER} 

run-wrk: build-wrk
	RIP=$$(docker inspect ${NSPACE}-db | grep \"IPAddress\" | head -n1 | awk -F\" '{print $$4}') && \
	docker run --name ${NSPACE}-wrk \
                   --env REDIS_IP=$${RIP} \
                   -d \
                   ${NSPACE}/${APP}-wrk:${VER} 


clean-db:
	docker stop ${NSPACE}-db && docker rm -f ${NSPACE}-db || true

clean-api:
	docker stop ${NSPACE}-api && docker rm -f ${NSPACE}-api || true

clean-wrk:
	docker stop ${NSPACE}-wrk && docker rm -f ${NSPACE}-wrk || true


cycle-api: clean-api build-api run-api

cycle-db: clean-db build-db run-db

cycle-wrk: clean-wrk build-wrk run-wrk

cycle-all: cycle-db cycle-api cycle-wrk


push-api:
	docker push ${NSPACE}/${APP}-api:${VER}

push-wrk:
	docker push ${NSPACE}/${APP}-wrk:${VER}

push-all: push-api push-wrk


clean: clean-wrk clean-api clean-db

superclean: clean-wrk clean-api clean-db
	docker rmi -f ${NSPACE}/${APP}-api:${VER}
	docker rmi -f ${NSPACE}/${APP}-wrk:${VER}


