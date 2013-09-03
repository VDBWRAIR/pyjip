#!/usr/bin/env python


from jip import find, Pipeline, create_jobs


def test_bash_tool_options():
    bash = find("bash")
    assert bash.options is not None
    assert len(bash.options) == 4
    assert bash.options['cmd'] is not None
    assert bash.options['input'] is not None
    assert bash.options['output'] is not None


def test_bash_tool_job_rendering():
    p = Pipeline()
    p.run('bash', cmd="testme", output="test.out")
    jobs = create_jobs(p, embedded=True)
    assert len(jobs) == 1
    assert jobs[0].command == "(testme)> test.out"
