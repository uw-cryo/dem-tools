import pytest

from demtools.asp import Stereo


@pytest.mark.parametrize(
    'mock_run_command', [Stereo.RUN_COMMAND], indirect=True
)
@pytest.mark.usefixtures('mock_run_command')
class TestStereo(object):
    def test_run(self):
        assert Stereo().run_command == 'stereo'

    def test_algorithm_option(self):
        for algorithm in ['Local', 'SGM', 'SSGM', 'MGM']:
            assert Stereo(algorithm=algorithm).algorithm == \
                   Stereo.ALGORITHMS[algorithm]

    def test_map_projected(self):
        subject = Stereo(map_projected=True)
        run_call = subject.run_call()
        assert '-t dgmaprpc' in run_call
        assert '--alignment-method None' in run_call
        assert len(run_call) == 5

    def test_default_run_options(self):
        run_call = Stereo().run_call()
        assert '--stereo-algorithm 0' in run_call
        assert '--nodata-value -32768' in run_call
        assert len(run_call) == 3

    def test_map_projected_filter_options(self):
        options = ['-t foo', '--alignment-method align']
        subject = Stereo(map_projected=True, run_options=options)
        run_call = subject.run_call()
        assert '-t dgmaprpc' in run_call
        assert '--alignment-method None' in run_call
        assert '-t foo' not in run_call
        assert '--alignment-method align' not in run_call
        assert len(run_call) == 5

    def test_filter_run_options(self):
        subject = Stereo(run_options=['--stereo-algorithm 3'])
        run_call = subject.run_call()
        assert '--stereo-algorithm 3' not in run_call
        assert '--stereo-algorithm 0' in run_call     # Default Stereo algorithm

    def test_keep_custom_run_options(self):
        subject = Stereo(run_options=['--threads 6', '--processes 4'])
        run_call = subject.run_call()
        assert '--stereo-algorithm 3' not in run_call
        assert '--threads 6' in run_call
        assert '--processes 4' in run_call