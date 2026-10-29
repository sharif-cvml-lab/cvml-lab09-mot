from __future__ import annotations

from tracking_types import Detection, Track, compute_iou


class Tracker:
    def __init__(self, iou_threshold: float = 0.3, max_age: int = 15, min_hits: int = 3):
        """Already implemented. Do NOT modify.

        iou_threshold: minimum IoU for a detection to be associated with a track.
        max_age:       a track is deleted after more than max_age consecutive missed frames.
        min_hits:      a track is reported only after it has been matched at least this many times.

        The GUI changes these three attributes live, so always read them from self inside update().
        """
        self.iou_threshold = iou_threshold
        self.max_age = max_age
        self.min_hits = min_hits
        self.tracks: list[Track] = []  # every track that is still alive
        self.next_id = 1               # the ID given to the next new track

    def update(self, detections: list[Detection]) -> list[Track]:
        """
        TODO: Implement a minimal IoU tracker.

        IMPORTANT:

        - This is the only file students should modify.
        - Keep the class name, __init__ and the signature of update() unchanged.
        - Do not add other top-level functions or classes to this file.
        - Do not use scipy, cv2 trackers or any other tracking library. Plain Python and
          the helpers imported above are enough.

        Called once per frame, in order.

        Input:

            detections: list of Detection (box, score, class_id) for the current frame.
                        It can be empty.

        Available helpers (see tracking_types.py):

            compute_iou(box_a, box_b)  -> IoU of two boxes
            Track(track_id, detection) -> new track (hits = 1, missed = 0)
            track.update(detection)    -> call when the track is matched in this frame
            track.mark_missed()        -> call when the track is NOT matched in this frame
            track.box, track.class_id, track.hits, track.missed, track.id

        Expected implementation sequence:

        1. Association candidates: for every (track, detection) pair of the SAME class,
           compute the IoU and keep the pair only if IoU >= self.iou_threshold.
        2. Greedy matching: sort the candidate pairs by IoU, highest first. Walk through them
           and accept a pair only if neither its track nor its detection is already matched.
           Call track.update(detection) for every accepted pair.
        3. Unmatched tracks: call track.mark_missed().
        4. Unmatched detections: create a new Track with ID self.next_id, append it to
           self.tracks, and increase self.next_id.
        5. Track deletion: remove every track whose missed counter is greater than self.max_age.
        6. Return only the tracks that have been matched at least self.min_hits times
           (these include confirmed tracks that are currently missed/lost).

        Edge cases to handle: no detections (all tracks are missed), no tracks yet (all
        detections give birth to new tracks), and two tracks competing for one detection.

        Keep the implementation deterministic and free of GUI code.
        """
        return []
