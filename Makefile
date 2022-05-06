install: install_auth install_task_tracker

install_auth:
	cd auth; make install

install_task_tracker:
	cd task_tracker; make install
