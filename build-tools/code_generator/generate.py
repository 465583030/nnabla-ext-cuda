# Copyright (c) 2017 Sony Corporation. All Rights Reserved.
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

import io
import os
import sys

from generator_common.init_cpp_common import generate_init_cpp
from utils.load_function_rst import Functions
from load_implements_rst import Implements
from utils.common import check_update

base = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../..')
template = os.path.abspath(os.path.dirname(
    os.path.abspath(__file__)) + '/templates')
functions = Functions()
info = functions.info
info['Implements'] = Implements().info

generation_list = {
    'cuda': ['src/nbla/cuda/init.cpp'],
    'cudnn': ['src/nbla/cuda/cudnn/init.cpp']
}

function_generation_list = {
    'cuda': ['include/nbla/cuda/function/{}.hpp', 'src/nbla/cuda/function/{}.cu'],
    'cudnn': ['include/nbla/cuda/cudnn/function/{}.hpp', 'src/nbla/cuda/cudnn/function/{}.cu']
}

for implements, filelist in generation_list.items():
    for fn in filelist:
        filename = '{}/{}'.format(base, fn)
        modulename = fn.replace('/', '_').replace('.', '_')
        temp = '{}/{}_template{}'.format(template,
                                         modulename, os.path.splitext(fn)[1])
        exec('import generator.generate_{}'.format(modulename))
        code_template = None
        with io.open(temp, 'rt', encoding='utf_8_sig') as f:
            code_template = f.read()
        if code_template:
            code = eval(
                ('generator.generate_{}.generate' +
                 '(info, code_template)').format(modulename))
            if code:
                check_update(filename, code, force=True)

for category, functions in info['Functions'].items():
    for function, function_info in functions.items():
        function_name = info['Names'][function]
        for implement in info['Implements'][function]:
            for fn in function_generation_list[implement]:
                filename = '{}/{}'.format(base, fn.format(function_name))
                modulename = fn.replace(
                    '/', '_').replace('.', '_').replace('_{}', '')
                temp = '{}/{}_template{}'.format(template,
                                                 modulename, os.path.splitext(fn)[1])
                exec('import function_generator.generate_{}'.format(modulename))
                s = None
                with io.open(temp, 'rt', encoding='utf_8_sig') as f:
                    s = f.read()
                if s:
                    code = eval(
                        ("function_generator.generate_{}.generate" +
                         "(info['Functions'][category][function], function, function_name, s)").format(modulename))
                if code:
                    check_update(filename, code)
