#################### PACKAGE ACTIONS ###################

reinstall_package:
	@pip uninstall -y decipherer || :
	@pip install -e .

run_api:
	uvicorn web.app:app --reload

run_app:
	streamlit run web/app.py
