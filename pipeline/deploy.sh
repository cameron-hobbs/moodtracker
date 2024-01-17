#!/bin/bash

# todo: sed replace Dockerrun.aws.json

cd staging || exit

eb deploy moodtracker-prod

