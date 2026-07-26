class Session:
    def __init__(self,
                 env,
                 read_fn,
                 eval_fn,
                 ctx=None):
        self.env = env
        self.ctx = ctx
        self.read_fn = read_fn
        self.eval_fn = eval_fn

    def evaluate(self, expr):
        parsed = self.read_fn(expr)
        res, env = self.eval_fn(parsed, self.env, self.ctx)
        self.env = env
        return res

    def currnt_env(self):
        return self.env
