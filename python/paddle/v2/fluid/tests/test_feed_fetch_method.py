#   Copyright (c) 2018 PaddlePaddle Authors. All Rights Reserve.
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

import paddle.v2.fluid.core as core
import unittest
import numpy as np


class TestFeedFetch(unittest.TestCase):
    def test_feed_fetch(self):
        scope = core.Scope()
        place = core.CPUPlace()
        input_array = np.ones((4, 4, 6)).astype("float32")
        input_array[0, 0, 0] = 3
        input_array[3, 3, 5] = 10
        input_tensor = core.LoDTensor([[0, 2, 4]])
        input_tensor.set(input_array, place)

        core.set_feed_variable(scope, input_tensor, "feed", 0)

        output_tensor = core.get_fetch_variable(scope, "feed", 0)

        output_lod = output_tensor.lod()
        self.assertEqual(0, output_lod[0][0])
        self.assertEqual(2, output_lod[0][1])
        self.assertEqual(4, output_lod[0][2])

        output_array = np.array(output_tensor)
        self.assertEqual(3, output_array[0, 0, 0])
        self.assertEqual(10, output_array[3, 3, 5])


if __name__ == "__main__":
    unittest.main()
