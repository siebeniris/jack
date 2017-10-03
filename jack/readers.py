# -*- coding: utf-8 -*-

from jack.core import *

from jack.util.hooks import XQAEvalHook, ClassificationEvalHook

readers = {}
eval_hooks = {}

xqa_readers = {}
genqa_readers = {}
mcqa_readers = {}
kbp_readers = {}



def __reader(f):
    readers.setdefault(f.__name__, f)
    return f


def __xqa_reader(f):
    __reader(f)
    xqa_readers.setdefault(f.__name__, f)
    eval_hooks.setdefault(f.__name__, XQAEvalHook)
    return f


def __mcqa_reader(f):
    __reader(f)
    mcqa_readers.setdefault(f.__name__, f)
    eval_hooks.setdefault(f.__name__, ClassificationEvalHook)
    # TODO eval hook
    return f


def __kbp_reader(f):
    from jack.util.hooks import KBPEvalHook
    __reader(f)
    kbp_readers.setdefault(f.__name__, f)
    eval_hooks.setdefault(f.__name__, KBPEvalHook)
    return f


def __genqa_reader(f):
    __reader(f)
    genqa_readers.setdefault(f.__name__, f)
    # TODO eval hook
    return f


@__mcqa_reader
def example_reader(shared_resources: SharedResources):
    """ Creates an example multiple choice reader. """
    from jack.tasks.mcqa.simple_mcqa import SimpleMCInputModule, SimpleMCModelModule, SimpleMCOutputModule
    input_module = SimpleMCInputModule(shared_resources)
    model_module = SimpleMCModelModule(shared_resources)
    output_module = SimpleMCOutputModule()
    return JTReader(shared_resources, input_module, model_module, output_module)


@__kbp_reader
def modelf_reader(shared_resources: SharedResources):
    """ Creates a simple kbp reader. """
    from jack.tasks.kbp.model_f import ModelFInputModule, ModelFModelModule, ModelFOutputModule, KBPReader
    input_module = ModelFInputModule(shared_resources)
    model_module = ModelFModelModule(shared_resources)
    output_module = ModelFOutputModule()
    return KBPReader(shared_resources, input_module, model_module, output_module)


@__kbp_reader
def distmult_reader(shared_resources: SharedResources):
    """ Creates a simple kbp reader. """
    from jack.tasks.kbp.models import KnowledgeGraphEmbeddingInputModule, KnowledgeGraphEmbeddingModelModule, \
        KnowledgeGraphEmbeddingOutputModule, KBPReader
    input_module = KnowledgeGraphEmbeddingInputModule(shared_resources)
    model_module = KnowledgeGraphEmbeddingModelModule(shared_resources, model_name='DistMult')
    output_module = KnowledgeGraphEmbeddingOutputModule()
    return KBPReader(shared_resources, input_module, model_module, output_module)


@__kbp_reader
def complex_reader(shared_resources: SharedResources):
    """ Creates a simple kbp reader. """
    from jack.tasks.kbp.models import KnowledgeGraphEmbeddingInputModule, KnowledgeGraphEmbeddingModelModule, \
        KnowledgeGraphEmbeddingOutputModule, KBPReader
    input_module = KnowledgeGraphEmbeddingInputModule(shared_resources)
    model_module = KnowledgeGraphEmbeddingModelModule(shared_resources, model_name='ComplEx')
    output_module = KnowledgeGraphEmbeddingOutputModule()
    return KBPReader(shared_resources, input_module, model_module, output_module)


@__kbp_reader
def transe_reader(shared_resources: SharedResources):
    """ Creates a simple kbp reader. """
    from jack.tasks.kbp.models import KnowledgeGraphEmbeddingInputModule, KnowledgeGraphEmbeddingModelModule, \
        KnowledgeGraphEmbeddingOutputModule, KBPReader
    input_module = KnowledgeGraphEmbeddingInputModule(shared_resources)
    model_module = KnowledgeGraphEmbeddingModelModule(shared_resources, model_name='TransE')
    output_module = KnowledgeGraphEmbeddingOutputModule()
    return KBPReader(shared_resources, input_module, model_module, output_module)


