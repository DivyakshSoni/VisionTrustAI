from typing import Dict, Any, Callable
import logging

logger = logging.getLogger(__name__)

class CanaryGate:
    """
    Implements ZTAAF Principle 4: Assume the verifier is breached.
    Every detector must pass a known-answer canary self-test before its output is trusted.
    """
    def __init__(self):
        self.canary_results: Dict[str, bool] = {}

    def run_canary_test(
        self, 
        detector_id: str, 
        detector_fn: Callable, 
        canary_input: Any, 
        expected_output: Any,
        tolerance_fn: Callable[[Any, Any], bool] = lambda out, exp: out == exp
    ) -> bool:
        """
        Executes a detector against a frozen canary set.
        """
        try:
            actual_output = detector_fn(canary_input)
            passed = tolerance_fn(actual_output, expected_output)
        except Exception as e:
            logger.error(f"Canary test for {detector_id} failed with exception: {e}")
            passed = False
            
        self.canary_results[detector_id] = passed
        if not passed:
            logger.warning(f"[ZTAAF ALERT] Detector {detector_id} failed canary check! Its evidence will be excluded.")
            self._trigger_retroactive_review(detector_id)
            
        return passed
        
    def has_passed(self, detector_id: str) -> bool:
        """
        Returns True if the detector has passed its canary test in this session.
        """
        return self.canary_results.get(detector_id, False)

    def _trigger_retroactive_review(self, detector_id: str):
        """
        Flags prior judgments made by this detector for re-review.
        In a full implementation, this would query the Findings database and flag records.
        """
        print(f"[Retroactive Review] Flagging all previous findings by {detector_id} in this session as 'verifier_integrity_compromised'")

# Global instance for the session orchestration
gate = CanaryGate()
