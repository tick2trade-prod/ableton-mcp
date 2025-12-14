# Ableton Manual References for 6 New Agents

Based on `artifacts/agent_enhancements_summary.md` and I Am Machine spec.

## 1. Sidechain Agent

**Ableton Manual References**:
- **Section 28.9.2** "Compressor Tips" (page 521)
  - Excerpt: "These can either be frequencies in the compressed signal or, by using the EQ in conjunction with an external sidechain, frequencies in another track's audio."
- **Section 17.5.2** "Internal Routing" (page 363)
  - Excerpt: "Tap Points for Every Chain in a Track. If a track has one or more Instrument or Effect Racks in its device chain, internal routing points (Pre FX, Post FX and Post Mixer) will also be available..."

**Use in Test Docstrings**:
```python
"""Tests for SidechainAgent - Sidechain compression routing.

Reference: Ableton Manual Section 28.9.2 "Compressor Tips" (page 521)
Reference: Ableton Manual Section 17.5.2 "Internal Routing" (page 363)
"""
```

---

## 2. Sampler/Granular Agent

**Ableton Manual References**:
- **Section 30.4.2** "Playback Effects Section - Drum Sampler" (page 660)
  - Excerpt: "You can apply one of nine playback effects to further sculpt a sample's sound: Stretch, Loop, Pitch..."
- **Section 30.10.3** "Sampler Zone Tab" (page 702)
  - Slice mode, loop selector, sample playback
- **Section 28.31** "Granulator III" (page 579)
  - Granular synthesis parameters

**Use in Test Docstrings**:
```python
"""Tests for SamplerAgent - Sample manipulation and granular synthesis.

Reference: Ableton Manual Section 30.4.2 "Drum Sampler Playback" (page 660)
Reference: Ableton Manual Section 28.31 "Granulator III" (page 579)
"""
```

---

## 3. Groove/Quantization Agent

**Ableton Manual References**:
- **Section 14.1** "Groove Pool" (page 326)
  - Relevance: 0.69
  - Excerpt: "The Hot-Swap Groove Button. Grooves can be applied to both audio and MIDI clips. In audio clips, grooves work by adjusting the clip's warping behavior, and thus only work on clips with Warp enabled."
- **Section 10.5.12** "Editing Velocities" (page 258)
  - Velocity humanization

**Use in Test Docstrings**:
```python
"""Tests for GrooveAgent - Groove templates and quantization.

Reference: Ableton Manual Section 14.1 "Groove Pool" (page 326)
Reference: Ableton Manual Section 10.5.12 "Editing Velocities" (page 258)
"""
```

---

## 4. Return Track Agent

**Ableton Manual References**:
- **Section 18.4** "Return Tracks and the Main Track" (page 381)
  - Excerpt: "Return tracks can process audio sent to them from numerous tracks."
- **Section 18.1** "The Live Mixer" (page 376)
  - Send knobs and routing
- **Section 28.19** "Hybrid Reverb" (page 542)
  - Reverb configuration for returns

**Use in Test Docstrings**:
```python
"""Tests for ReturnTrackAgent - Return track and send management.

Reference: Ableton Manual Section 18.4 "Return Tracks" (page 381)
Reference: Ableton Manual Section 18.1 "The Live Mixer - Sends" (page 376)
"""
```

---

## 5. Advanced Automation Agent

**Ableton Manual References**:
- **Section 40.5.1** "Navigating Between Breakpoints" (page 927)
  - Relevance: 0.61
  - Excerpt: "The current location on the grid. Use the left and right arrow keys to move the insert marker. As you move across the envelope, the automation or modulation value at the current location is displayed."
- **Section 6.1** "Arrangement View Layout" (page 145)
  - Timeline automation structure
- **Section 11.2.5** "LFO" (page 284)
  - Modulation envelope shapes

**Use in Test Docstrings**:
```python
"""Tests for AutomationAgent - Parameter automation and envelopes.

Reference: Ableton Manual Section 40.5.1 "Navigating Breakpoints" (page 927)
Reference: Ableton Manual Section 6.1 "Arrangement View" (page 145)
"""
```

---

## 6. Browser/Library Agent

**Ableton Manual References**:
- **Section 5.1** "Browser Overview" (page 113)
  - Browser navigation, search, categories
- **Section 5.3** "Searching and Filtering" (page 120)
  - Sound Similarity search, tag filtering
- **Section 5.4** "Hot-Swap Mode" (page 123)
  - Quick device/sample replacement

**Use in Test Docstrings**:
```python
"""Tests for BrowserAgent - Sample and preset browser integration.

Reference: Ableton Manual Section 5.3 "Searching and Filtering" (page 120)
Reference: Ableton Manual Section 5.4 "Hot-Swap Mode" (page 123)
"""
```

---

## Quick Reference Table

| Agent | Primary Reference | Page | Relevance |
|-------|-------------------|------|-----------|
| Sidechain | 28.9.2 Compressor Tips | 521 | HIGH |
| Sampler/Granular | 30.4.2 Drum Sampler | 660 | HIGH |
| Groove | 14.1 Groove Pool | 326 | MEDIUM |
| Return Track | 18.4 Return Tracks | 381 | MEDIUM |
| Automation | 40.5.1 Breakpoints | 927 | MEDIUM |
| Browser | 5.3 Searching | 120 | LOW |

---

## Implementation Notes

- Add these references to test file docstrings (module level)
- Add specific page references to test method docstrings
- Include relevant excerpts in class docstrings for context
- Update agent implementation files with same references

## Example Pattern (from test_percussion_agent.py)

```python
"""Tests for PercussionAgent - Drum rack and percussion setup.

Reference: Ableton Manual Section 34.3.1 "Loop Selector" (page 797)
Reference: Ableton Manual Section 24.4.1 "Drum Rack Basics" (page 446)

TDD Workflow:
- 🔴 RED: Write failing test
- 🟢 GREEN: Implement minimum code to pass
- 🔄 REFACTOR: Clean up with tests as safety net
"""

class TestPercussionAgentDrumRack:
    """Test drum rack configuration.

    Reference: Ableton Manual Section 24.4.1 "Drum Rack Basics" (page 446)
    """

    def test_configure_drum_rack_basic(self, mock_mcp_client):
        """Test basic drum rack configuration.

        Reference: Page 446 - Drum Rack 4x4 pad layout

        🔴 RED: This test should fail - method doesn't exist yet
        """
        # ...
```