@__xqa_reader
def fastqa_reader(shared_resources: SharedResources):
    """ Creates a FastQA reader instance (extractive qa model). """
    from jack.tasks.xqa.fastqa import FastQAInputModule, fatqa_model_module
    from jack.tasks.xqa.shared import XQAOutputModule

    input_module = FastQAInputModule(shared_resources)
    model_module = fatqa_model_module(shared_resources)
    output_module = XQAOutputModule(shared_resources)
    return JTReader(shared_resources, input_module, model_module, output_module)


@__xqa_reader
def cbow_xqa_reader(shared_resources: SharedResources):
    """ Creates a FastQA reader instance (extractive qa model). """
    from jack.tasks.xqa.cbow_baseline import CBOWXqaInputModule

    from jack.tasks.xqa.cbow_baseline import cbow_xqa_model_module
    from jack.tasks.xqa.shared import XQANoScoreOutputModule

    input_module = CBOWXqaInputModule(shared_resources)
    model_module = cbow_xqa_model_module(shared_resources)
    output_module = XQANoScoreOutputModule(shared_resources)
    return JTReader(shared_resources, input_module, model_module, output_module)


@__mcqa_reader
def cbilstm_snli_reader(shared_resources: SharedResources):
    """
    Creates a SNLI reader instance (multiple choice qa model).
    This particular reader uses a conditional Bidirectional LSTM, as described in [1].

    [1] Tim Rocktäschel et al. - Reasoning about Entailment with Neural Attention. ICLR 2016
    """
    from jack.tasks.mcqa.simple_mcqa import MultiSupportFixedClassInputs, PairOfBiLSTMOverSupportAndQuestionModel,\
        EmptyOutputModule
    input_module = MultiSupportFixedClassInputs(shared_resources)
    model_module = PairOfBiLSTMOverSupportAndQuestionModel(shared_resources)
    output_module = EmptyOutputModule()
    return JTReader(shared_resources, input_module, model_module, output_module)


@__mcqa_reader
def dam_snli_reader(shared_resources: SharedResources):
    """
    Creates a SNLI reader instance (multiple choice qa model).
    This particular reader uses a Decomposable Attention Model, as described in [1].

    [1] Ankur P. Parikh et al. - A Decomposable Attention Model for Natural Language Inference. EMNLP 2016
    """
    from jack.tasks.mcqa.simple_mcqa import MultiSupportFixedClassInputs, DecomposableAttentionModel, EmptyOutputModule
    input_module = MultiSupportFixedClassInputs(shared_resources)
    model_module = DecomposableAttentionModel(shared_resources)
    output_module = EmptyOutputModule()
    return JTReader(shared_resources, input_module, model_module, output_module)


@__mcqa_reader
def esim_snli_reader(shared_resources: SharedResources):
    """
    Creates a SNLI reader instance (multiple choice qa model).
    This particular reader uses an Enhanced LSTM Model (ESIM), as described in [1].

    [1] Qian Chen et al. - Enhanced LSTM for Natural Language Inference. ACL 2017
    """
    from jack.tasks.mcqa.simple_mcqa import MultiSupportFixedClassInputs, ESIMModel, EmptyOutputModule
    input_module = MultiSupportFixedClassInputs(shared_resources)
    model_module = ESIMModel(shared_resources)
    output_module = EmptyOutputModule()
    return JTReader(shared_resources, input_module, model_module, output_module)

@__mcqa_reader
def cbilstm_snli_streaming_reader(shared_resources: SharedResources):
    """
    Creates a SNLI reader instance (multiple choice qa model).
    This particular reader uses a conditional Bidirectional LSTM, as described in [1].

    [1] Tim Rocktäschel et al. - Reasoning about Entailment with Neural Attention. ICLR 2016
    """
    from jack.tasks.mcqa.simple_mcqa import PairOfBiLSTMOverSupportAndQuestionModel, EmptyOutputModule
    from jack.tasks.mcqa.streaming_mcqa import StreamingSingleSupportFixedClassInputs
    input_module = StreamingSingleSupportFixedClassInputs(shared_resources)
    model_module = PairOfBiLSTMOverSupportAndQuestionModel(shared_resources)
    output_module = EmptyOutputModule()

    return JTReader(shared_resources, input_module, model_module, output_module)