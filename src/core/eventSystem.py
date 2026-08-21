# MARK: eventTarget


from typing import Any, Callable, Dict

EventCallback = Callable[..., Any]
EventMap = Dict[str, list[EventCallback]]


class EventTarget:
  eventMap: EventMap

  def __init__(self):
    self.eventMap = {}

  def add_event_listener(self, name: str, callback: EventCallback):
    """Calls the passed `callback` function when the specified event is triggered."""
    if name not in self.eventMap:
      self.eventMap[name] = []
    self.eventMap[name].append(callback)

  def remove_event_listener(self, name: str, callback: EventCallback):
    """Removes the `callback` function from the stack."""

    if name not in self.eventMap.keys():
      return
    callback_stack = self.eventMap[name]
    if callback not in callback_stack:
      return
    callback_stack.remove(callback)

  def dispatch_event(self, name: str, detail: Dict[Any, Any] | None = None) -> None:
    if name not in self.eventMap:
      self.eventMap[name] = []
    for callback in self.eventMap[name]:
      callback(detail)
