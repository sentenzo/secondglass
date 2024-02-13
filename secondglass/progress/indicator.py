class IProgressIndicator:
    def __init__(self, window_id: int) -> None:
        pass

    def set_value(self, val: float) -> None:
        raise NotImplementedError

    def set_state_noprogress(self) -> None:
        raise NotImplementedError

    def set_state_indeterminate(self) -> None:
        raise NotImplementedError

    def set_state_normal(self) -> None:
        raise NotImplementedError

    def set_state_error(self) -> None:
        raise NotImplementedError

    def set_state_paused(self) -> None:
        raise NotImplementedError


class Dummy(IProgressIndicator):
    def set_value(self, val: float) -> None:
        raise NotImplementedError

    def set_state_noprogress(self) -> None:
        pass

    def set_state_indeterminate(self) -> None:
        pass

    def set_state_normal(self) -> None:
        pass

    def set_state_error(self) -> None:
        pass

    def set_state_paused(self) -> None:
        pass
