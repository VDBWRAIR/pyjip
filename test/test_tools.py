#!/usr/bin/env python
import pytest
from jip.tools import Tool, ValidationError, ScriptTool
from jip.options import ParserException


def test_tool_validation_valid():
    help_string = """\
    Some Tool

    Usage: tools [-i <input>] [-o <output>]

    Options:
        -i, --input <input>    The input
                               [Default: stdin]
        -o, --output <output>  The output
                               [Default: stdout]
    """
    tool = Tool(help_string)
    assert tool.options is not None
    assert len(tool.options) == 2
    tool.validate()


def test_tool_validation_missing_required():
    help_string = """\
    Some Tool

    Usage: tools -i <input> [-o <output>]

    Options:
        -i, --input <input>    The input
        -o, --output <output>  The output
                               [Default: stdout]
    """
    tool = Tool(help_string)
    assert tool.options is not None
    assert len(tool.options) == 2
    with pytest.raises(ValidationError) as execinfo:
        tool.validate()
    assert str(execinfo.value) == "tools: Option -i/--input " \
        "is required but not set!"


def test_tool_validation_unknown():
    help_string = """\
    Some Tool

    Usage: tools [-i <input>] [-o <output>]

    Options:
        -i, --input <input>    The input
                               [Default: stdin]
        -o, --output <output>  The output
                               [Default: stdout]
    """
    tool = Tool(help_string)
    assert tool.options is not None
    assert len(tool.options) == 2
    with pytest.raises(ParserException) as execinfo:
        tool.parse_args(["-x"])
    assert str(execinfo.value) == "unrecognized arguments: -x"


def test_tool_validate_input_file_not_found():
    help_string = """\
    Some Tool

    Usage: tools [-i <input>] [-o <output>]

    Options:
        -i, --input <input>    The input
                               [Default: stdin]
        -o, --output <output>  The output
                               [Default: stdout]
    """
    tool = Tool(help_string)
    tool.parse_args(["-i", "unknown"])
    with pytest.raises(ValidationError) as execinfo:
        tool.validate()
    assert str(execinfo.value) == "tools: Input file not found: unknown"


def test_load_script_block_from_string():
    script = ScriptTool.from_string(
        """#!/bin/bash
#Simple tool
#
#Usage: simple [-i <input>]
cat ${input}
        """)
    assert script is not None