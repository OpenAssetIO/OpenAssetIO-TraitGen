#
#   Copyright 2022 The Foundry Visionmongers Ltd
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
"""
Tests for the main openassetio_traitgen.generate entry point.
"""

import logging
from unittest import mock

import pytest

import openassetio_traitgen

# pylint: disable=redefined-outer-name, invalid-name
# pylint: disable=missing-class-docstring, missing-function-docstring
# pylint: disable=too-many-arguments


class Test_generate:
    def test_when_description_path_valid_then_generate_called_with_declaration(
        self,
        yaml_path_all,
        declaration_all,
        some_output_dir,
        some_creation_callback,
        mock_generator_a,
        a_capturing_logger,
    ):
        openassetio_traitgen.generate(
            description_path=yaml_path_all,
            output_directory=some_output_dir,
            generator="a",
            creation_callback=some_creation_callback,
            logger=a_capturing_logger,
        )

        call_args = mock_generator_a.generate.call_args[0]
        assert call_args[0] == declaration_all

    def test_when_description_path_invalid_then_FileNotFoundError_raised(
        self,
        some_output_dir,
        some_creation_callback,
        a_capturing_logger,
    ):
        with pytest.raises(FileNotFoundError):
            openassetio_traitgen.generate(
                description_path="invalid",
                output_directory=some_output_dir,
                generator="a",
                creation_callback=some_creation_callback,
                logger=a_capturing_logger,
            )

    def test_when_generator_set_then_generate_called_with_supplied_generation_arguments(
        self,
        yaml_path_all,
        some_output_dir,
        some_creation_callback,
        mock_generator_a,
        a_capturing_logger,
    ):
        openassetio_traitgen.generate(
            description_path=yaml_path_all,
            output_directory=some_output_dir,
            generator="a",
            creation_callback=some_creation_callback,
            logger=a_capturing_logger,
        )

        call_args = mock_generator_a.generate.call_args[0]
        assert call_args[2] == some_output_dir
        assert call_args[3] is some_creation_callback

    def test_when_generator_not_set_then_generate_not_called(
        self,
        yaml_path_all,
        some_output_dir,
        some_creation_callback,
        mock_generator_a,
        a_capturing_logger,
    ):
        with pytest.raises(ValueError):
            openassetio_traitgen.generate(
                description_path=yaml_path_all,
                output_directory=some_output_dir,
                generator="",
                creation_callback=some_creation_callback,
                logger=a_capturing_logger,
            )

        mock_generator_a.generate.assert_not_called()

    def test_when_dry_run_set_true_then_generate_not_called(
        self,
        yaml_path_all,
        some_output_dir,
        some_creation_callback,
        mock_generator_a,
        a_capturing_logger,
    ):
        openassetio_traitgen.generate(
            description_path=yaml_path_all,
            output_directory=some_output_dir,
            generator="a",
            creation_callback=some_creation_callback,
            logger=a_capturing_logger,
            dry_run=True,
        )

        mock_generator_a.generate.assert_not_called()

    def test_when_dry_run_set_false_then_generate_called(
        self,
        yaml_path_all,
        some_output_dir,
        some_creation_callback,
        mock_generator_a,
        a_capturing_logger,
    ):
        openassetio_traitgen.generate(
            description_path=yaml_path_all,
            output_directory=some_output_dir,
            generator="a",
            creation_callback=some_creation_callback,
            logger=a_capturing_logger,
            dry_run=False,
        )

        mock_generator_a.generate.assert_called()

    def test_when_no_globals_then_generator_called_with_default_globals(
        self,
        yaml_path_all,
        some_output_dir,
        some_creation_callback,
        mock_generator_a,
        a_capturing_logger,
    ):
        openassetio_traitgen.generate(
            description_path=yaml_path_all,
            output_directory=some_output_dir,
            generator="a",
            creation_callback=some_creation_callback,
            logger=a_capturing_logger,
        )

        expected_globals = openassetio_traitgen.generators.helpers.default_template_globals()
        expected_globals["generator"] = "a"

        call_args = mock_generator_a.generate.call_args[0]
        assert call_args[1] == expected_globals

    def test_when_globals_supplied_then_generator_called_with_updated_globals(
        self,
        yaml_path_all,
        some_output_dir,
        some_creation_callback,
        mock_generator_a,
        a_capturing_logger,
    ):
        extra_globals = {"a": 1, "b": "🤠", "copyrightOwner": "Me"}

        openassetio_traitgen.generate(
            description_path=yaml_path_all,
            output_directory=some_output_dir,
            generator="a",
            creation_callback=some_creation_callback,
            logger=a_capturing_logger,
            template_globals=extra_globals,
        )

        expected_globals = openassetio_traitgen.generators.helpers.default_template_globals()
        expected_globals.update(extra_globals)
        expected_globals["generator"] = "a"

        call_args = mock_generator_a.generate.call_args[0]
        assert call_args[1] == expected_globals

    def test_when_globals_supplied_include_generator_then_generator_global_not_overridden(
        self,
        yaml_path_all,
        some_output_dir,
        some_creation_callback,
        mock_generator_a,
        a_capturing_logger,
    ):
        extra_globals = {"generator": "b"}

        openassetio_traitgen.generate(
            description_path=yaml_path_all,
            output_directory=some_output_dir,
            generator="a",
            creation_callback=some_creation_callback,
            logger=a_capturing_logger,
            template_globals=extra_globals,
        )

        expected_globals = openassetio_traitgen.generators.helpers.default_template_globals()
        expected_globals["generator"] = "a"

        call_args = mock_generator_a.generate.call_args[0]
        assert call_args[1] == expected_globals

    def test_when_valid_then_structure_is_logged_as_info(
        self,
        yaml_path_all,
        some_output_dir,
        some_creation_callback,
        a_capturing_logger,
        structure_all_log_messages,
    ):
        openassetio_traitgen.generate(
            description_path=yaml_path_all,
            output_directory=some_output_dir,
            generator="python",
            creation_callback=some_creation_callback,
            logger=a_capturing_logger,
        )
        structureMsg = a_capturing_logger.handlers[0].messages
        structureMsg.remove((logging.INFO, "Generating with generator python..."))
        assert structureMsg == structure_all_log_messages

    def test_when_dry_run_set_true_then_structure_is_still_logged_as_info(
        self,
        yaml_path_all,
        some_output_dir,
        some_creation_callback,
        a_capturing_logger,
        structure_all_log_messages,
    ):
        openassetio_traitgen.generate(
            description_path=yaml_path_all,
            output_directory=some_output_dir,
            generator="python",
            creation_callback=some_creation_callback,
            logger=a_capturing_logger,
            dry_run=True,
        )

        # Dry run does not make it to the generation code path, so no
        # "Generating with" message is logged.
        assert a_capturing_logger.handlers[0].messages == structure_all_log_messages

    def test_when_invalid_generator_error_raised(
        self,
        yaml_path_all,
        some_output_dir,
        some_creation_callback,
        a_capturing_logger,
    ):
        with pytest.raises(ValueError) as exc:
            openassetio_traitgen.generate(
                description_path=yaml_path_all,
                output_directory=some_output_dir,
                generator="Algol",
                creation_callback=some_creation_callback,
                logger=a_capturing_logger,
            )

        assert exc.value.args[0] == "Could not find generator Algol"


@pytest.fixture
def mock_generator_a(monkeypatch):
    mock_generator = mock.Mock()
    mock_generator.generate = mock.Mock()
    monkeypatch.setattr(openassetio_traitgen.generators, "a", mock_generator, raising=False)
    return mock_generator


@pytest.fixture
def some_output_dir(tmp_path):
    return str(tmp_path)


@pytest.fixture
def some_creation_callback():
    return lambda _: _


@pytest.fixture
def structure_all_log_messages():
    return [
        (logging.INFO, "Package: openassetio-traitgen-test-all"),
        (logging.INFO, "Traits:"),
        (logging.INFO, "aNamespace:"),
        (logging.INFO, "  - AllProperties"),
        (logging.INFO, "  - NoProperties"),
        (logging.INFO, "  - NoPropertiesMultipleUsage"),
        (logging.INFO, "anotherNamespace:"),
        (logging.INFO, "  - NoProperties"),
        (logging.INFO, "Specifications:"),
        (logging.INFO, "test:"),
        (logging.INFO, "  - LocalAndExternalTrait"),
        (logging.INFO, "  - OneExternalTrait"),
        (logging.INFO, "  - TwoLocalTraits"),
    ]
