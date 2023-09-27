from typing import Any, Type

from pydantic import BaseModel, ValidationError


class Validator(BaseModel):

    def __init__(self, **data: Any):
        if not data:
            raise ValidationError("At least one argument is required")
        super().__init__(**data)

    class Config:
        extra = 'allow'
        arbitrary_types_allowed = True

from enum import Enum


class States(Enum):
    INIT = 'init'
    READY = 'ready'
    INPUT_VALIDATION = 'input validation'
    RUNNING = 'running'
    OUTPUT_VALIDATION = 'output validation'
    PROCESSING_OUTPUT = 'processing output'
    COMPLETE = 'complete'
    FAILED = 'failed'


ALLOWED_TRANSITIONS = {
    None: [States.INIT],
    States.INIT: [States.INPUT_VALIDATION, States.FAILED],
    #States.READY: [States.INPUT_VALIDATION, States.FAILED],
    States.INPUT_VALIDATION: [States.RUNNING, States.FAILED],
    States.RUNNING: [States.OUTPUT_VALIDATION, States.FAILED],
    States.OUTPUT_VALIDATION: [States.COMPLETE, States.PROCESSING_OUTPUT, States.FAILED],
    States.PROCESSING_OUTPUT: [States.COMPLETE, States.FAILED, States.INPUT_VALIDATION], #input validation when running a function again
    States.COMPLETE: [States.INPUT_VALIDATION],
    States.FAILED: [States.INPUT_VALIDATION]
}

import os

from langfuse import Langfuse
from langfuse.api.model import CreateTrace, CreateGeneration, UpdateGeneration, CreateSpan, UpdateSpan, CreateScore

langfuse_client = Langfuse(
    public_key=os.environ['LANGFUSE_PUBLIC_KEY'],
    secret_key=os.environ['LANGFUSE_SECRET_KEY'],
    host="https://cloud.langfuse.com/"
)


class LLMTrace:

    def __init__(self,
                 **kwargs):
        self.trace = langfuse_client.trace(CreateTrace(**kwargs))

    def create_generation(self,
                          **kwargs):
        self.current_generation = self.trace.generation(CreateGeneration(
            **kwargs))

    def update_generation(self,
                          **kwargs):
        self.current_generation.update(UpdateGeneration(
            **kwargs
        ))

    def create_span(self,
                    **kwargs):
        self.current_span = self.trace.span(CreateSpan(**kwargs))

    def update_span(self,
                    **kwargs):
        self.current_span.update(UpdateSpan(**kwargs))

    def score_generation(self,
                         **kwargs):
        self.current_generation.score(CreateScore(**kwargs))