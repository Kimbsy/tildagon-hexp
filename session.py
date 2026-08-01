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

    def evaluate(self, expr):
        try:
            parsed = self.read_fn(expr)
            res, env = self.eval_fn(parsed, self.env, self.ctx)
            self.history.insert(0, [expr, str(res)])
            self.env = env
            return res
        except Exception as e:
            self.on_error_cb(e)
            return None

    def current_env(self):
        return self.env

    def update(self):
        f = self.env['hexp-update']
        if f:
            self.evaluate("(hexp-update)")

    def draw(self):
        f = self.env['hexp-draw']
        if f:
            self.evaluate("(hexp-draw)")
