# Copyright 2012 Rackspace Hosting, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock

from silverberg.test.util import BaseTestCase

from silverberg.client import CqlClient

from silverberg.cluster import RoundRobinCassandraCluster


class RoundRobinCassandraClusterTests(BaseTestCase):
    def setUp(self):
        self.cass_client_patcher = mock.patch("silverberg.cluster.CqlClient")
        self.CqlClient = self.cass_client_patcher.start()
        self.addCleanup(self.cass_client_patcher.stop)

        self.clients = []

        def _CqlClient(*args, **kwargs):
            c = mock.Mock(CqlClient)
            self.clients.append(c)
            return c

        self.CqlClient.side_effect = _CqlClient

    def test_round_robin_execute(self):
        cluster = RoundRobinCassandraCluster(['one', 'two', 'three'], 'keyspace')

        for client, arg in [(0, 'foo'), (1, 'bar'), (2, 'baz'), (0, 'bax')]:
            result = cluster.execute(arg)
            self.clients[client].execute.assert_called_with(arg)
            self.assertEqual(self.clients[client].execute.return_value, result)
