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

    def default_hooks(self):
        self.evaluate("(def hexp-init (fn () {}))", append_history=False)
        self.evaluate("(def hexp-update (fn (state) state))", append_history=False)
        self.evaluate("(def hexp-draw (fn (state) state))", append_history=False)

    # allow the user defined program a hook to initialise the ongoing hexp state
    def prog_init(self):
        self.evaluate("(def hexp-state (hexp-init))", append_history=False)

    def update(self):
        f = self.env['hexp-update']
        if f:
            self.evaluate("(hexp-update hexp-state)", append_history=False)

    def draw(self):
        f = self.env['hexp-draw']
        if f:
            self.evaluate("(hexp-draw hexp-state)", append_history=False)
