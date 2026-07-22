from langchain_core.runnables import RunnableLambda


class BaseChain:

    def __init__(self, runnable):

        self.chain = runnable

    def invoke(self, inputs):

        return self.chain.invoke(inputs)

    def stream(self, inputs):

        return self.chain.stream(inputs)