# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
This test suite check /project endpoint
"""

import uuid
import os
import asyncio
import aiohttp
import pytest


from unittest.mock import patch, MagicMock
from tests.utils import asyncio_patch, AsyncioMagicMock

from gns3server.handlers.api.controller.project_handler import ProjectHandler
from gns3server.controller import Controller
from gns3server.controller.vm import VM


@pytest.fixture
def compute(http_controller, async_run):
    compute = MagicMock()
    compute.id = "example.com"
    Controller.instance()._computes = {"example.com": compute}
    return compute


@pytest.fixture
def project(http_controller, async_run):
    return async_run(Controller.instance().addProject())


@pytest.fixture
def vm(project, compute, async_run):
    vm = VM(project, compute, name="test", vm_type="vpcs")
    project._vms[vm.id] = vm
    return vm


def test_create_vm(http_controller, tmpdir, project, compute):
    response = MagicMock()
    response.json = {"console": 2048}
    compute.post = AsyncioMagicMock(return_value=response)

    response = http_controller.post("/projects/{}/vms".format(project.id), {
        "name": "test",
        "vm_type": "vpcs",
        "compute_id": "example.com",
        "properties": {
                "startup_script": "echo test"
        }
    }, example=True)
    assert response.status == 201
    assert response.json["name"] == "test"
    assert "name" not in response.json["properties"]


def test_update_vm(http_controller, tmpdir, project, compute, vm):
    response = MagicMock()
    response.json = {"console": 2048}
    compute.put = AsyncioMagicMock(return_value=response)

    response = http_controller.put("/projects/{}/vms/{}".format(project.id, vm.id), {
        "name": "test",
        "vm_type": "vpcs",
        "compute_id": "example.com",
        "properties": {
                "startup_script": "echo test"
        }
    }, example=True)
    assert response.status == 201
    assert response.json["name"] == "test"
    assert "name" not in response.json["properties"]


def test_start_vm(http_controller, tmpdir, project, compute, vm):
    response = MagicMock()
    compute.post = AsyncioMagicMock()

    response = http_controller.post("/projects/{}/vms/{}/start".format(project.id, vm.id), example=True)
    assert response.status == 201
    assert response.json["name"] == vm.name


def test_stop_vm(http_controller, tmpdir, project, compute, vm):
    response = MagicMock()
    compute.post = AsyncioMagicMock()

    response = http_controller.post("/projects/{}/vms/{}/stop".format(project.id, vm.id), example=True)
    assert response.status == 201
    assert response.json["name"] == vm.name


def test_suspend_vm(http_controller, tmpdir, project, compute, vm):
    response = MagicMock()
    compute.post = AsyncioMagicMock()

    response = http_controller.post("/projects/{}/vms/{}/suspend".format(project.id, vm.id), example=True)
    assert response.status == 201
    assert response.json["name"] == vm.name


def test_reload_vm(http_controller, tmpdir, project, compute, vm):
    response = MagicMock()
    compute.post = AsyncioMagicMock()

    response = http_controller.post("/projects/{}/vms/{}/reload".format(project.id, vm.id), example=True)
    assert response.status == 201
    assert response.json["name"] == vm.name


def test_delete_vm(http_controller, tmpdir, project, compute, vm):
    response = MagicMock()
    compute.post = AsyncioMagicMock()

    response = http_controller.delete("/projects/{}/vms/{}".format(project.id, vm.id), example=True)
    assert response.status == 201