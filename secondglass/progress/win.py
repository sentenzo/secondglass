import sys
from math import ceil

from .indicator import IProgressIndicator

# https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nf-shobjidl_core-itaskbarlist3-setprogressstate

TBPF_NOPROGRESS = 0x00000000
TBPF_INDETERMINATE = 0x00000001
TBPF_NORMAL = 0x00000002
TBPF_ERROR = 0x00000004
TBPF_PAUSED = 0x00000008

PROGRESS_MAX_VAL = 100_000


class TaskbarProgressIndicatorWin(IProgressIndicator):
    def __init__(self, window_id: int) -> None:
        self.window_handler = window_id
        if not sys.platform == "win32":
            raise NotImplementedError("Can only run on Windows")

        import comtypes.client as cc

        cc.GetModule("./TaskbarLib.tlb")
        from comtypes.gen.TaskbarLib import ITaskbarList3

        self.taskbar = cc.CreateObject(
            "{56FDF344-FD6D-11d0-958A-006097C9A090}",
            interface=ITaskbarList3,
        )
        self.taskbar.HrInit()
        self.taskbar.ActivateTab(self.window_handler)
        self.set_value(0.0)
        self.set_state_noprogress()

    def set_value(self, val: float) -> None:
        int_val = min(ceil(val * PROGRESS_MAX_VAL), PROGRESS_MAX_VAL)
        self.taskbar.SetProgressValue(
            self.window_handler, int_val, PROGRESS_MAX_VAL
        )

    def set_state_noprogress(self) -> None:
        self.taskbar.SetProgressState(self.window_handler, TBPF_NOPROGRESS)

    def set_state_indeterminate(self) -> None:
        self.taskbar.SetProgressState(self.window_handler, TBPF_INDETERMINATE)

    def set_state_normal(self) -> None:
        self.taskbar.SetProgressState(self.window_handler, TBPF_NORMAL)

    def set_state_error(self) -> None:
        self.taskbar.SetProgressState(self.window_handler, TBPF_ERROR)

    def set_state_paused(self) -> None:
        self.taskbar.SetProgressState(self.window_handler, TBPF_PAUSED)
