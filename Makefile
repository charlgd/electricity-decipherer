#################### PACKAGE ACTIONS ###################

reinstall_package:
	@pip uninstall -y decipherer || :
	@pip install -e .

run_api:
	uvicorn decipherer.api.main:app --reload
