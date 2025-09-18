from typing import Annotated, Sequence, TypedDict, List, Union, Dict, Any, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class AgentState_temp(TypedDict):
    name: str
    kuch_bhi: str
    messages_l1: Annotated[Sequence[BaseMessage], add_messages]



class AgentState(TypedDict):
    # top-level metadata
    schema_version: str           # e.g. "1.0"
    message_id: str               # uuid
    trace_id: str                 # uuid
    created_at: str               # timestamp (ISO 8601 recommended)
    panel_id: str

    defect_type: str
    issue_critical: bool

    # nested objects (kept as generic dicts because we must use a single TypedDict)
    # work_order: expected keys: "order_id": str, optional "vin": str
    work_order: Dict[str, Optional[str]]

    # source: expected keys: "edge_id": str, "camera_id": str, "model_version": str
    source: Dict[str, str]

    # environment: expected keys:
    #   "temperature_c": float,
    #   "humidity_pct": float,
    #   optional "spray_pressure_bar": float,
    #   "other_sensors": dict (free-form)
    environment: Dict[str, Any]

    # images: 
    #   { "image_id": str, "uri": str, "camera_pose": dict, "timestamp": str }
    image: Dict[str, Any] #could be made a list of objects with expected shape:  List[Dict[str, Any]]


    # timing
    processing_latency_ms: float

    #agent layers
    reasoning_layer_messages: Annotated[Sequence[BaseMessage], add_messages]
    reasoning_layer_output: str
    action_layer_messages: Annotated[Sequence[BaseMessage], add_messages]
    action_layer_output: str
    learning_layer_flags: Dict[str, bool] # keys: "confirmed_defect_type", "confirmed_root_cause", "was_issue_resolved_by_suggested_changes"
    learning_layer_correct_values: Dict[str, str] # keys: "defect_type", "root_cause", "issue_resolved"
    # learning_layer_messages: Annotated[Sequence[BaseMessage], add_messages]
    suggestion_to_resolve_issue: str


    # detections: list of objects with expected shape:
    #   {
    #     "defect_id": str,
    #     "type": str,
    #     optional "subtype": str,
    #     "confidence": float,    # 0..1
    #     "severity": float,      # 0..1
    #     "bbox": List[Union[int,float]], # [x1,y1,x2,y2] pixels
    #     optional "mask_uri": str,
    #     optional "physical_size_mm": float,
    #     optional "notes": str
    #   }
    # detections: List[Dict[str, Any]]


