# Targets

build:
	python3.11 -m venv .venv && \
	source .venv/bin/activate && \
	pip3.11 install --upgrade pip && \
	pip3.11 install -r scripts/util/requirements.txt 
.PHONY: build

buildDocker:
	cd scripts && \
	aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 287138694668.dkr.ecr.ap-southeast-2.amazonaws.com && \
	docker build --platform=linux/amd64 -t nrlappstack-nrlecrrepoc7c22d9c-yaczcrzir0ic . && \
	docker tag nrlappstack-nrlecrrepoc7c22d9c-yaczcrzir0ic:latest 287138694668.dkr.ecr.ap-southeast-2.amazonaws.com/nrlappstack-nrlecrrepoc7c22d9c-yaczcrzir0ic:latest && \
	docker push 287138694668.dkr.ecr.ap-southeast-2.amazonaws.com/nrlappstack-nrlecrrepoc7c22d9c-yaczcrzir0ic:latest
.PHONY: buildDocker

deploy: build
	. .venv/bin/activate && \
	cd dynamodb; cdk deploy
.PHONY: deploy

deployApp: build
	. .venv/bin/activate && \
	cd nrl_app; cdk deploy
.PHONY: deployApp

deployAll: build deploy updateLadder updateTeams getData viewStats
.PHONY: deployAll

updateLadder: build
	. .venv/bin/activate && \
	python3.11 scripts/update_ladder.py
.PHONY: updateLadder

updateTeams: build
	. .venv/bin/activate && \
	python3.11 scripts/update_teams.py
.PHONY: updateTeams

getData: build
	. .venv/bin/activate && \
	python3.11 scripts/get_data.py
.PHONY: getData

viewStats: build
	. .venv/bin/activate && \
	python3.11 scripts/view_stats.py

destroy:
	. .venv/bin/activate && \
	cd dynamodb; cdk destroy; cd .. && \
	rm -rf .venv
.PHONY: destroy

clean:
	rm -rf .venv
.PHONY: clean
