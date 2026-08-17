class Session:
    def __init__(self,
                 env,
                 read_fn,
                 eval_fn,
                 on_error_cb,
                 ctx=None):
        self.env = env
        self.ctx = ctx
        self.read_fn = read_fn
        self.eval_fn = eval_fn
        self.on_error_cb = on_error_cb
        self.history = []

    def evaluate(self, expr, append_history=True):
        try:
            parsed = self.read_fn(expr)
            res, env = self.eval_fn(parsed, self.env, self.ctx)
            if append_history:
                self.history.append([expr, str(res)])
            self.env = env
            return res
        except Exception as e:
            self.on_error_cb(expr, e)
            return None

    def current_env(self):
        return self.env

    def update(self):
        f = self.env['hexp-update']
        if f:
            self.evaluate("(hexp-update)", append_history=False)

    def draw(self):
        f = self.env['hexp-draw']
        if f:
            self.evaluate("(hexp-draw)", append_history=False)
