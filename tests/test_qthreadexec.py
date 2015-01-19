# © 2014 Mark Harviston <mark.harviston@gmail.com>
# © 2014 Arve Knudsen <arve.knudsen@gmail.com>
# BSD License
import pytest
import quamash


@pytest.fixture
def executor(request):
	exe = quamash.QThreadExecutor(5)
	request.addfinalizer(exe.shutdown)
	return exe


@pytest.fixture
def shutdown_executor():
	exe = quamash.QThreadExecutor(5)
	exe.shutdown()
	return exe


def test_shutdown_after_shutdown(shutdown_executor):
	with pytest.raises(RuntimeError):
		shutdown_executor.shutdown()


def test_ctx_after_shutdown(shutdown_executor):
	with pytest.raises(RuntimeError):
		with shutdown_executor:
			pass


def test_submit_after_shutdown(shutdown_executor):
	with pytest.raises(RuntimeError):
		shutdown_executor.submit(None)


def test_run_in_executor_without_loop(executor):
	f = executor.submit(lambda x: 2 + x, 2)
	r = f.result()
	assert r == 4


def test_run_in_executor_as_ctx_manager():
	with quamash.QThreadExecutor() as executor:
		f = executor.submit(lambda x: 2 + x, 2)
		r = f.result()
	assert r == 4
