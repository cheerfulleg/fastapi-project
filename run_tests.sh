#!/bin/bash
TESTING=True pytest -p no:warnings -k
#TESTING=True pytest -p no:warnings -k 'not test_task_status'