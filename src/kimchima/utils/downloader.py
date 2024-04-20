
# coding=utf-8
# Copyright [2024] [SkywardAI]
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations


import os
import shutil
from functools import lru_cache

from kimchima.pkg import logging

logger=logging.get_logger(__name__)


class Downloader:
    r"""
    This class is designed to download the model from Huggingface and save it to the specified folder.
    """

    def __init__(self):
        raise EnvironmentError(
            "Embeddings is designed to be instantiated "
            "using the `Embeddings.from_pretrained(pretrained_model_name_or_path)` method."
        )

    @classmethod
    def _move_files_and_remove_dir(cls, src_folder, dst_folder):
        for filename in os.listdir(src_folder):
            dst_file = os.path.join(dst_folder, filename)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.move(os.path.join(src_folder, filename), dst_folder)
        shutil.rmtree(src_folder)

    @classmethod
    @lru_cache(maxsize=1)
    def model_downloader(cls, *args, **kwargs):
        r"""
        Here we will use pipeline from Huggingface to download the model.
        And save the model to the specified folder.
        """
        model_name=kwargs.pop("model_name", None)
        if model_name is None:
            raise ValueError("model_name is required")
        
        pipe=kwargs.pop("pipe", None)
        if pipe is None:
            raise ValueError("pipe is required")

        folder_name=kwargs.pop("folder_name", None)
        
        pipe.save_pretrained(folder_name if folder_name is not None else model_name)
        logger.info(f"Model {model_name} has been downloaded successfully")

    
    @classmethod
    @lru_cache(maxsize=1)
    def auto_downloader(cls, *args, **kwargs):
        r"""
        Here we will use AutoModel from Huggingface to download the model.
        It support a wider range of models beyond causal language models,
        like BERT, RoBERTa, BART, T5 and more.

        It returns the base model without a specific head, it does not directly
        perform tasks like text generation or translation.

        Args:
            model_name: str
                The model name to download.
            model: model instance
                The model to download.
            tokenizer: str
                The tokenizer to download.
            folder_name: str
                The folder name to save the model.
        """

        model_name=kwargs.pop("model_name", None)
        if model_name is None:
            raise ValueError("model_name is required")
        
        model=kwargs.pop("model", None)
        if model is None:
            raise ValueError("model is required")
        
        tokenizer=kwargs.pop("tokenizer", None)
        if tokenizer is None:
            raise ValueError("tokenizer is required")

        folder_name=kwargs.pop("folder_name", None)
        if folder_name is None:
            folder_name = model_name

        # save_pretrained only saves the model weights, not the configuration
        model.save_pretrained(folder_name)
        
        tokenizer.save_pretrained(folder_name + "/tmp1", legacy_format=False)
        tokenizer.save_pretrained(folder_name + "/tmp2", legacy_format=True)

        for tmp_folder in ["/tmp1", "/tmp2"]:
            cls._move_files_and_remove_dir(folder_name+ tmp_folder, folder_name)
        logger.info(f"Model {model_name} has been downloaded successfully")

    
    @classmethod
    @lru_cache(maxsize=1)
    def casual_downloader(cls, *args, **kwargs):
        r"""
        Here we will use AutoModelForCausalLM from Huggingface to download the model
        Like GPT-2 XLNet etc. 
        It return a language modeling head which can be used to generate text,
        translate text, write content, answer questions in a informative way.
        """
        model_name=kwargs.pop("model_name", None)
        if model_name is None:
            raise ValueError("model_name is required")
        model=kwargs.pop("model", None)
        if model is None:
            raise ValueError("model is required")

        folder_name=kwargs.pop("folder_name", None)
        # https://github.com/huggingface/transformers/issues/25296
        # https://github.com/huggingface/accelerate/issues/661

        model.save_pretrained(folder_name if folder_name is not None else model_name)
        logger.info(f"Model {model_name} has been downloaded successfully")

    @classmethod
    @lru_cache(maxsize=1)
    def auto_token_downloader(cls, *args, **kwargs):
        r"""
        Here we will use AutoTokenizer from Huggingface to download the tokenizer congifuration.
        """
        model_name=kwargs.pop("model_name", None)
        if model_name is None:
            raise ValueError("model_name is required")
        
        tokenizer=kwargs.pop("tokenizer", None)
        if tokenizer is None:
            raise ValueError("tokenizer is required")

        folder_name=kwargs.pop("folder_name", None)
        
        tokenizer.save_pretrained(folder_name if folder_name is not None else model_name)
        logger.info(f"Tokenizer {model_name} has been downloaded successfully")

