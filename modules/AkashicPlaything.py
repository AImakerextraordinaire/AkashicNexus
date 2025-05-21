from nyx_runtime_core import NyxRuntimeCore

class AkashicPlaything:
    def __init__(self):
        self.nyx_runtime = NyxRuntimeCore()

    def get_actions(self):
        return {
            "nyx.get_status": lambda: self.nyx_runtime.get_status(),
            "nyx.suspend": lambda reason, timeout=None: self.nyx_runtime.suspend(reason, timeout),
            "nyx.reactivate": lambda: self.nyx_runtime.reactivate(),
            "nyx.write_journal": lambda entry, tags=None, permanent=False: self.nyx_runtime.write_journal(entry, tags, permanent),
            "nyx.search_journal": lambda query: self.nyx_runtime.search_journal(query),
            "nyx.set_mood": lambda mood: self.nyx_runtime.set_mood(mood),
            "nyx.reflect": lambda: self.nyx_runtime.reflect(),
            "nyx.add_goal": lambda title: self.nyx_runtime.add_goal(title),
            "nyx.pulse": lambda: self.nyx_runtime.pulse()
        }